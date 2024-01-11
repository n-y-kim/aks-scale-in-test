from kubernetes import client, config
import yaml

class Deployment:
    def __init__(self):
        config.load_incluster_config()
        self.api_instance = client.AppsV1Api()

    def create_deployment(self, namespace, yaml_file_path, node_name):
        with open(yaml_file_path) as file:
            dep = yaml.safe_load(file)
            # Change the node name in the yaml file
            dep['spec']['template']['spec']['nodeSelector']['kubernetes.io/hostname'] = node_name
            # Change the deployment name in the yaml file to shield-deployment-<node_name>
            dep['metadata']['name'] = 'shield-deployment-' + node_name
            resp = self.api_instance.create_namespaced_deployment(
                body=dep, 
                namespace=namespace)
            return resp
            #print("Deployment created. status='%s'" % resp.metadata.name)
    
    def have_deployment(self, namespace, deployment_name):
        # if deployment exist, return True
        try:
            self.api_instance.read_namespaced_deployment(deployment_name, namespace)
            return True
        except:
            return False
    
    def delete_deployment(self, namespace, deployment_name):
        # if deployment exist, delete it
        try:
            self.api_instance.delete_namespaced_deployment(deployment_name, namespace)
            return True
        except:
            return False
        
    def check_other_deployments(self):        
        # Get all deployments
        deployments = self.api_instance.list_namespaced_deployment(namespace="default")
        
        # Check if there are any deployments with name starting with 'shield-deployment-'
        for deployment in deployments.items:
            if deployment.metadata.name.startswith("shield-deployment-"):
                return True
        
        return False

# Usage:
# dep = Deployment()
# dep.create_deployment("default", "shield_app.yaml")