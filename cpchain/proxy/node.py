# pylint: disable=wrong-import-position
import logging
import os
import asyncio

if __name__ == '__main__':
    from twisted.internet import asyncioreactor
    loop = asyncio.get_event_loop()
    asyncioreactor.install(eventloop=loop)
else:
    loop = asyncio.get_event_loop()

from twisted.internet import reactor, ssl, defer
from twisted.web.server import Site
from twisted.internet.task import LoopingCall

from kademlia.network import Server

from cpchain import config
from cpchain.proxy.network import PeerProtocol
from cpchain.proxy.server import SSLServerFactory, FileServer
from cpchain.proxy.client import start_client
from cpchain.utils import join_with_rc, join_with_root

logger = logging.getLogger(__name__)


class KadServer(Server):
    def listen(self, port, interface='0.0.0.0'):
        """
        Start listening on the given port.

        Provide interface="::" to accept ipv6 address
        """
        loop = asyncio.get_event_loop()
        listen = loop.create_datagram_endpoint(self._create_protocol,
                                               local_addr=(interface, port))
        logger.info("Node %i listening on %s:%i",
                    self.node.long_id, interface, port)

        d = defer.Deferred()

        def create_endpoint_done(future):
            self.transport, self.protocol = future.result() # pylint: disable=attribute-defined-outside-init
            self.refresh_table()
            d.callback(True)

        future = asyncio.ensure_future(listen)
        future.add_done_callback(create_endpoint_done)

        return d


def get_eth_addr():
    return b'fake_eth_addr'

class Peer:
    def __init__(self):
        self.service_port = None
        self.eth_addr = None
        self.ip = None

    def start_service(self, ctrl_port=None, data_port=None):

        self.eth_addr = get_eth_addr()

        server_key = os.path.expanduser(
            join_with_rc(config.proxy.server_key))
        server_crt = os.path.expanduser(
            join_with_rc(config.proxy.server_crt))

        if not os.path.isfile(server_key):
            logger.info("SSL key/cert file not found, "
                        + "run local self-test by default")
            server_key_sample = 'cpchain/assets/proxy/key/server.key'
            server_crt_sample = 'cpchain/assets/proxy/key/server.crt'
            server_key = join_with_root(server_key_sample)
            server_crt = join_with_root(server_crt_sample)

        # ctrl channel
        ctrl_port = (ctrl_port or config.proxy.server_ctrl_port)
        ctrl_factory = SSLServerFactory()
        reactor.listenSSL(ctrl_port, ctrl_factory,
                          ssl.DefaultOpenSSLContextFactory(
                              server_key, server_crt))

        self.service_port = ctrl_port

        # data channel
        data_port = (data_port or config.proxy.server_data_port)
        file_factory = Site(FileServer())
        reactor.listenSSL(data_port, file_factory,
                          ssl.DefaultOpenSSLContextFactory(
                              server_key, server_crt))

        ctrl_factory.data_port = data_port

        def set_external_ip():
            if self.ip is None:
                # waiting for node bootstrap finish
                reactor.callLater(1, set_external_ip)

            ctrl_factory.ip = self.ip

        set_external_ip()

    def join_centra_net(self, port=None, boot_node=None):

        if boot_node and not self.service_port:
            logger.error("proxy service not started")
            return

        port = port or config.proxy.server_peer_port
        protocol = PeerProtocol()
        reactor.listenUDP(port, protocol)

        def refresh():
            protocol.refresh_peers()

        if boot_node:
            protocol.peer_id = self.eth_addr
            protocol.peer_info = self.service_port
            protocol.bootstrap(boot_node)
        else:
            LoopingCall(refresh).start(5)

    def join_decentra_net(self, port=None, boot_nodes=None):

        if boot_nodes and not self.service_port:
            logger.error("proxy service not started")
            return

        port = (port or config.proxy.server_dht_port)

        peer = KadServer()

        if boot_nodes:

            d = defer.Deferred()

            def set_key_done(_):
                d.callback(True)

            def stun_done(future):
                addr = future.result()
                self.ip = addr[1][0]
                addr = '%s,%d' % (self.ip, self.service_port)
                asyncio.ensure_future(
                    peer.set(
                        self.eth_addr,
                        addr
                        )
                    ).add_done_callback(set_key_done)

            def bootstrap_done(_):
                asyncio.ensure_future(
                    peer.protocol.stun(
                        boot_nodes[0]
                        )
                    ).add_done_callback(stun_done)

            def listen_done(_):
                asyncio.ensure_future(
                    peer.bootstrap(
                        boot_nodes
                        )
                    ).add_done_callback(bootstrap_done)

            peer.listen(port).addCallback(listen_done)

            return d

        return peer.listen(port)


    def pick_peer(self, boot_node, port=None):
        port = port or 8150
        protocol = PeerProtocol()
        reactor.listenUDP(port, protocol)

        def pick_peer_done(result):
            protocol.transport.stopListening()
            success, data = result
            if success and data:
                return tuple(data)

        d = protocol.pick_peer(boot_node)
        d.addBoth(pick_peer_done)
        return d

    def get_peer(self, eth_addr, boot_nodes, port=None):

        if isinstance(boot_nodes, tuple):
            port = port or 8150
            protocol = PeerProtocol()
            reactor.listenUDP(port, protocol)

            def get_peer_done(result):
                protocol.transport.stopListening()
                success, data = result
                if success and data:
                    return tuple(data)

            d = protocol.get_peer(eth_addr, boot_nodes)
            d.addBoth(get_peer_done)
            return d

        elif isinstance(boot_nodes, list):
            port = port or 8250

            peer = KadServer()

            d = defer.Deferred()

            def get_key_done(future):
                value = future.result()
                peer.stop()
                d.callback(tuple(value.split(',')))

            def bootstrap_done(_):
                asyncio.ensure_future(
                    peer.get(eth_addr)
                    ).add_done_callback(get_key_done)

            def listen_done(_):
                asyncio.ensure_future(
                    peer.bootstrap(
                        boot_nodes
                        )
                    ).add_done_callback(bootstrap_done)

            peer.listen(port).addCallback(listen_done)

            return d

        else:
            logger.error("wrong boot nodes")


