#this is a boilerplate log submodule

import yaml
import logging
import logging.config

def setup_logging(default_path = 'log.yaml', default_level = logging.INFO):
    path = default_path
    with open(path, 'rt') as f:
        try:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        except Exception as e:
            print(e)
            print('Error in Logging Configuration. Using default configs')
            logging.basicConfig(level=default_level)