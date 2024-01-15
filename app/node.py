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
    
    def add_taint(self, node_name, taint_key, taint_effect):
        # Add taint to node using patch kubernetes api
        node = self.api.read_node(node_name)
        
        # Create new taint
        new_taint = client.V1Taint(effect=taint_effect, key=taint_key, value='true')
        
        # If the node already has taints, check if the new taint already exists
        if node.spec.taints is not None:
            for taint in node.spec.taints:
                if taint.key == taint_key and taint.effect == taint_effect:
                    # The taint already exists, so return
                    return
            # The taint doesn't exist, so append the new taint to the existing taints
            node.spec.taints.append(new_taint)
        else:
            node.spec.taints = [new_taint]
        
        # Patch the node
        thread = self.api.patch_node(node_name, node)
        
        return thread
    
    def add_annotation(self, node_name, annotation_key, annotation_value):
        # Read the existing node
        node = self.api.read_node(node_name)

        # If the node already has annotations, add the new annotation to the dictionary
        if node.metadata.annotations is not None:
            node.metadata.annotations[annotation_key] = annotation_value
        # If the node doesn't have any annotations, initialize the annotations dictionary with the new annotation
        else:
            node.metadata.annotations = {annotation_key: annotation_value}

        # Update the node with the new annotation
        return self.api.patch_node(node_name, node)