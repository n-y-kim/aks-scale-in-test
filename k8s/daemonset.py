from kubernetes import client, config

class DaemonSet:
    def __init__(self):
        config.load_incluster_config()
        self.api = client.AppsV1Api()
        
    # Get daemonset's name
    def get_daemonset_name(self, namespace):
        daemonset_name = self.api.list_namespaced_daemon_set(namespace).items[0].metadata.name
        return daemonset_name

    # Add PriorityClass to the daemonset
    def add_priority_class(self, namespace, daemonset_name):
        body = {
            "spec": {
                "template": {
                    "spec": {
                        "priorityClassName": "system-node-critical"
                    }
                }
            }
        }
        resp = self.api.patch_namespaced_daemon_set(
            name=daemonset_name,
            namespace=namespace,
            body=body
        )
        return resp
    
    def delete_priority_class(self, namespace, daemonset_name):
        body = {
            "spec": {
                "template": {
                    "spec": {
                        "priorityClassName": None
                    }
                }
            }
        }
        resp = self.api.patch_namespaced_daemon_set(
            name=daemonset_name,
            namespace=namespace,
            body=body
        )
        return resp