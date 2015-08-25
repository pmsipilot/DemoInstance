from database import Instance
from demo_config import DemoConfig
from demo import Demo
import threading
from time import sleep
import logging


class Pool(threading.Thread):
    def __init__(self):
        self.config = DemoConfig()
        self.stop = False
        threading.Thread.__init__(self)

    def check_pool(self):
        demo = Demo(self.config)
        database = demo.database

        logging.debug('CHECK POOL INSTANCE')
        images_pool = {}
        instances_pool = {}

        # Get image key with pool value
        for key, image in self.config.images.items():
                images_pool[key] = {'need': 0, 'instances': []}
                if 'pool' in image:
                    images_pool[key]['need'] = image['pool']

        # Get all pooled instance
        for instance in demo.get_pooled_instance_database():
            # Type in database but not in config
            if instance['type'] not in images_pool:
                images_pool[instance['type']] = {'need': 0, 'instances': []}
            images_pool[instance['type']]['instances'].append(instance)

        for key, image_pool in images_pool.items():
            count_pool_instance = len(image_pool['instances'])
            # Remove overpopulated pool
            if image_pool['need'] < count_pool_instance:
                logging.debug('Pool %s is overpopulated', key)
                while count_pool_instance > image_pool['need']:
                    instance_to_remove = image_pool['instances'].pop()
                    demo.database_remove_server(instance_to_remove['id'])
                    count_pool_instance -= 1
            elif image_pool['need'] > count_pool_instance:
                logging.debug('Pool %s is underpopulated', key)
                while count_pool_instance < image_pool['need']:
                    logging.debug('Pool create %s', key)
                    demo.create_pool_instance(key)
                    count_pool_instance += 1
            else:
                logging.debug('Pool %s is ok', key)

    def run(self):
        time_between_iter = 60
        while True:
            try:
                self.check_pool()
            except Exception as e:
                if self.config.dev:
                    raise
                logging.error("Pool Raise Execption %s", e.message)
            i = 0
            while i < time_between_iter:
                if self.stop:
                    logging.info('Stop pool')
                    return
                i += 1
                sleep(1)
        logging.error('Pool is stop')
