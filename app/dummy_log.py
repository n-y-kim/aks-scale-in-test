import logging
import time
import signal
import sys

from node import Node
from pdb import Pdb

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s|%(levelname)s] - %(message)s')
handler.setFormatter(formatter) 

logger.addHandler(handler)

# Write log with level INFO, with time and messsage

def signal_handler(sig, frame):
    global sigterm_received
    logging.info('Received SIGTERM. Changing sigterm_received to True.')
    sigterm_received = True

def main():
    global sigterm_received
    logger.info("Logging app running...")
    while True:
        
        node = Node()
        my_node_name = node.get_node_name()
        my_node_status = node.get_node_status(my_node_name)
        my_node_taint = node.get_node_taint(my_node_name)
        
        logger.info("Running on node: %s" % my_node_name)
        logger.info("Node status: %s" % my_node_status)
        
        if sigterm_received or my_node_taint or my_node_status == 'NotReady':
            
            logger.info("=====================================")
            logger.info('SIGTERM received: %s' % sigterm_received)
            logger.info('Node taint: %s' % my_node_taint)

            for _ in range(36):
                logger.info("Sleeping for 5 second...")
                time.sleep(5)
                logger.info("Woke up after 5 second.")
            
            logger.info("Script finished.")
            logger.info("=====================================")
            # logger.info("Changing PDB for scale-in operation.")
            
            # pdb = Pdb()
            # pdb.patch_pdb()
            
            # logger.info("Changed minimum available pods to 0.")
            logger.info("Exiting....")
            sigterm_received = True
            exit(0)
        else:
            logging.info("Node is in Ready state. No Scale-in activated.")
            pass
        time.sleep(2)

if __name__ == '__main__':
    sigterm_received = False
    signal.signal(signal.SIGTERM, signal_handler)
    main()