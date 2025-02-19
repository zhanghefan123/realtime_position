import etcd3
from config import loader as lm


class EtcdClient:
    def __init__(self, config_loader: lm.Loader):
        """
        初始化 EtcdClient
        :param config_loader: 配置加载对象
        """
        self.etcd_client = etcd3.client(host=config_loader.etcd_addr,
                                        port=config_loader.etcd_port)

    def get(self, prefix: str):
        """
        根据键进行值的索引
        :param prefix: 前缀
        :return: 键所对应的值
        """
        return self.etcd_client.get_prefix(prefix)

    def set(self, prefix: str, value):
        """
        根据<prefix, value>进行值的设置
        :param prefix: 前缀
        :param value 相应的值
        :return: None
        """
        self.etcd_client.put(prefix, value)