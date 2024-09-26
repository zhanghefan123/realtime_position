import argparse
import time
import signal
from config import loader as lm
from service import etcd_client as ecm
from typing import Dict, Callable
from entities.system import system as sm


def signal_handler(signum, frame):
    exit()


class Starter:
    PARSE_CMD_ARGS = "parse_cmd_args"
    SET_CONFIG_LOADER = "set_config_loader"
    SET_ETCD_CLIENT = "set_etcd_client"
    SET_SYSTEM = "set_system"
    UPDATE_STATUS = "update_status"

    def __init__(self):
        """
        进行系统的初始化
        """
        self.config_file_path: str = ""
        self.config_loader = None
        self.etcd_client = None
        self.system = None
        self.start_functions: Dict[str, Callable] = {
            Starter.PARSE_CMD_ARGS: self.parse_cmd_args,
            Starter.SET_CONFIG_LOADER: self.set_config_loader,
            Starter.SET_ETCD_CLIENT: self.set_etcd_client,
            Starter.SET_SYSTEM: self.set_system,
            Starter.UPDATE_STATUS: self.update_status,
        }

    def start(self):
        """
        系统启动方法
        """
        for index, key in enumerate(self.start_functions.keys()):
            print(f"step {index + 1}: {key}")
            corresponding_function = self.start_functions[key]
            corresponding_function()

    def parse_cmd_args(self):
        """
        进行命令行参数的解析, 并返回配置文件的路径
        :return: config_file_path
        """
        parser = argparse.ArgumentParser("realtime position parser")
        parser.add_argument('--config', help='Path to configuration file', required=False,
                            default="../security_topology/resources/configuration.yml")
        config_file_path = parser.parse_args().config
        self.config_file_path = config_file_path

    def set_config_loader(self):
        """
        进行 config_loader 配置对象的设置
        :return:
        """
        self.config_loader = lm.Loader(config_file_path=self.config_file_path)
        self.config_loader.load_from_env()

    def set_etcd_client(self):
        """
        进行 etcd_client 的设置
        :return:
        """
        self.etcd_client = ecm.EtcdClient(config_loader=self.config_loader)

    def set_system(self):
        """
        初始化系统
        :return:
        """
        satellites = self.etcd_client.load_satellites()
        inter_satellite_links = self.etcd_client.load_inter_satellite_links(satellites)
        self.system = sm.System(config_loader=self.config_loader,
                                etcd_client=self.etcd_client,
                                satellites=satellites,
                                inter_satellite_links=inter_satellite_links)

    def update_status(self):
        """
        进行系统状态的更新
        :return:
        """
        signal.signal(signal.SIGTERM, signal_handler)
        while True:
            self.system.update()
            print("update delay")
            time.sleep(self.config_loader.position_update_interval)


if __name__ == "__main__":
    system = Starter()
    system.start()
