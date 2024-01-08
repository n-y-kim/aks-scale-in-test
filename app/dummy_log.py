import logging
import time

from node import Node
from pdb import Pdb

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setLevel(logging.INFO)

logger.addHandler(handler)

# Write log with level INFO, with time and message per 5seconds
# If my node's status is in 'NotReady', write log with "Not Ready detected." and run script from script/change_pdb.sh

def main():
    logger.info("Logging app running...")
    while True:
        
        node = Node()
        my_node_name = node.get_node_name()
        my_node_status = node.get_node_status(my_node_name)
        my_node_taint = node.get_node_taint(my_node_name)
        
        if my_node_taint or my_node_status == 'NotReady':
            logger.info("Not Ready detected OR Tainted to be deleted.")
            logger.info("Running custom script that will need 3 minutes to finish.")
            time.sleep(180)
            logger.info("Script finished.")
            logger.info("=====================================")
            logger.info("Changing PDB for scale-in operation.")
            
            pdb = Pdb()
            pdb.patch_pdb()
            
            logger.info("Changed minimum available pods to 0.")
            logger.info("Exiting....")
            exit(0)
        else:
            logging.info("Node is in Ready state. No Scale-in activated.")
            pass
        time.sleep(2)

if __name__ == '__main__':
    main()