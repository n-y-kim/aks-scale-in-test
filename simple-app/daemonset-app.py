from k8s.daemonset import DaemonSet
from k8s.deployment import Deployment
from k8s.configmap import ConfigMap
from k8s.node import Node
from k8s.pod import Pod
from k8s.ownerreference import OwnerReference

from loggingconfig.logs import logger

import time
import os

def main():
    daemonset = DaemonSet('default')
    configmap = ConfigMap('default')
    pod = Pod('default')
    node_name = Node().get_node_name()
    
    ds_name = daemonset.get_daemonset_name()
    configmap_name = node_name + "-" + ds_name
    
    pod_name = os.getenv('HOSTNAME')
    
    while True:
        # Check if the configmap exists
        # If there is no configmap with the same name as the daemonset pod, this means that this is the first time the daemonset is created
        if not configmap.isExisting(configmap_name): 
            logger.info("Daemonset pod is being created for the first time.")
            
            owner = OwnerReference('Pod', pod_name, pod.get_uid(pod_name))
            owner_reference = owner.get_owner_reference()
            
            logger.info("Creating configmap for the first time.")
            # Create a configmap
            configmap.create(configmap_name, owner_references=[owner_reference])
            
            logger.info("Creating deployment using the file: log_app_deployment.yaml")
            # Create deployment
            deployment = Deployment('default')
            deployment.create('log_app_deployment.yaml', node_name)
            
        else:
            logger.info("This is not the first time the daemonset is being created. Configmap and deployment already exist.")
            
        time.sleep(10)

    return

if __name__ == '__main__':
    main()