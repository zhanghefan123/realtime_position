from entities.node import node as nm
from entities.link import link as lkm
from typing import List, Dict
from service import etcd_client as ecm
from config import loader as lm


class System:
    def __init__(self, config_loader: lm.Loader, etcd_client: ecm.EtcdClient, satellites: List[nm.Node],
                 inter_satellite_links: List[lkm.Link]):
        """
        进行系统的初始化
        :param config_loader: 配置加载对象
        :param etcd_client: etcd 客户端
        :param satellites: 所有的卫星
        :param inter_satellite_links: 所有的星间链路
        """
        self.config_loader = config_loader
        self.etcd_client = etcd_client
        self.satellites = satellites
        self.inter_satellite_links = inter_satellite_links

    def update_satellites_positions(self):
        """
        进行卫星的位置的更新
        :return:
        """
        for satellite in self.satellites:
            # 进行每个卫星的位置的更新
            satellite.update_position()

    def update_satellite_interface_delay(self):
        """
        进行链路的延迟的更新
        :return:
        """
        # 从节点的 pid 到所其所属的接口的一个映射
        # delay_map: Dict[int, Dict[str, float]] = {}
        for inter_satellite_link in self.inter_satellite_links:
            # 首先进行延迟的更新
            inter_satellite_link.update_delay()
            # 获取源和目的的 pid
            source_node = inter_satellite_link.source_node
            target_node = inter_satellite_link.target_node
            # 获取源和目的的接口名称
            source_iface_name = inter_satellite_link.source_iface_name
            target_iface_name = inter_satellite_link.target_iface_name
            # 存放到 delay map
            source_node.interface_delay_map[source_iface_name] = inter_satellite_link.delay_in_ms
            target_node.interface_delay_map[target_iface_name] = inter_satellite_link.delay_in_ms
        # 遍历所有的卫星进行更新
        for satellite in self.satellites:
            # 更新卫星的延迟
            self.etcd_client.update_satellite_delay(satellite)

    def update(self):
        """
        更新位置以及延迟
        :return:
        """
        self.update_satellites_positions()
        self.update_satellite_interface_delay()
