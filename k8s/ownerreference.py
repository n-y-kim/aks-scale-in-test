from kubernetes import client, config

class OwnerReference:
    def __init__(self, kind, name, uid):
        config.load_incluster_config()
        self.kind = kind
        self.name = name
        self.uid = uid
        self.owner_reference = client.V1OwnerReference(
            api_version='apps/v1',
            block_owner_deletion=True,
            controller=True,
            kind=kind,
            name=name,
            uid=uid)

    def get_owner_reference(self):
        return self.owner_reference