import logging
import yaml
from kubernetes import client, config

class Pdb:
    def __init__(self, namespace="default"):
        config.load_incluster_config()
        self.api_instance= client.PolicyV1Api()
        self.namespace = namespace
    
    def add_with_deployment_name(self, deployment_name, yaml_file_path):
        with open(yaml_file_path) as file:
            pdb = yaml.safe_load(file)
            pdb['metadata']['name'] = deployment_name + '-pdb'
            pdb['spec']['selector']['matchLabels']['deployment'] = deployment_name
            resp = self.api_instance.create_namespaced_pod_disruption_budget(
                namespace=self.namespace,
                body=pdb
            )
            return resp
        

    def patch_pdb(self, pdb_name="log-pdb", min_available=0):
        # Define the patch
        patch = [{"op": "replace", "path": "/spec/minAvailable", "value": min_available}]

        # Patch the PDB
        try:
            self.api_instance.patch_namespaced_pod_disruption_budget(
                name=pdb_name,
                namespace=self.namespace,
                body=patch
            )
        except Exception as e:
            logging.info("Exception when calling PolicyV1Api->patch_namespaced_pod_disruption_budget: %s\n" % e)