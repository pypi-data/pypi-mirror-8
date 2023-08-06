# Copyright (C) 2014 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import logging
import os
import tempfile
import shutil
import random

from gevent import Greenlet
import zmq.green as zmq
from zmq.auth.certs import create_certificates

import beeswarm
from beeswarm.shared.message_enum import Messages
from beeswarm.server.db import database_setup
from beeswarm.server.db.entities import Client, Honeypot, Drone, DroneEdge, BaitUser
from beeswarm.shared.socket_enum import SocketNames



logger = logging.getLogger(__name__)


class ConfigActor(Greenlet):
    def __init__(self, config_file, work_dir, command_requests_only=False):
        Greenlet.__init__(self)
        self.config_file = os.path.join(work_dir, config_file)
        self.commands_only = command_requests_only
        if not os.path.exists(self.config_file):
            self.config = {}
            self._save_config_file()
        self.config = json.load(open(self.config_file, 'r'))
        self.work_dir = work_dir

        context = beeswarm.shared.zmq_context
        self.config_commands = context.socket(zmq.REP)
        self.drone_command_receiver = None

        if not self.commands_only:
            self.drone_command_receiver = context.socket(zmq.PUSH)

        self.enabled = True

    def close(self):
        if self.config_commands:
            self.config_commands.close()
        self.enabled = False

    def _run(self):
        self.config_commands.bind(SocketNames.CONFIG_COMMANDS.value)
        if not self.commands_only:
            self.drone_command_receiver.connect(SocketNames.DRONE_COMMANDS.value)

        poller = zmq.Poller()
        poller.register(self.config_commands, zmq.POLLIN)
        while self.enabled:
            socks = dict(poller.poll(500))
            if self.config_commands in socks and socks[self.config_commands] == zmq.POLLIN:
                self._handle_commands()

    def _handle_commands(self):
        msg = self.config_commands.recv()

        if ' ' in msg:
            cmd, data = msg.split(' ', 1)
        else:
            cmd = msg
        logger.debug('Received command: {0}'.format(cmd))

        if cmd == Messages.SET_CONFIG_ITEM.value:
            self._handle_command_set(data)
            self.config_commands.send('{0} {1}'.format(Messages.OK.value, '{}'))
        elif cmd == Messages.GET_CONFIG_ITEM.value:
            value = self._handle_command_get(data)
            self.config_commands.send('{0} {1}'.format(Messages.OK.value, value))
        elif cmd == Messages.GEN_ZMQ_KEYS.value:
            self._handle_command_genkeys(data)
        elif cmd == Messages.DRONE_CONFIG.value:
            result = self._handle_command_get_droneconfig(data)
            self.config_commands.send('{0} {1}'.format(Messages.OK.value, json.dumps(result)))
        elif cmd == Messages.DRONE_CONFIG_CHANGED.value:
            # send OK straight away - we don't want the sender to wait
            self.config_commands.send('{0} {1}'.format(Messages.OK.value, '{}'))
            self._handle_command_drone_config_changed(data)
        elif cmd == Messages.BAIT_USER_ADD.value:
            self._handle_command_bait_user_add(data)
            self.config_commands.send('{0} {1}'.format(Messages.OK.value, '{}'))
        elif cmd == Messages.BAIT_USER_DELETE.value:
            self._handle_command_bait_user_delete(data)
            self.config_commands.send('{0} {1}'.format(Messages.OK.value, '{}'))
        elif cmd == Messages.DRONE_DELETE.value:
            self._handle_command_delete_drone(data)
            self.config_commands.send('{0} {1}'.format(Messages.OK.value, '{}'))
        elif cmd == Messages.DRONE_ADD.value:
            self._handle_command_add_drone()
        else:
            logger.warning('Unknown command received: {0}'.format(cmd))
            self.config_commands.send(Messages.FAIL.value)

    def _handle_command_set(self, data):
        new_config = json.loads(data)
        self.config.update(new_config)
        self._save_config_file()

    def _handle_command_get(self, data):
        # example: 'network,host' will lookup self.config['network']['host']
        keys = data.split(',')
        value = self._retrieve_nested_config(keys, self.config)
        return value

    def _retrieve_nested_config(self, keys, dict):
        if keys[0] in dict:
            if len(keys) == 1:
                return dict[keys[0]]
            else:
                return self._retrieve_nested_config(keys[1:], dict[keys[0]])

    def _handle_command_genkeys(self, name):
        private_key, publickey = self._get_zmq_keys(name)
        self.config_commands.send(Messages.OK.value + ' ' + json.dumps({'public_key': publickey,
                                                                  'private_key': private_key}))

    def _handle_command_drone_config_changed(self, drone_id):
        self._send_config_to_drone(drone_id)
        self._reconfigure_all_clients()

    def _handle_command_bait_user_delete(self, data):
        bait_user_id = int(data)
        db_session = database_setup.get_session()
        bait_user = db_session.query(BaitUser).filter(BaitUser.id == bait_user_id).first()
        if bait_user:
            db_session.delete(bait_user)
            db_session.commit()
            self._bait_user_changed(bait_user.username, bait_user.password)
        else:
            logger.warning('Tried to delete non-existing bait user with id {0}.'.format(bait_user_id))

    def _handle_command_bait_user_add(self, data):
        username, password = data.split(' ')
        db_session = database_setup.get_session()
        existing_bait_user = db_session.query(BaitUser).filter(BaitUser.username == username,
                                                               BaitUser.password == password).first()
        if not existing_bait_user:
            new_bait_user = BaitUser(username=username, password=password)
            db_session.add(new_bait_user)
            db_session.commit()

    def _bait_user_changed(self, username, password):
        db_session = database_setup.get_session()
        drone_edge = db_session.query(DroneEdge).filter(DroneEdge.username == username,
                                                        DroneEdge.password == password).first()
        # A drone is using the bait users, reconfigure all
        # TODO: This is lazy, we should only reconfigure the drone(s) who are actually
        # using the credentials
        if drone_edge:
            self._reconfigure_all_clients()

    def _send_config_to_drone(self, drone_id):
        config = self._get_drone_config(drone_id)
        logger.debug('Sending config to {0}: {1}'.format(drone_id, config))
        self.drone_command_receiver.send('{0} {1} {2}'.format(drone_id, Messages.CONFIG.value, json.dumps(config)))

    def _handle_command_get_droneconfig(self, drone_id):
        return self._get_drone_config(drone_id)

    def _reconfigure_all_clients(self):
        db_session = database_setup.get_session()
        db_session.query(DroneEdge).delete()
        db_session.commit()
        honeypots = db_session.query(Honeypot).all()
        clients = db_session.query(Client).all()
        # delete old architecture
        credentials = db_session.query(BaitUser).all()
        for honeypot in honeypots:
            for capability in honeypot.capabilities:
                for client in clients:
                    # following three variables should be make somewhat user configurable again
                    client_timings = json.loads(client.bait_timings)
                    if capability.protocol in client_timings:
                        # the time range in which to activate the bait sessions
                        activation_range = client_timings[capability.protocol]['active_range']
                        # period to sleep before using activation_probability
                        sleep_interval = client_timings[capability.protocol]['sleep_interval']
                        # the probability that a bait session will be activated, 1 is always activate
                        activation_probability = client_timings[capability.protocol]['activation_probability']
                    else:
                        logger.warning('Bait timings for {0} not found on client drone {1}({2}), using defaults instead'
                                       .format(capability.protocol, client.name, client.id))
                        activation_range = '00:00 - 23:59'
                        sleep_interval = '60'
                        activation_probability = 1
                    bait_credentials = random.choice(credentials)
                    client.add_bait(capability, activation_range, sleep_interval,
                                    activation_probability, bait_credentials.username, bait_credentials.password)
        db_session.commit()

        drones = db_session.query(Drone).all()
        for drone in drones:
            self._send_config_to_drone(drone.id)

    def _get_drone_config(self, drone_id):
        db_session = database_setup.get_session()
        drone = db_session.query(Honeypot).filter(Drone.id == drone_id).first()
        # lame! what is the correct way?
        if not drone:
            drone = db_session.query(Client).filter(Drone.id == drone_id).first()
        if not drone:
            drone = db_session.query(Drone).filter(Drone.id == drone_id).first()
        if not drone:
            self.config_commands.send(Messages.FAIL.value)

        server_zmq_url = 'tcp://{0}:{1}'.format(self.config['network']['server_host'],
                                                self.config['network']['zmq_port'])
        server_zmq_command_url = 'tcp://{0}:{1}'.format(self.config['network']['server_host'],
                                                        self.config['network']['zmq_command_port'])

        private_key, public_key = self._get_zmq_keys(str(drone.id))

        # common section that goes for all types of drones
        drone_config = {
            'general': {
                'mode': drone.discriminator,
                'id': int(drone.id),
                'fetch_ip': False,
                'name': drone.name
            },
            'beeswarm_server': {
                'zmq_url': server_zmq_url,
                'zmq_command_url': server_zmq_command_url,
                'zmq_server_public': self.config['network']['zmq_server_public_key'],
                'zmq_own_public': public_key,
                'zmq_own_private': private_key,
            },
            'timecheck': {
                'enabled': True,
                'poll': 5,
                'ntp_pool': 'pool.ntp.org'
            }
        }

        if drone.discriminator == 'honeypot':
            drone_config['certificate_info'] = {
                'common_name': drone.cert_common_name,
                'country': drone.cert_country,
                'state': drone.cert_state,
                'locality': drone.cert_locality,
                'organization': drone.cert_organization,
                'organization_unit': drone.cert_organization_unit
            }
            drone_config['capabilities'] = {}
            for capability in drone.capabilities:
                users = {}
                for bait in capability.baits:
                    users[bait.username] = bait.password
                drone_config['capabilities'][capability.protocol] = {'port': capability.port,
                                                                     'enabled': True,
                                                                     'protocol_specific_data': json.loads(
                                                                         capability.protocol_specific_data),
                                                                     'users': users}
        elif drone.discriminator == 'client':
            drone_config['baits'] = {}
            for bait in drone.baits:
                _bait = {'server': bait.capability.honeypot.ip_address,
                         'port': bait.capability.port,
                         'honeypot_id': bait.capability.honeypot_id,
                         'username': bait.username,
                         'password': bait.password,
                         'active_range': bait.activation_range,
                         'sleep_interval': bait.sleep_interval,
                         'activation_probability': bait.activation_probability}
                if bait.capability.honeypot_id not in drone_config['baits']:
                    drone_config['baits'][bait.capability.honeypot_id] = {}
                assert bait.capability.protocol not in drone_config['baits'][bait.capability.honeypot_id]
                drone_config['baits'][bait.capability.honeypot_id][bait.capability.protocol] = _bait
            if drone.bait_timings:
                drone_config['bait_timings'] = json.loads(drone.bait_timings)
            else:
                drone_config['bait_timings'] = {}

        return drone_config

    def _save_config_file(self):
        with open(self.config_file, 'w+') as config_file:
            config_file.write(json.dumps(self.config, indent=4))

    def _get_zmq_keys(self, id):
        cert_path = os.path.join(self.work_dir, 'certificates')
        public_keys = os.path.join(cert_path, 'public_keys')
        private_keys = os.path.join(cert_path, 'private_keys')
        public_key_path = os.path.join(public_keys, '{0}.pub'.format(id))
        private_key_path = os.path.join(private_keys, '{0}.pri'.format(id))

        if not os.path.isfile(public_key_path) or not os.path.isfile(private_key_path):
            logging.debug('Generating ZMQ keys for: {0}.'.format(id))
            for _path in [cert_path, public_keys, private_keys]:
                if not os.path.isdir(_path):
                    os.mkdir(_path)

            tmp_key_dir = tempfile.mkdtemp()
            try:
                public_key, private_key = create_certificates(tmp_key_dir, id)
                # the final location for keys
                shutil.move(public_key, public_key_path)
                shutil.move(private_key, private_key_path)
            finally:
                shutil.rmtree(tmp_key_dir)

        # return copy of keys
        return open(private_key_path, "r").readlines(), open(public_key_path, "r").readlines()

    def _remove_zmq_keys(self, id):
        cert_path = os.path.join(self.work_dir, 'certificates')
        public_keys = os.path.join(cert_path, 'public_keys')
        private_keys = os.path.join(cert_path, 'private_keys')
        public_key_path = os.path.join(public_keys, '{0}.pub'.format(id))
        private_key_path = os.path.join(private_keys, '{0}.pri'.format(id))

        for _file in [public_key_path, private_key_path]:
            if os.path.isfile(_file):
                os.remove(_file)

    def _handle_command_delete_drone(self, data):
        drone_id = data
        logger.debug('Deleting drone: {0}'.format(drone_id))
        db_session = database_setup.get_session()
        drone_to_delete = db_session.query(Drone).filter(Drone.id == drone_id).first()
        if drone_to_delete:
            db_session.delete(drone_to_delete)
            db_session.commit()
            # tell the drone to kill itself
            self.drone_command_receiver.send('{0} {1} '.format(drone_id, Messages.DRONE_DELETE.value))
            self._remove_zmq_keys(drone_id)
            self._reconfigure_all_clients()

    def _handle_command_add_drone(self):
        db_session = database_setup.get_session()
        drone = Drone()
        db_session.add(drone)
        db_session.commit()
        logger.debug('New drone has been added with id: {0}'.format(drone.id))

        drone_config = self._get_drone_config(drone.id)
        self.config_commands.send('{0} {1}'.format(Messages.OK.value, json.dumps(drone_config)))


