from kubernetes import client, config

class DaemonSet:
    def __init__(self, namespace):
        config.load_incluster_config()
        self.api = client.AppsV1Api()
        self.namespace = namespace
        
    # Get daemonset's name
    def get_daemonset_name(self):
        daemonset_name = self.api.list_namespaced_daemon_set(self.namespace).items[0].metadata.name
        return daemonset_name

    # Add PriorityClass to the daemonset
    def add_priority_class(self, daemonset_name):
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
            namespace=self.namespace,
            body=body
        )
        return resp
    
    def delete_priority_class(self, daemonset_name):
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
            namespace=self.namespace,
            body=body
        )
        return resp
    
    def get_uid(self, daemonset_name):
        uid = self.api.list_namespaced_daemon_set(self.namespace).items[0].metadata.uid
        return uid