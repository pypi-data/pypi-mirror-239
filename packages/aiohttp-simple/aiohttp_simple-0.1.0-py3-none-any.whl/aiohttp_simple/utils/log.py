import logging
import logging.config
import os
from llm_test_group.utils.setting import check_config_file_folder

import yaml


class Log:
    def init_log(self):
        config_file_folder = check_config_file_folder()
        logConfFile = os.path.join(config_file_folder, "log.yaml")
        with open(logConfFile, "r") as f:
            cfg = yaml.load(f, Loader=yaml.loader.SafeLoader)
        logging.config.dictConfig(cfg)
    
    def getLogger(self, name):
        return logging.getLogger()

if __name__ == "__main__":
    Log().init_log()
    logger1 = logging.getLogger()
    logger1.info('1')
    logger1.warning('1')
