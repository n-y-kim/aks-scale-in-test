import logging
import time
import signal
import sys

from node import Node
from pdb import Pdb
from deployment import Deployment

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s|%(levelname)s] - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

CANDIDATE_TAINT = "DeletionCandidateOfClusterAutoscaler"
FINAL_TAINT = "ToBeDeletedByClusterAutoscaler"
NO_SCALE_DOWN_ANNOTATION = "cluster-autoscaler.kubernetes.io/scale-down-disabled"

# Write log with level INFO, with time and messsage

def signal_handler(sig, frame):
    global sigterm_received
    logging.info('Received SIGTERM. Changing sigterm_received to True.')
    sigterm_received = True

def run_script(node, my_node_name): #180s
    for _ in range(36):
        logger.info("Sleeping for 5 second...")
        logger.info("Set this node as the candidate with API just in case the taint gets removed after the scan interval.")
        
        node.add_taint(my_node_name, CANDIDATE_TAINT, "PreferNoSchedule")
        time.sleep(5)
        
        logger.info("Woke up after 5 second.")
        logger.info("=====================================")

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
        
        # If the node is candidate for deletion, create shield pod to prevent scale-in
        if my_node_taint == CANDIDATE_TAINT:
            logger.info("Node is candidate for deletion. Creating shield pod...")
            
            deploy = Deployment()
            
            if deploy.check_other_deployments():
                logger.info("There are other shield deployments. This node is not the final candidate for deletion.")
                
                add_annotation = node.add_annotation(my_node_name, NO_SCALE_DOWN_ANNOTATION, "true")
                
                logger.info("Adding annotation result: %s" % add_annotation)
                logger.info("Exiting...")
                
                exit(0)
            else:
                response = deploy.create_deployment("default", "shield_app.yaml", my_node_name)
                # Print create success response
                logger.info("Shield pod created with name: %s" % response)
        
            run_script(node, my_node_name)
            
            # Delete annotations in another nodes
            nodes = node.get_nodes_with_annotation(NO_SCALE_DOWN_ANNOTATION)
            nodes.update_annotations(NO_SCALE_DOWN_ANNOTATION, "false")
            
            node.add_taint(my_node_name, CANDIDATE_TAINT, "PreferNoSchedule")
            
            # Delete shield deployment
            response = deploy.delete_deployment("default", "shield-deployment-" + my_node_name)
            logger.info("Shield pod deleted with name: %s" % response)
            
            # Make this node as the final candidate for deletion
            logger.info("Making this node as the final candidate for deletion...")
            
            taint_added_result = node.add_taint(my_node_name, "ToBeDeletedByClusterAutoscaler", "NoSchedule")
            
            logger.info("Taint added result: %s" % taint_added_result)
            
            exit(0)
            
        
        # if sigterm_received or my_node_taint=="ToBeDeletedByClusterAutoscaler" or my_node_status == 'NotReady':
            
        #     logger.info("Node is candidate for deletion. Creating shield pod...")
            
        #     deploy = Deployment()
        #     if deploy.have_deployment("default", "shield-deployment-" + my_node_name):
        #         logger.info("Shield pod already exists. No need to create.")
        #         pass
        #     else: 
        #         response = deploy.create_deployment("default", "shield_app.yaml", my_node_name)
        #         # Print create success response
        #         logger.info("Shield pod created with name: %s" % response)
            
        #     logger.info("=====================================")
        #     logger.info('SIGTERM received: %s' % sigterm_received)
        #     logger.info('Node taint: %s' % my_node_taint)

        #     logger.info("Deleting deployment to scale-in.")
            
        #     if deploy.delete_deployment("default", "shield-deployment-" + my_node_name):
        #         logger.info("Deleted deployment")
        #     else:
        #         logger.info("Deployment does not exist. No need to delete.")
        #     logger.info("Exiting....")
        #     sigterm_received = True
        #     exit(0)
        # else:
        #     logging.info("Node is in Ready state. No Scale-in activated.")
        #     pass
        time.sleep(2)

if __name__ == '__main__':
    sigterm_received = False
    signal.signal(signal.SIGTERM, signal_handler)
    main()