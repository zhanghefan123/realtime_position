import math
from entities.node import common_info as cim
from entities.vars import consts as cm


def calculate_distance(source_node: cim.CommonInfo, target_node: cim.CommonInfo):
    """
    计算两个点之间的距离
    :param source_node: 源节点基本信息
    :param target_node: 目的节点基本信息
    :return:
    """
    source_position = source_node.current_position
    target_position = target_node.current_position
    z1 = (source_position[cm.ALTITUDE_KEY] + cm.R_EARTH) * math.sin(source_position[cm.LATITUDE_KEY])
    base1 = (source_position[cm.ALTITUDE_KEY] + cm.R_EARTH) * math.cos(source_position[cm.LATITUDE_KEY])
    x1 = base1 * math.cos(source_position[cm.LONGITUDE_KEY])
    y1 = base1 * math.sin(source_position[cm.LONGITUDE_KEY])
    z2 = (target_position[cm.ALTITUDE_KEY] + cm.R_EARTH) * math.sin(target_position[cm.LATITUDE_KEY])
    base2 = (target_position[cm.ALTITUDE_KEY] + cm.R_EARTH) * math.cos(target_position[cm.LATITUDE_KEY])
    x2 = base2 * math.cos(target_position[cm.LONGITUDE_KEY])
    y2 = base2 * math.sin(target_position[cm.LONGITUDE_KEY])
    distance_in_meters = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    return distance_in_meters
