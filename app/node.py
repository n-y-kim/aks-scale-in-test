from kubernetes import client, config

class Node:
    def __init__(self):
        config.load_incluster_config()
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

        return node_ready_status
    
    def get_node_name(self):
        # Get current namespace
        namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
        
        # Get the current pod name
        pod_name = open("/etc/hostname").read().strip()
        pod = self.api.read_namespaced_pod(pod_name, namespace)
        
        # Get the node name
        node_name = pod.spec.node_name
        
        return node_name
    
    def get_node_taint(self, node_name):
        # Get the node's taints
        node_taints = self.api.read_node(node_name).spec.taints
        
        # If node_taints is None, return False
        if node_taints is None:
            return ""
        
        # If there is a taint with key 'ToBeDeletedByClusterAutoscaler' and effect 'NoSchedule', return True
        for taint in node_taints:
            if (taint.key == 'ToBeDeletedByClusterAutoscaler' and taint.effect == 'NoSchedule') or (taint.key == 'DeletionCandidateOfClusterAutoscaler' and taint.effect == 'PreferNoSchedule'):
                return taint.key
        
        return ""