from pyroute2.netlink import Marshal
from pyroute2.netlink import NLM_F_DUMP
from pyroute2.netlink import NLM_F_REQUEST
from pyroute2.netlink.generic import ctrlmsg
from pyroute2.netlink.generic import NETLINK_GENERIC
from pyroute2.netlink.generic import GENL_ID_CTRL
from pyroute2.netlink.generic import CTRL_CMD_GETFAMILY
from pyroute2.iocore.iocore import IOCore


class Netlink(IOCore):
    '''
    Main netlink messaging class. It automatically spawns threads
    to monitor network and netlink I/O, creates and destroys message
    queues.

    By default, netlink class connects to the local netlink socket
    on startup. If you prefer to connect to another host, use::

        nl = Netlink(host='tcp://remote.host:7000')

    It is possible to connect to uplinks after the startup::

        nl = Netlink(do_connect=False)
        nl.connect('tcp://remote.host:7000')

    To act as a server, call serve()::

        nl = Netlink()
        nl.serve('unix:///tmp/pyroute')
    '''
    family = NETLINK_GENERIC
    groups = 0
    marshal = Marshal
    name = 'Netlink API'

    def __init__(self, debug=False, timeout=3, do_connect=True,
                 host=None, key=None, cert=None, ca=None, addr=None,
                 fork=False, pid=None):
        self.default_target = '/%i/%i' % (self.family, self.groups)
        host = host or 'netlink://'
        host = '%s%s' % (host, self.default_target)
        IOCore.__init__(self, debug, timeout, do_connect,
                        host, key, cert, ca, addr, fork,
                        pid=pid)

    def nlm_request(self, msg, msg_type,
                    msg_flags=NLM_F_DUMP | NLM_F_REQUEST,
                    terminate=None, response_timeout=None):
        '''
        Send netlink request, filling common message
        fields, and wait for response.
        '''
        nonce = self.nonce.alloc()
        msg['header']['sequence_number'] = nonce
        msg['header']['type'] = msg_type
        msg['header']['flags'] = msg_flags
        msg.encode()

        result = self.request(msg.buf.getvalue(),
                              addr=self.default_peer,
                              nonce=nonce,
                              nonce_pool=self.nonce,
                              terminate=terminate,
                              response_timeout=response_timeout)

        for msg in result:
            # reset message buffer, make it ready for encoding back
            msg.reset()
            if not self.debug:
                del msg['header']

        return result


class GenericNetlink(Netlink):

    def __init__(self, proto, msg_class, pid=None):
        Netlink.__init__(self, pid=pid)
        self.marshal.msg_map[GENL_ID_CTRL] = ctrlmsg
        self.prid = self.get_protocol_id(proto)
        self.marshal.msg_map[self.prid] = msg_class

    def get_protocol_id(self, prid):
        msg = ctrlmsg()
        msg['cmd'] = CTRL_CMD_GETFAMILY
        msg['version'] = 1
        msg['attrs'].append(['CTRL_ATTR_FAMILY_NAME', prid])
        response = self.nlm_request(msg, GENL_ID_CTRL,
                                    msg_flags=NLM_F_REQUEST)[0]
        prid = [i[1] for i in response['attrs']
                if i[0] == 'CTRL_ATTR_FAMILY_ID'][0]
        return prid
