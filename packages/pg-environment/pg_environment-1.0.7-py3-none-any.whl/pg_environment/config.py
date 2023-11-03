from pg_common import SingletonBase
from pg_common import log_info, merge_dict, is_valid_ip
import os
from pg_environment.define import *
import socket
import json


__auth__ = "baozilaji@gmail.com"
__all__ = ["config"]

__KEYS__ = ["SHELL", "PWD", "LOGNAME", "HOME", "LANG", "TERM", "USER", "OLDPWD"]


class _Config(SingletonBase):
    def __init__(self):
        self._conf = {}
        self._init()
        self._init_default()
        self._init_base()
        log_info(self._conf)

    def _init_base(self):
        # init host ip
        _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _sock.connect(('8.8.8.8', 80))
        _ip = _sock.getsockname()[0]
        _sock.close()
        if is_valid_ip(_ip):
            self.update(ENV_HOSTIP, _ip)

        # init work dir
        if not self.get_conf(ENV_PWD):
            self.update(ENV_PWD, os.getcwd())

        # init environ
        _work_dir = self.get_conf(ENV_PWD)
        _dir_name = _work_dir.split("/")[-1]
        self.update(ENV_ENVIRONMENT, EnvType.DEV.value)
        _channel = ""
        if _dir_name and len(_dir_name) > 0:
            _infos = _dir_name.split("_")
            if len(_infos) > 1:
                # dir name rules
                # xxxx_channel_port
                # xxxx_port
                # xxxx_channel, xxxx_10001_prod
                # xxxx, xxxx_test_10001_wx
                _useful = _infos[1:]
                for _info in _useful:
                    if _info in ('test', 'dev', 'prod'):
                        self.update(ENV_ENVIRONMENT, _info)
                    elif _info.isdigit():
                        self.update(ENV_HOSTPORT, int(_info))
                    else:
                        _channel = _info

        _env_default_file = "%s/conf/default.json" % (_work_dir, )
        if os.path.exists(_env_default_file):
            with open(_env_default_file, "r") as _f:
                merge_dict(self._conf, json.load(_f))


        # init from file
        _env_config_file = "%s/conf/%s.json" % (_work_dir, self.get_conf(ENV_ENVIRONMENT))
        if os.path.exists(_env_config_file):
            with open(_env_config_file, "r") as _f:
                merge_dict(self._conf, json.load(_f))

        self.update(ENV_CHANNEL, _channel)

        if self.get_conf(ENV_CHANNEL) and self.get_conf(ENV_ENVIRONMENT) == EnvType.PROD.value:
            _env_channel_cfg = "%s/conf/%s.json" % (_work_dir, self.get_conf(ENV_CHANNEL))
            if os.path.exists(_env_channel_cfg):
                with open(_env_channel_cfg, "r") as _f:
                    merge_dict(self._conf, json.load(_f))

    def _init(self):
        for _k, _v in os.environ.items():
            if _k in __KEYS__:
                self.update(_k.lower(), _v)

    def _init_default(self):
        self.merge(DEFAULT_CONF)

    def update(self, key, value):
        if key is None:
            return
        if key in self._conf and isinstance(self._conf[key], dict):
            if isinstance(value, dict):
                merge_dict(self._conf[key], value)
            else:
                self._conf[key] = value
        else:
            self._conf[key] = value

    def merge(self, values):
        if isinstance(values, dict):
            merge_dict(self._conf, values)

    def get_conf(self, key: str, default=None):
        return self._conf.get(key, default)
    
    def get_sub_conf(self, key: str, obj_key: str="", default=None):
        if not key:
            return default
        if not obj_key or not isinstance(obj_key, str):
            return self.get_conf(key, default)
        _sub = obj_key.split(".")
        _sub = [s for s in _sub if s != '']
        _last_has_key = None
        _last_obj = self._conf
        for _key in _sub:
            if key in _last_obj:
                _last_has_key = _last_obj
            if _key in _last_obj:
                _last_obj = _last_obj[_key]

                if key in _last_obj:
                    _last_has_key = _last_obj
        if _last_has_key:
            return _last_has_key[key]
        else:
            return default

    def is_dev(self):
        return self.get_conf(ENV_ENVIRONMENT) == EnvType.DEV.value

    def is_prod(self):
        return self.get_conf(ENV_ENVIRONMENT) == EnvType.PROD.value

    def is_test(self):
        return self.get_conf(ENV_ENVIRONMENT) == EnvType.TEST.value

    def get_channel(self):
        return self.get_conf(ENV_CHANNEL)

    def get_pwd(self):
        return self.get_conf(ENV_PWD)

    def is_debug(self):
        return self.get_conf(ENV_DEBUG)

    def get_host(self):
        return self.get_conf(ENV_HOSTIP)

    def get_port(self):
        return self.get_conf(ENV_HOSTPORT)

    def get_timezone(self):
        return self.get_conf(ENV_TIMEZONE)


config = _Config()
