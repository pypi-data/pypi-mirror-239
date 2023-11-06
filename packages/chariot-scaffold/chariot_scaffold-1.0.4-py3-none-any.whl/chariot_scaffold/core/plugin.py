import os
import sys
import abc
import json
import yaml
import requests
from chariot_scaffold import plugin_spec, lang
from chariot_scaffold.tools import generate_file
from chariot_scaffold.core.base import Base
from chariot_scaffold.tools import generate_online_pack, generate_offline_pack


requests.packages.urllib3.disable_warnings() # noqa


class Connection(Base):
    def __init__(self, model=None):
        super().__init__(model=model)

    def hook(self):
        connection = {}
        for k, v in self.input.items():
            connection[k] = {"title": {lang: v["title"]}, "description": {lang: v["description"]}, "type": v["type"]}

            if v["required"]:
                connection[k]["required"] = v["required"]
            if v["default"] is not None:
                connection[k]["default"] = v["default"]
        plugin_spec.connection = connection


class Action(Base):
    def __init__(self, title=None, description=None, model=None): # noqa
        super().__init__(title, description, model)

    def hook(self):
        actions = {self._func_name: {"title": {lang: self.title} , "description": {lang: self.description}, "input": {}, "output":{}}}

        for k, v in self.input.items():
            actions[self._func_name]["input"][k] = {"title": {lang: v["title"]}, "description": {lang: v["description"]}, "type": v["type"]}

            if v["required"]:
                actions[self._func_name]["input"][k]["required"] = v["required"]
            if v["default"] is not None:
                actions[self._func_name]["input"][k]["default"] = v["default"]

        if not self.output.get("output"):
            # 返回值注解绑定
            for k, v in self.output.items():
                actions[self._func_name]["output"][k] = {"title": {lang: v["title"]}, "description": {lang: v["description"]}, "type": v["type"]}
        else:
            # 默认返回值绑定
            actions[self._func_name]["output"]["output"] = {"title": {lang: "输出"}, "description": {lang: "输出"}, "type": self.output["output"]["type"]}

        plugin_spec.actions.update(actions)


class Trigger(Base):
    def __init__(self, title=None, description=None, model=None):   # noqa
        super().__init__(title, description, model)

    def hook(self):
        alarm_receivers ={self._func_name: {"title": {lang: self.title} , "description": {lang: self.description},
                                            "input": {}}}
        for k, v in self.input.items():
            alarm_receivers[self._func_name]["input"][k] = {"title": {lang: v["title"]},
                                                            "description": {lang: v["description"]}, "type": v["type"]}

            if v["required"]:
                alarm_receivers[self._func_name]["input"][k]["required"] = v["required"]
            if v["default"] is not None:
                alarm_receivers[self._func_name]["input"][k]["default"] = v["default"]
        plugin_spec.alarm_receivers.update(alarm_receivers)


class Pack(metaclass=abc.ABCMeta):
    def __init__(self):
        ...

    @abc.abstractmethod
    def connection(self, *args, **kwargs):  # 该裹的裹脚布一个也少不了
        ...

    @classmethod
    def plugin_config_init(cls, name, title=None, description=None, version=None):

        plugin_spec.entrypoint = os.path.split(os.path.abspath(sys.modules[cls.__module__].__file__))[-1].replace('.py', '')

        plugin_spec.module= cls.__name__
        plugin_spec.title =  title if title else cls.__name__
        plugin_spec.version =  version if version else "0.1.0"
        plugin_spec.description = description
        plugin_spec.name = name

    @classmethod
    def generate_online_pack(cls, path=None):
        file_path = os.path.abspath(sys.modules[cls.__module__].__file__) if path is None else path
        assert os.path.exists(file_path), FileNotFoundError("目录不存在")
        generate_online_pack(file_path, plugin_spec.name, plugin_spec.vendor, plugin_spec.version)

    @classmethod
    def generate_offline_pack(cls, path=None):
        file_path = os.path.abspath(sys.modules[cls.__module__].__file__) if path is None else path
        assert os.path.exists(file_path), FileNotFoundError("目录不存在")
        generate_offline_pack(file_path, plugin_spec.name, plugin_spec.vendor, plugin_spec.version)

    def send(self, alarm):
        assert plugin_spec.alarm_receivers, "只能在声明了Trigger的方法中使用"
        session = requests.session()
        response = session.post(self.dispatcher_url, verify=False, json=alarm)
        assert response.status_code == 200, "调用失败"


    def set_cache(self, data):
        assert plugin_spec.alarm_receivers, "只能在声明了Trigger的方法中使用"
        session = requests.session()
        cache = {
            "method": "set",
            "data": json.dumps(data),
        }
        response = session.post(self.cache_url, json=cache, verify=False)
        assert response.status_code == 200, "调用失败"
        return response.json()

    def get_cache(self):
        assert plugin_spec.alarm_receivers, "只能在声明了Trigger的方法中使用"
        session = requests.session()
        method = {
            "method": "get"
        }
        response = session.post(self.cache_url, json=method, verify=False)
        assert response.status_code == 200, "调用失败"
        return response.json()

    def create_yaml(self, path=None):
        file_path = path if path is not None else "./"
        assert os.path.exists(file_path), FileNotFoundError("目录不存在")
        stream = open(os.path.join(file_path, "plugin.spec.yaml"), 'w', encoding='utf8')
        yaml.safe_dump(self.json, stream, allow_unicode=True, sort_keys=False, default_flow_style=False)

    def generate_project(self, path=None):
        self.create_yaml(path=path)
        generate_file(module=plugin_spec.module, entrypoint=plugin_spec.entrypoint, path=path)

    @property
    def yaml(self):
        return yaml.safe_dump(self.json, allow_unicode=True, sort_keys=False)

    @property
    def json(self):
        return json.loads(plugin_spec.__repr__())

    @property
    def dispatcher_url(self):
        return "http://127.0.0.1:10001/transpond"

    @dispatcher_url.setter
    def dispatcher_url(self, url):
        self.dispatcher_url = url

    @property
    def cache_url(self):
        return ""

    @cache_url.setter
    def cache_url(self, url):
        self.cache_url = url

    @property
    def webhook_url(self):
        return ""

    @webhook_url.setter
    def webhook_url(self, url):
        self.webhook_url = url

    def __repr__(self):
        return plugin_spec.__repr__()
