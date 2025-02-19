import argparse
import time
import signal
from config import loader as lm
from service.etcd import api as eam
from service.etcd import client as ecm
from typing import Dict, Callable
from entities.system import maintain_system as sm


def signal_handler(signum, frame):
    """
    信号处理函数
    :param signum: 信号量
    :param frame:  帧
    :return:
    """
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
        self.config_file_path: str = ""  # 配置文件的路径
        self.config_loader = None
        self.etcd_api = None
        self.system = None
        self.start_functions: Dict[str, Callable] = {
            Starter.PARSE_CMD_ARGS: self.parse_cmd_args,
            Starter.SET_CONFIG_LOADER: self.set_config_loader,
            Starter.SET_ETCD_CLIENT: self.set_etcd_client,
            Starter.SET_SYSTEM: self.set_maintain_system,
            Starter.UPDATE_STATUS: self.run_maintain_system,
        }

    def start(self):
        """
        系统启动方法
        :return None
        """
        for index, key in enumerate(self.start_functions.keys()):
            print(f"step {index + 1}: {key}")
            corresponding_function = self.start_functions[key]
            corresponding_function()

    def parse_cmd_args(self):
        """
        step1: 进行命令行参数的解析, 并返回配置文件的路径
        :return: None
        """
        parser = argparse.ArgumentParser("realtime position parser")
        parser.add_argument('--config', help='Path to configuration file', required=False,
                            default="../security_topology/resources/configuration.yml")
        config_file_path = parser.parse_args().config
        self.config_file_path = config_file_path

    def set_config_loader(self):
        """
        step2: 进行 config_loader 配置对象的设置
        :return: None
        """
        self.config_loader = lm.Loader(config_file_path=self.config_file_path)
        self.config_loader.load_from_env()

    def set_etcd_client(self):
        """
        step3: 进行 etcd_client 的设置
        :return: None
        """
        etcd_client = ecm.EtcdClient(config_loader=self.config_loader)
        self.etcd_api = eam.EtcdApi(etcd_client=etcd_client, config_loader=self.config_loader)

    def set_maintain_system(self):
        """
        初始化系统
        :return: None
        """
        satellites = self.etcd_api.load_satellites()
        ground_stations = self.etcd_api.load_ground_stations()
        inter_satellite_links = self.etcd_api.load_isls(satellites)
        self.system = sm.MaintainSystem(config_loader=self.config_loader,
                                        etcd_api=self.etcd_api,
                                        satellites=satellites,
                                        ground_stations=ground_stations,
                                        isls=inter_satellite_links)

    def run_maintain_system(self):
        """
        进行系统状态的更新
        :return:
        """
        # 注册信号处理函数
        signal.signal(signal.SIGTERM, signal_handler)
        # 进行系统的更新
        while True:
            self.system.update()
            time.sleep(self.config_loader.position_update_interval)


if __name__ == "__main__":
    system = Starter()
    system.start()