def start_proxy_request(sign_message, boot_node, proxy_id=None):

    d = defer.Deferred()

    def start_client_done(proxy_reply):
        d.callback(proxy_reply)

    def get_proxy_done(addr):
        start_client(sign_message, addr).addCallback(start_client_done)

    def get_proxy(boot_node, proxy_id=None):
        if proxy_id is None:
            # pick a proxy from tracker
            return Peer().pick_peer(
                boot_node=boot_node
                )

        # find the (ip, port) for given proxy
        return Peer().get_peer(
            eth_addr=proxy_id,
            boot_nodes=boot_node
        )

    get_proxy(boot_node, proxy_id).addCallback(get_proxy_done)

    return d


# Code below for testing purpose only, pls. ignore.
# Will be removed in formal release.
if __name__ == '__main__':
    import sys

    from twisted.python import log as twisted_log # pylint: disable=ungrouped-imports
    twisted_log.startLogging(sys.stdout)

    if sys.argv[1] == 'tracker':
        peer = Peer()
        peer.join_centra_net(port=8101)
        peer.join_decentra_net(port=8201)

    elif sys.argv[1] == 'peer':
        peer = Peer()
        peer.start_service()
        peer.join_centra_net(
            boot_node=('127.0.0.1', 8101)
            )

        peer.join_decentra_net(
            boot_nodes=[('127.0.0.1', 8201)]
            )

    elif sys.argv[1] == 'pick_peer':
        def found_peer(peer):
            logger.debug(peer)
            reactor.stop()

        peer = Peer()
        peer.pick_peer(
            boot_node=('127.0.0.1', 8101)
            ).addCallback(found_peer)

    elif sys.argv[1] == 'get_peer':
        peer = Peer()

        count = 0
        def got_peer(peer):
            global count  # pylint: disable=global-statement
            logger.debug(peer)
            count += 1
            if count == 2:
                reactor.stop()

        peer.get_peer(
            eth_addr=b'fake_eth_addr',
            boot_nodes=('127.0.0.1', 8101)
            ).addCallback(got_peer)

        peer.get_peer(
            eth_addr=b'fake_eth_addr',
            boot_nodes=[('127.0.0.1', 8201)]
            ).addCallback(got_peer)

    elif sys.argv[1] == 'service':
        peer = Peer()
        peer.start_service()

    reactor.run()
