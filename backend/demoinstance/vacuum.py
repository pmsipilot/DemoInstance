from database import Instance
from demo_config import DemoConfig
from demo import Demo
import threading
from time import sleep
import logging


class Vacuum(threading.Thread):
    def __init__(self):
        self.config = DemoConfig()
        self.stop = False
        threading.Thread.__init__(self)

    def check_old_instance(self):
        demo = Demo(self.config)
        database = demo.database

        logging.debug('CHECK OLD INSTANCE')
        query = database\
            .query(Instance)\
            .filter(Instance.status != 'DELETED')\
            .filter(Instance.status != 'POOL')
        logging.debug("%s count", query.count())
        instances = demo.provider.get_instances()
        for data_instance in query.all():
            if data_instance.get_dead_time() == -1:
                logging.info('%s is to old', data_instance.provider_id)
                demo.database_remove_server(data_instance.provider_id)

            on_cloud = False
            for id in instances:
                if data_instance.provider_id == id:
                    on_cloud = True
                    break
            if not on_cloud and data_instance.provider_id:
                logging.info(
                    '%s is not present on cloud anymore',
                    data_instance.id
                )
                demo.database_remove_server(data_instance.provider_id)

    def run(self):
        time_between_vacuum = 60
        while True:
            try:
                self.check_old_instance()
            except Exception as e:
                if self.config.dev:
                    raise
                logging.error("Vaccum Raise Execption %s", e.message)
            i = 0
            while i < time_between_vacuum:
                if self.stop:
                    logging.info('Stop vacuum')
                    return
                i += 1
                sleep(1)
        logging.error('Vacuum is stop')
