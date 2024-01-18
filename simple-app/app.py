import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='[%(asctime)s|%(levelname)s] - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

from k8s.node import Node
from k8s.deployment import Deployment

# If the node's taint is the candidate taint, set priorityClassName to system-node-critical
def main():
    node = Node()
    
    start_time = time.time()
    
    while True:
        if node.get_node_taint(node.get_node_name()) == 'DeletionCandidateOfClusterAutoscaler':
            
            logger.info("DeletionCandidateOfClusterAutoscaler taint found. Setting priorityClassName to system-node-critical.")
            
            deployment = Deployment()
            deployment.add_priority_class('default', 'log-agent')
            
            # Sleep for 10 minutes with while loop printing log every 5 seconds
            for _ in range(120):
                logger.info("Sleeping for 5 second...")
                time.sleep(5)
                logger.info("Woke up after 5 second.")
                logger.info("=====================================")
            
            deployment.delete_deployment('default', 'log-agent')
            
            # Exit the app
            exit()
        
        else:
            logger.info("Node: %s", node.get_node_name())
            # Show how much time passed since the first log
            logger.info("Time passed: %s seconds" % (time.time() - start_time))
            time.sleep(3)

if __name__ == '__main__':
    main()