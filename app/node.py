from kubernetes import client, config
import logging

class Node:
    def __init__(self):
        self.api = client.CoreV1Api()

    def get_node_status(self, node_name):
        # Get the node's status
        node_status = self.api.read_node_status(node_name)

        # Find the 'Ready' condition
        ready_condition = next((condition for condition in node_status.status.conditions if condition.type == 'Ready'), None)

        # Check if the 'Ready' condition was found and if its status is 'True'
        if ready_condition and ready_condition.status == 'True':
            node_ready_status = 'Ready'
        else:
            node_ready_status = 'NotReady'

        # Log the node's ready status as INFO
        logging.info('Found node %s status: %s' % (node_name, node_ready_status))

        return node_ready_status
    
    def get_node_name(self):
        # Load the in-cluster config
        config.load_incluster_config()

        # Get current namespace
        namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
        
        # Get the current pod name
        pod_name = open("/etc/hostname").read().strip()
        pod = self.api.read_namespaced_pod(pod_name, namespace)
        
        # Get the node name
        node_name = pod.spec.node_name
        
        # Log the node name as INFO
        logging.info('Found node name: %s' % node_name)
        
        return node_name