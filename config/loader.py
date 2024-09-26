import os
import yaml
from datetime import datetime


class Loader:
    def __init__(self, config_file_path: str):
        """
        进行配置对象的初始化
        :param config_file_path: 配置对象路径
        """
        self.config_file_path = config_file_path  # 配置对象路径
        self.etcd_addr: str = ""  # etcd 监听地址
        self.etcd_port: int = 0  # etcd 监听端口
        self.etcd_isls_prefix: str = ""  # etcd 星间链路前缀
        self.etcd_satellites_prefix: str = ""  # etcd 卫星前缀
        self.constellation_start_time = None  # 星座启动时间
        self.position_update_interval = None  # 更新时间

    def load_from_env(self):
        """
        从环境变量之中进行配置的加载
        :return:
        """
        self.etcd_addr = os.getenv("ETCD_LISTEN_ADDR")
        self.etcd_port = int(os.getenv("ETCD_CLIENT_PORT"))
        self.etcd_isls_prefix = os.getenv("ETCD_ISLS_PREFIX")
        self.etcd_satellites_prefix = os.getenv("ETCD_SATELLITES_PREFIX")
        self.constellation_start_time = os.getenv("CONSTELLATION_START_TIME")
        self.resolve_constellation_start_time()
        self.position_update_interval = int(os.getenv("UPDATE_INTERVAL"))

    # def load(self):
    #     """
    #     进行配置的加载
    #     """
    #     # 1. 打开文件并使用 yaml 库进行解析
    #     with open(file=self.config_file_path, mode='r', encoding="utf-8") as f:
    #         content = f.read()
    #         config_data = yaml.load(content, Loader=yaml.FullLoader)
    #
    #     # 2. etcd 配置
    #     self.etcd_addr = config_data["network_config"]["local_network_address"]
    #     etcd_config = config_data["services_config"]["etcd_config"]
    #     self.etcd_port = int(etcd_config["client_port"])
    #
    #     self.etcd_isls_prefix = etcd_config["etcd_prefix"]["isls_prefix"]
    #     self.etcd_satellites_prefix = etcd_config["etcd_prefix"]["satellites_prefix"]
    #
    #     # 3. 加载星座配置
    #     self.constellation_start_time = config_data["constellation_config"]["start_time"]
    #
    #     # 4. 解析启动时间
    #     self.resolve_constellation_start_time()

    def resolve_constellation_start_time(self):
        """
        解析星座启动时间
        """
        year, month, date, hour, minute, second = self.constellation_start_time.split("|")
        constellation_start_time = datetime(int(year), int(month), int(date),
                                            int(hour), int(minute), int(second))
        self.constellation_start_time = constellation_start_time

    def __str__(self):
        """
        配置对象的字符串表示
        :return:
        """
        return f"""
        etcd_addr: {self.etcd_addr}
        etcd_port: {self.etcd_port}
        etcd_isls_prefix: {self.etcd_isls_prefix}
        etcd_satellites_prefix: {self.etcd_satellites_prefix}
        """
