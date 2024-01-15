from kubernetes import client, config

class Nodes:
    def __init__(self):
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()

    def get_nodes_with_annotation(self, annotation_key):
        ret = self.v1.list_node(watch=False)
        nodes_with_annotation = [node for node in ret.items if annotation_key in node.metadata.annotations]
        return nodes_with_annotation

    def update_annotations(self, node_name, annotation_key, annotation_value):
        body = {
            "metadata": {
                "annotations": {
                    annotation_key: annotation_value
                }
            }
        }
        return self.v1.patch_node(node_name, body)