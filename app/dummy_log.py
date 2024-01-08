import logging
import time
import os

import node

logger = logging.getLogger(__name__)

# Write log with level INFO, with time and message per 5seconds
# If my node's status is in 'NotReady', write log with "Not Ready detected." and run script from script/change_pdb.sh

def main():
    while True:
        logger.info("Hello World!")
        my_node_name = node.get_node_name()
        my_node_status = node.get_node_status(my_node_name)
        if my_node_status == 'NotReady':
            logger.info("Not Ready detected.")
            logger.info("Running script to change PDB for scale-in operation.")
            os.system("script/change_pdb.sh")
            logger.info("Script finished.")
            logger.info("Exiting....")
            exit(0)
        else:
            pass
        time.sleep(2)

if __name__ == '__main__':
    main()