import sys
import logging

from cpchain.utils import reactor
from cpchain.proxy.node import Peer

logger = logging.getLogger(__name__)

if len(sys.argv) == 1:
    logger.info("Usage: python3 first_node.py <tracker_port> <dht_port>")
    logger.info("example: python3 first_node.py 8101 8201")
    logger.info("not port specified, use default port 8100 and 8200")
    peer = Peer()
    peer.join_centra_net()
    peer.join_decentra_net()

elif len(sys.argv) == 3:
    peer = Peer()
    peer.join_centra_net(port=int(sys.argv[1]))
    peer.join_decentra_net(port=int(sys.argv[2]))

else:
    logger.info("Usage: python3 first_node.py <tracker_port> <dht_port>")
    sys.exit(1)

reactor.run()