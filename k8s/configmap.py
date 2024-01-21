from kubernetes import client, config

class ConfigMap:
    def __init__(self, namespace):
        config.load_incluster_config()
        self.api_instance = client.CoreV1Api()
        self.namespace = namespace
        
    def isExisting(self, name):
        try:
            resp = self.api_instance.read_namespaced_config_map(
                name=name, 
                namespace=self.namespace)
            return True
        except:
            return False
    
    def create(self, name, owner_references = None):
        body = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": name,
                "ownerReferences": owner_references
            },
            "data": {
                "config": "config"
            }
        }
        resp = self.api_instance.create_namespaced_config_map(
            body=body, 
            namespace=self.namespace)
        return resp
    
    def delete(self, name):
        resp = self.api_instance.delete_namespaced_config_map(
            name=name, 
            namespace=self.namespace)
        return resp