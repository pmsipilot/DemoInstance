from novaclient.client import Client
import logging


class DemoProv():
    def __init__(self, config):
        pass

    def get_instances(self):
        raise NotImplementedError

    def instance_exist(self, id):
        raise NotImplementedError

    def instance_is_up(self, id):
        raise NotImplementedError

    def create_instance(self, image_conf):
        raise NotImplementedError

    def remove_instance(self, id):
        raise NotImplementedError

    def get_instance_ip(self, id):
        raise NotImplementedError
