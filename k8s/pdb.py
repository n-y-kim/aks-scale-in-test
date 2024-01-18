import logging
from kubernetes import client, config

class Pdb:
    def __init__(self):
        config.load_incluster_config()
        self.api= client.PolicyV1Api()

    def patch_pdb(self, pdb_name="log-pdb", namespace="default", min_available=0):
        # Define the patch
        patch = [{"op": "replace", "path": "/spec/minAvailable", "value": min_available}]

        # Patch the PDB
        try:
            self.api_instance.patch_namespaced_pod_disruption_budget(
                name=pdb_name,
                namespace=namespace,
                body=patch
            )
        except Exception as e:
            logging.info("Exception when calling PolicyV1Api->patch_namespaced_pod_disruption_budget: %s\n" % e)