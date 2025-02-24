from entities.node import common_info as cim
from entities.vars import consts as cm
from tools.tools import calculate_distance


class Link:
    def __init__(self, link_type,
                 link_id: int,
                 band_width: float,
                 source_node: cim.CommonInfo,
                 target_node: cim.CommonInfo,
                 source_iface_name: str,
                 target_iface_name: str):
        """
        初始化链路
        :param link_type: 链路类型
        :param link_id: 链路 ID
        :param source_node: 源节点
        :param target_node: 目的节点
        :param source_iface_name: 源节点接口名
        :param target_iface_name: 目的接口名
        """
        # ------ 初始化的属性 ------
        self.link_type = link_type
        self.link_id = link_id
        self.bandwidth = band_width
        self.source_node = source_node
        self.target_node = target_node
        self.source_iface_name = source_iface_name
        self.target_iface_name = target_iface_name
        # ------ 初始化的属性 ------

        # ------ 计算得到的属性 ------
        self.distance_in_meters: float = 0
        self.delay_in_ms: float = 0
        # ------ 计算得到的属性 ------

    def update_distance(self):
        """
        计算两个点之间的距离
        :return:
        """
        return calculate_distance(self.source_node, self.target_node)

    def update_delay(self):
        """
        先进行距离的更新，然后计算延迟
        :return:
        """
        self.distance_in_meters = self.update_distance()
        self.delay_in_ms = self.distance_in_meters / cm.LIGHT_SPEED * cm.S_TO_MS

    def __str__(self):
        """
        字符串表示
        :return:
        """
        return f"""
        link_id: {self.link_id}
        bandwidth: {self.bandwidth} bps
        source_node: {self.source_node}
        target_node: {self.target_node}
        delay: {self.delay_in_ms} ms
        """
