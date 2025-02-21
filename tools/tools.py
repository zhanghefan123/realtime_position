import math
from entities.node import common_info as cim
from entities.vars import consts as cm


def calculate_elevation(ground_station: cim.CommonInfo, satellite: cim.CommonInfo):
    """
    计算卫星与地面站之间的仰角
    :param ground_station: 地面站信息
    :param satellite: 卫星信息
    :return:
    """
    return calculate_elevation_inner(
        ground_station.current_position[cm.LONGITUDE_KEY],
        ground_station.current_position[cm.LATITUDE_KEY],
        satellite.current_position[cm.LONGITUDE_KEY],
        satellite.current_position[cm.LATITUDE_KEY],
        satellite.current_position[cm.ALTITUDE_KEY]
    )


def calculate_elevation_inner(ground_longitude_rad, ground_latitude_rad, satellite_longitude_rad,
                              satellite_latitude_rad,
                              satellite_altitude):
    """
    计算卫星与地面站之间的仰角
    :param ground_longitude_rad: 地面站经度
    :param ground_latitude_rad: 地面站纬度
    :param satellite_longitude_rad: 卫星经度
    :param satellite_latitude_rad: 卫星纬度
    :param satellite_altitude: 卫星高度 (单位为米)
    """

    # 地心角计算
    delta_longitude = ground_longitude_rad - satellite_longitude_rad
    cos_gamma = (math.cos(ground_latitude_rad) * math.cos(satellite_latitude_rad) * math.cos(delta_longitude) +
                 math.sin(ground_latitude_rad) * math.sin(satellite_latitude_rad))
    gamma = math.acos(cos_gamma)

    # 计算仰角
    numerator = math.cos(gamma) - (cm.R_EARTH / (cm.R_EARTH + satellite_altitude))
    denominator = math.sin(gamma)

    if denominator == 0:
        return 90.0 if numerator >= 0 else -90.0

    elevation_rad = math.atan(numerator / denominator)
    elevation_deg = math.degrees(elevation_rad)
    return elevation_deg


def geodetic_to_cartesian(latitude_rad, longitude_rad, altitude, R_EARTH):
    """
    将地理坐标（纬度、经度、高度）转换为三维直角坐标（x, y, z）
    :param latitude_rad: 纬度（弧度）
    :param longitude_rad: 经度（弧度）
    :param altitude: 高度（米）
    :param R_EARTH: 地球半径（米）
    :return: (x, y, z) 坐标（米）
    """
    # 计算 z 和 base
    z = (R_EARTH + altitude) * math.sin(latitude_rad)
    base = (R_EARTH + altitude) * math.cos(latitude_rad)

    # 计算 x 和 y
    x = base * math.cos(longitude_rad)
    y = base * math.sin(longitude_rad)

    return x, y, z


def calculate_distance(source_node: cim.CommonInfo, target_node: cim.CommonInfo):
    """
    计算两个点之间的距离
    :param source_node: 源节点基本信息
    :param target_node: 目的节点基本信息
    :return: 两点之间的三维距离（米）
    """
    # 获取两点之间的坐标
    source_position = source_node.current_position
    target_position = target_node.current_position

    # 将地理坐标转换为直角坐标
    x1, y1, z1 = geodetic_to_cartesian(
        source_position[cm.LATITUDE_KEY],
        source_position[cm.LONGITUDE_KEY],
        source_position[cm.ALTITUDE_KEY],
        cm.R_EARTH
    )
    x2, y2, z2 = geodetic_to_cartesian(
        target_position[cm.LATITUDE_KEY],
        target_position[cm.LONGITUDE_KEY],
        target_position[cm.ALTITUDE_KEY],
        cm.R_EARTH
    )
    distance_in_meters = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    return distance_in_meters
