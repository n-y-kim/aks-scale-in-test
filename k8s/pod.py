from kubernetes import client, config

class Pod:
    def __init__(self, namespace):
        config.load_incluster_config()
        self.api = client.CoreV1Api()
        self.namespace = namespace
    
    def get_uid(self, pod_name):
        uid = self.api.list_namespaced_pod(self.namespace).items[0].metadata.uid
        return uid