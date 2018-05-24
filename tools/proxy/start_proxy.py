import sys
import logging

from twisted.python import log

from cpchain.utils import reactor
from cpchain.proxy.node import Peer

logger = logging.getLogger(__name__)

if len(sys.argv) != 3:
    logger.info("Usage: python3 start_proxy.py <tracker ip:port> <dht ip:port>")
    logger.info("example: python3 start_proxy.py 127.0.0.1:8101 127.0.0.1:8201")
    sys.exit(1)

log.startLogging(sys.stdout)

(addr, port) = sys.argv[1].split(':')
tracker = (str(addr), int(port))

peer = Peer()
peer.start_service()
peer.join_centra_net(
    tracker=tracker
    )

(addr, port) = sys.argv[2].split(':')
boot_nodes = [(str(addr), int(port))]

boot_nodes = [('127.0.0.1', 8201)]
peer.join_decentra_net(
    boot_nodes=boot_nodes
    )

reactor.run()