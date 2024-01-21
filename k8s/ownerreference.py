from kubernetes import client, config

class OwnerReference:
    def __init__(self, kind, name, uid):
        config.load_incluster_config()
        self.kind = kind
        self.name = name
        self.uid = uid
        owner_reference = client.V1OwnerReference(
            api_version='apps/v1',
            block_owner_deletion=True,
            controller=True,
            kind=kind,
            name=name,
            uid=uid)

        return owner_reference