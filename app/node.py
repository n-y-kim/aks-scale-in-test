from kubernetes import client, config

class Node:
    def __init__(self):
        self.v1 = client.CoreV1Api()

    def get_node_status(self, node_name):
        # Get the node's status
        node_status = self.v1.read_node_status(node_name)

        # Print the node's status
        print(node_status.status)

    def get_node_name(self):
        # Load the in-cluster config
        config.load_incluster_config()

        # Get a list of all nodes
        nodes = self.v1.list_node().items

        # Get the hostname of the current node
        hostname = open('/etc/hostname').read().strip()

        # Find the node that the pod is running on
        my_node = next((node for node in nodes if node.metadata.name == hostname), None)

        if my_node is not None:
            print(f'This pod is running on node: {my_node.metadata.name}')
        else:
            print('Could not determine the node that this pod is running on.')
        
        return my_node.metadata.name if my_node else None