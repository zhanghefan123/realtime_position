import math
from entities.node import node as nm
from entities.vars import consts as cm


class Link:
    def __init__(self, link_type,
                 link_id: int,
                 band_width: float,
                 source_node: nm.Node,
                 target_node: nm.Node,
                 source_iface_name: str,
                 target_iface_name: str):
        """
        初始化链路
        :param link_type: 链路类型
        :param source_node: 源节点
        :param target_node: 目的节点
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
        source_position = self.source_node.current_position
        target_position = self.target_node.current_position
        z1 = (source_position[cm.ALTITUDE_KEY] + cm.R_EARTH) * math.sin(source_position[cm.LATITUDE_KEY])
        base1 = (source_position[cm.ALTITUDE_KEY] + cm.R_EARTH) * math.cos(source_position[cm.LATITUDE_KEY])
        x1 = base1 * math.cos(source_position[cm.LONGITUDE_KEY])
        y1 = base1 * math.sin(source_position[cm.LONGITUDE_KEY])
        z2 = (target_position[cm.ALTITUDE_KEY] + cm.R_EARTH) * math.sin(target_position[cm.LATITUDE_KEY])
        base2 = (target_position[cm.ALTITUDE_KEY] + cm.R_EARTH) * math.cos(target_position[cm.LATITUDE_KEY])
        x2 = base2 * math.cos(target_position[cm.LONGITUDE_KEY])
        y2 = base2 * math.sin(target_position[cm.LONGITUDE_KEY])
        distance_in_meters = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
        self.distance_in_meters = distance_in_meters

    def update_delay(self):
        """
        先进行距离的更新，然后计算延迟
        :return:
        """
        self.update_distance()
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
