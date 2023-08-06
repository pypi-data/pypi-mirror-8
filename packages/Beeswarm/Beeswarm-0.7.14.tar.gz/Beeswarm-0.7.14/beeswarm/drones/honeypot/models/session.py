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

import hmac
import logging
import json
from datetime import datetime

from beeswarm.shared.models.base_session import BaseSession
from beeswarm.shared.misc.rfbes import RFBDes
from beeswarm.shared.message_enum import Messages

logger = logging.getLogger(__name__)


class Session(BaseSession):
    authenticator = None
    default_timeout = 25
    honeypot_id = None

    def __init__(self, source_ip, source_port, protocol, users, destination_port=None, destination_ip=None):

        super(Session, self).__init__(protocol, source_ip, source_port, destination_ip, destination_port)

        self.connected = True
        self.authenticated = False
        self.honeypot_id = Session.honeypot_id
        self.users = users

        # for session specific volatile data (will not get logged)
        self.vdata = {}
        self.last_activity = datetime.utcnow()

        self.send_log(Messages.SESSION_PART_HONEYPOT_SESSION_START.value, self.to_dict())

    def activity(self):
        self.last_activity = datetime.utcnow()

    def is_connected(self):
        return self.connected

    def try_auth(self, _type, **kwargs):
        authenticated = False
        if _type == 'plaintext':
            if kwargs.get('username') in self.users:
                if self.users[kwargs.get('username')] == kwargs.get('password'):
                    authenticated = True

        elif _type == 'cram_md5':
            def encode_cram_md5(challenge, user, password):
                response = user + ' ' + hmac.HMAC(password, challenge).hexdigest()
                return response

            if kwargs.get('username') in self.users:
                uname = kwargs.get('username')
                digest = kwargs.get('digest')
                s_pass = self.users[uname]
                challenge = kwargs.get('challenge')
                ideal_response = encode_cram_md5(challenge, uname, s_pass)
                _, ideal_digest = ideal_response.split()
                if ideal_digest == digest:
                    authenticated = True
        elif _type == 'des_challenge':
            challenge = kwargs.get('challenge')
            response = kwargs.get('response')
            for valid_password in self.users.values():
                aligned_password = (valid_password + '\0' * 8)[:8]
                des = RFBDes(aligned_password)
                expected_response = des.encrypt(challenge)
                if response == expected_response:
                    authenticated = True
                    kwargs['password'] = aligned_password
                    break
        else:
            assert False

        if authenticated:
            self.authenticated = True
            self.add_auth_attempt(_type, True, **kwargs)
        else:
            self.add_auth_attempt(_type, False, **kwargs)

        if _type == 'des_challenge':
            kwargs['challenge'] = kwargs.get('challenge').encode('hex')
            kwargs['response'] = kwargs.get('response').encode('hex')

        self.send_log(Messages.SESSION_PART_HONEYPOT_AUTH.value, self.login_attempts[-1])
        logger.debug('{0} authentication attempt from {1}:{2}. Credentials: {3}'.format(self.protocol, self.source_ip,
                                                                                        self.source_port,
                                                                                        json.dumps(kwargs)))
        return authenticated

    def end_session(self):
        super(Session, self).end_session(Messages.SESSION_HONEYPOT.value)

