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
        self.etcd_gsls_prefix: str = ""  # etcd 星地链路前缀
        self.etcd_satellites_prefix: str = ""  # etcd 卫星前缀
        self.etcd_ground_stations_prefix: str = ""  # etcd 地面站前缀
        self.constellation_start_time = None  # 星座启动时间
        self.position_update_interval = None  # 更新时间
        self.satellite_available_gsls: int = 0  # 卫星可用于星地链路的接口的数量
        self.time_step_key = None
        self.minimum_elevation_angle_key = None

    def load_from_env(self):
        """
        从环境变量之中进行配置的加载, 下列这些参数在创建容器的时候都被设置为了环境变量
        :return:
        """
        self.etcd_addr = os.getenv("ETCD_LISTEN_ADDR")
        self.etcd_port = int(os.getenv("ETCD_CLIENT_PORT"))
        self.etcd_isls_prefix = os.getenv("ETCD_ISLS_PREFIX")
        self.etcd_gsls_prefix = os.getenv("ETCD_GSLS_PREFIX")
        self.etcd_satellites_prefix = os.getenv("ETCD_SATELLITES_PREFIX")
        self.etcd_ground_stations_prefix = os.getenv("ETCD_GROUND_STATIONS_PREFIX")
        self.constellation_start_time = os.getenv("CONSTELLATION_START_TIME")
        self.resolve_constellation_start_time()
        self.position_update_interval = int(os.getenv("UPDATE_INTERVAL"))
        self.satellite_available_gsls = int(os.getenv("SATELLITE_AVAILABLE_GSLS"))
        self.time_step_key = os.getenv("TIME_STEP_KEY")
        self.minimum_elevation_angle_key = os.getenv("MINIMUM_ELEVATION_ANGLE_KEY")

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
