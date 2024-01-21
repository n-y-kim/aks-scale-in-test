from k8s.daemonset import DaemonSet
from k8s.deployment import Deployment
from k8s.configmap import ConfigMap
from k8s.ownerreference import OwnerReference
from loggingconfig.logs import logger

def main():
    daemonset = DaemonSet()
    configmap = ConfigMap('default')
    configmap_name = daemonset.get_daemonset_name()
    
    # Check if the configmap exists
    # If there is no configmap with the same name as the daemonset, this means that this is the first time the daemonset is created
    if not configmap.isExisting(configmap_name): 
        logger.info("Daemonset is being created for the first time.")
        
        owner = OwnerReference('DaemonSet', configmap_name, daemonset.get_uid())
        
        logger.info("Creating configmap for the first time.")
        # Create a configmap
        configmap.create(configmap_name, owner_references=[owner])
        
        logger.info("Creating deployment using the file: log_app_deployment.yaml")
        # Create deployment
        deployment = Deployment()
        deployment.create('default', 'log_app_deployment.yaml')
        
    else:
        logger.info("This is not the first time the daemonset is being created. Configmap and deployment already exist.")
        
    return

if __name__ == '__main__':
    main()