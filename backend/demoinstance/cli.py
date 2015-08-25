from demo_config import DemoConfig
from database import DemoData
from http import ThreadedHTTPServer, Handler
from vacuum import Vacuum
from pool import Pool
import logging
import argparse

def cli_entrypoint():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='config file', default='./config.ini')
    args = parser.parse_args()

    DemoConfig.config_file = args.c
    config = DemoConfig()

    # create table
    session = DemoData.get_session(config)
    session.close()

    logging.basicConfig(level=config.log_level)
    vacuum = Vacuum()
    pool = Pool()
    try:
        vacuum.start()
        pool.start()
        server = ThreadedHTTPServer(('0.0.0.0', config.http_port), Handler)
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Exit signal catched")
        vacuum.stop = True
