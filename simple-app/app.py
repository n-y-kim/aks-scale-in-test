import time

from loggingconfig.logs import logger
from k8s.node import Node
from k8s.deployment import Deployment

# If the node's taint is the candidate taint, set priorityClassName to system-node-critical
def main():
    node = Node()
    node_name = node.get_node_name()
    
    start_time = time.time()
    
    while True:
        if node.get_node_taint(node_name) == 'DeletionCandidateOfClusterAutoscaler':
            
            logger.info("DeletionCandidateOfClusterAutoscaler taint found. Setting priorityClassName to system-node-critical.")
            
            deployment = Deployment('default')
            deployment_name = node_name + '-log-agent'
            deployment.add_priority_class(deployment_name)
            
            # Sleep for 10 minutes with while loop printing log every 5 seconds
            for _ in range(120):
                logger.info("Sleeping for 5 second...")
                time.sleep(5)
                logger.info("Woke up after 5 second.")
                logger.info("=====================================")
            
            deployment.delete_deployment(deployment_name)
            
            # Exit the app
            exit()
        
        else:
            logger.info("Node: %s", node.get_node_name())
            # Show how much time passed since the first log
            logger.info("Time passed: %s seconds" % (time.time() - start_time))
            time.sleep(3)

if __name__ == '__main__':
    main()