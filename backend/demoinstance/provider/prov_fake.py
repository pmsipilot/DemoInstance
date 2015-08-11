from prov import DemoProv
import uuid


class Fake(DemoProv):
    instances = {}

    def __init__(self, config):
        pass

    def get_instances(self):
        return Fake.instances.keys()

    def instance_exist(self, id):
        return id in Fake.instances

    def instance_is_up(self, id):
        return self.instance_exist(id)

    def create_instance(self, image_conf):
        id = str(uuid.uuid4())
        Fake.instances[id] = image_conf
        return id

    def remove_instance(self, id):
        del Fake.instances[id]

    def get_instance_ip(self, id):
        return '127.0.0.1'
