# encoding:utf-8

import json
import os
from common.log import logger

# 将所有可用的配置项写在字典里
available_setting ={}

class Config(dict):
    def __getitem__(self, key):
        if key not in available_setting:
            raise Exception("key {} not in available_setting".format(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key not in available_setting:
            raise Exception("key {} not in available_setting".format(key))
        return super().__setitem__(key, value)

    def get(self, key, default=None):
        try :
            return self[key]
        except KeyError as e:
            return default
        except Exception as e:
            raise e
    
config = Config()

def load_config():
    global config
    config_path = "./config.json"
    if not os.path.exists(config_path):
        logger.info('配置文件不存在，将使用config-template.json模板')
        config_path = "./config-template.json"

    config_str = read_file(config_path)
    # 将json字符串反序列化为dict类型
    config = Config(json.loads(config_str))

    # override config with environment variables.
    # Some online deployment platforms (e.g. Railway) deploy project from github directly. So you shouldn't put your secrets like api key in a config file, instead use environment variables to override the default config.
    for name, value in os.environ.items():
        if name in available_setting:
            logger.info("[INIT] override config by environ args: {}={}".format(name, value))
            config[name] = value

    logger.info("[INIT] load config: {}".format(config))



def get_root():
    return os.path.dirname(os.path.abspath( __file__ ))


def read_file(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()


def conf():
    return config
