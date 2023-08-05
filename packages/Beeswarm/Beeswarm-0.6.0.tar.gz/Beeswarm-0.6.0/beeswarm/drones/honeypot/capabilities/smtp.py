# Copyright (C) 2013 Aniket Panse <contact@aniketpanse.in>
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

# Parts of this code are from secure-smtpd (https://github.com/bcoe/secure-smtpd)

import base64
import logging
import time
import random
import smtpd
import asyncore
import asynchat
import mailbox
from smtpd import NEWLINE, EMPTYSTRING

from beeswarm.drones.honeypot.capabilities.handlerbase import HandlerBase


class SMTPChannel(smtpd.SMTPChannel):
    def __init__(self, smtp_server, newsocket, fromaddr,
                 smtp_map=None, session=None, opts=None):
        self.options = opts
        # A sad hack because SMTPChannel doesn't
        # allow custom banners, and sends it's own through its
        # __init__() method. When the initflag is False,
        # the push() method is effectively disabled, so the 
        # superclass banner is not sent.
        self._initflag = False
        self.banner = self.options['protocol_specific_data']['banner']

        # States
        self.login_pass_authenticating = False
        self.login_uname_authenticating = False
        self.plain_authenticating = False
        self.cram_authenticating = False
        self.authenticated = False

        self.username = None
        self.password = None
        self.digest = None

        self.sent_cram_challenge = None
        self.session = session
        self.options = opts

        smtpd.SMTPChannel.__init__(self, smtp_server, newsocket, fromaddr)
        asynchat.async_chat.__init__(self, newsocket, map=smtp_map)

        # Now we set the initflag, so that push() will work again.
        # And we push.
        self._initflag = True
        self.push("220 %s" % self.banner)

    def push(self, msg):
        # Only send data after superclass initialization
        if self._initflag:
            transmit_msg = msg + '\r\n'
            self.session.transcript_outgoing(transmit_msg)
            asynchat.async_chat.push(self, transmit_msg)

    def close_quit(self):
        self.close_when_done()
        self.handle_close()

    def smtp_QUIT(self, arg):
        self.push('221 Bye')
        self.close_when_done()
        self.close_quit()

    def collect_incoming_data(self, data):
        self.session.transcript_incoming(data + self.terminator)
        self.__line.append(data)

    def smtp_EHLO(self, arg):
        if not arg:
            self.push('501 Syntax: HELO/EHLO hostname')
            return
        if self.__greeting:
            self.push('503 Duplicate HELO/EHLO')
        else:
            self.push('250-%s Hello %s' % (self.banner, arg))
            self.push('250-AUTH PLAIN LOGIN CRAM-MD5')
            self.push('250 EHLO')

    def smtp_AUTH(self, arg):

        if (self.plain_authenticating and self.login_pass_authenticating and
                self.cram_authenticating):
            self.push('503 Bad sequence of commands')
            self.close_quit()

        if self.cram_authenticating:
            self.cram_authenticating = False
            cred = base64.b64decode(arg)
            self.username, self.digest = cred.split()
            if self.sent_cram_challenge is None:
                self.push('451 Internal confusion')
                return
            authbool = self.session.try_auth('cram_md5', username=self.username, digest=self.digest,
                                             challenge=self.sent_cram_challenge)
            if authbool:
                self.push('235 Authentication Successful')
                self.authenticated = True
                return
            else:
                self.push('535 authentication failed')
                self.close_quit()

        elif self.login_uname_authenticating:
            self.login_uname_authenticating = False
            self.username = base64.b64decode(arg)
            self.push('334 ' + base64.b64encode('Password:'))
            self.login_pass_authenticating = True
            return

        elif self.login_pass_authenticating:
            self.login_pass_authenticating = False
            self.password = base64.b64decode(arg)
            authbool = self.session.try_auth('plaintext', username=self.username, password=self.password)

            if authbool:
                self.push('235 Authentication Successful')
                self.authenticated = True
                return
            else:
                self.push('535 authentication failed')
                self.close_quit()

            self.push('535 authentication failed')
            self.close_quit()

        elif self.plain_authenticating:
            self.plain_authenticating = False
            # Our arg will ideally be the username/password
            _, self.username, self.password = base64.b64decode(arg).split('\x00')
            authbool = self.session.try_auth('plaintext', username=self.username, password=self.password)
            if authbool:
                self.push('235 Authentication Successful')
                self.authenticated = True
                return
            else:
                self.push('535 authentication failed')
                self.close_quit()

        elif 'PLAIN' in arg:
            self.plain_authenticating = True
            try:
                _, param = arg.split()
            except ValueError:
                # We need to get the credentials now since client has not sent
                # them. The space after the 334 is important as said in the RFC
                self.push("334 ")
                return
            _, self.username, self.password = base64.b64decode(param).split('\x00')
            authbool = self.session.try_auth('plaintext', username=self.username, password=self.password)
            if authbool:
                self.push('235 Authentication Successful')
                self.authenticated = True
                return
            else:
                self.push('535 authentication failed')
                self.close_quit()

        elif 'LOGIN' in arg:
            param = arg.split()
            if len(param) > 1:
                self.username = base64.b64decode(param[1])
                self.push('334 ' + base64.b64encode('Password:'))
                self.login_pass_authenticating = True
                return
            else:
                self.push('334 ' + base64.b64encode('Username:'))
                self.login_uname_authenticating = True
                return

        elif 'CRAM-MD5' in arg:
            self.cram_authenticating = True
            r = random.randint(5000, 20000)
            t = int(time.time())

            # challenge is of the form '<24609.1047914046@awesome.host.com>'
            self.sent_cram_challenge = "<" + str(r) + "." + str(t) + "@" + self.__fqdn + ">"
            self.push("334 " + base64.b64encode(self.sent_cram_challenge))
            return

    # This code is taken directly from the underlying smtpd.SMTPChannel
    # support for AUTH is added.
    def found_terminator(self):
        line = EMPTYSTRING.join(self.__line)

        if self.debug:
            self.logger.info('found_terminator(): data: %s' % repr(line))

        self.__line = []
        if self.__state == self.COMMAND:
            if not line:
                self.push('500 Error: bad syntax')
                return
            method = None
            i = line.find(' ')

            if (self.login_uname_authenticating or
                    self.login_pass_authenticating or
                    self.plain_authenticating or
                    self.cram_authenticating):
                # If we are in an authenticating state, call the
                # method smtp_AUTH.
                arg = line.strip()
                command = 'AUTH'
            elif i < 0:
                command = line.upper()
                arg = None
            else:
                command = line[:i].upper()
                arg = line[i + 1:].strip()

            # White list of operations that are allowed prior to AUTH.
            if not command in ['AUTH', 'EHLO', 'HELO', 'NOOP', 'RSET', 'QUIT']:
                if not self.authenticated:
                    self.push('530 Authentication required')
                    self.close_quit()
                    return

            method = getattr(self, 'smtp_' + command, None)
            if not method:
                self.push('502 Error: command "%s" not implemented' % command)
                return
            method(arg)
            return
        else:
            if self.__state != self.DATA:
                self.push('451 Internal confusion')
                return
                # Remove extraneous carriage returns and de-transparency according
            # to RFC 821, Section 4.5.2.
            data = []
            for text in line.split('\r\n'):
                if text and text[0] == '.':
                    data.append(text[1:])
                else:
                    data.append(text)
            self.__data = NEWLINE.join(data)
            status = self.__server.process_message(
                self.__peer,
                self.__mailfrom,
                self.__rcpttos,
                self.__data
            )
            self.__rcpttos = []
            self.__mailfrom = None
            self.__state = self.COMMAND
            self.set_terminator('\r\n')
            if not status:
                self.push('250 Ok')
            else:
                self.push(status)


class DummySMTPServer(object):
    def __init__(self, mail_vfs):
        self.mail_vfs = mail_vfs
        self.mboxpath = self.mail_vfs.getsyspath('mailbox')

    def process_message(self, peer, mailfrom, rcpttos, data):
        logging.info('Got new mail, peer ({}), from ({}), to ({})'.format(peer, mailfrom, rcpttos))
        if self.mboxpath is not None:
            mbox = mailbox.mbox(self.mboxpath, create=True)
            mbox.add(data)


class smtp(HandlerBase):
    def __init__(self, sessions, options, work_dir):
        super(smtp, self).__init__(sessions, options, work_dir)
        self._options = options

    def handle_session(self, gsocket, address):
        session_ = self.create_session(address)
        local_map = {}
        server = DummySMTPServer(self.vfsystem.opendir('/var/mail'))
        SMTPChannel(server, gsocket, address, session=session_,
                    smtp_map=local_map, opts=self._options)
        try:
            asyncore.loop(map=local_map)
        except Exception:
            # im sooooo evil!
            pass
        finally:
            session_.connected = False
