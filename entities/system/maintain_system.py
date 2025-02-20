import math
from entities.vars import consts as cm
from entities.node import ground_station as gm
from entities.node import satellite as sm
from entities.link import link as lkm
from typing import List
from service.etcd import api as eam
from config import loader as lm
from tools import tools as tm
from typing import Dict


class MaintainSystem:
    def __init__(self, config_loader: lm.Loader,
                 etcd_api: eam.EtcdApi,
                 satellites: List[sm.Satellite],
                 ground_stations: List[gm.GroundStation],
                 isls: List[lkm.Link]):
        """
        进行系统的初始化
        :param config_loader: 配置加载对象
        :param etcd_api: etcd api
        :param satellites: 所有的卫星
        :param isls: 所有的星间链路
        """
        self.config_loader = config_loader
        self.etcd_api = etcd_api
        self.satellites = satellites
        self.ground_stations = ground_stations
        self.isls = isls
        # self.satellite_gsl_mapping = {}
        # self.init_satellite_gsl_mapping()

    # def init_satellite_gsl_mapping(self):
    #     for satellite in self.satellites:
    #         self.satellite_gsl_mapping[satellite.container_name] = set()

    def update(self):
        """
        更新位置以及延迟
        :return:
        """
        print("update main function", flush=True)
        # 进行所有卫星位置的更新
        self.update_satellites_position()
        # 进行所有的星间链路的更新
        self.update_isls()
        # 进行所有的星地链路的更新
        self.update_gsls()
        # 进行所有的接口的延迟的更新
        self.update_interfaces_delay()

    def update_satellites_position(self):
        """
        进行卫星的位置的更新
        :return: None
        """
        # 遍历每个卫星
        for satellite in self.satellites:
            # 进行每个卫星的位置的更新
            satellite.update_position()

    def update_gsls(self):
        """
        找到应该要进行建立的那些 gsls, 以目前的方式来说, 每个地面站选择一个最近的卫星, 卫星可能允许多个 ISL
        :return:
        """
        gsls = []
        satellite_gsl_mapping = {}
        # 对每个地面站进行最近卫星的寻找
        # -----------------------------------------------------
        for ground_station in self.ground_stations:
            # 最近距离
            cloest_distance = math.inf
            # 最近卫星
            closest_satellite = None
            for satellite in self.satellites:
                # 判断卫星是否已经达到了最大的连接数量
                if ((satellite.container_name in satellite_gsl_mapping.keys()) and
                        (len(satellite_gsl_mapping[satellite.container_name]) >= self.config_loader.satellite_available_gsls)):
                    # 如果已经达到了最大的连接数量则继续
                    continue
                else:
                    # 计算距离
                    distance = tm.calculate_distance(source_node=ground_station, target_node=satellite)
                    # 进行距离的比较
                    if distance < cloest_distance:
                        # 设置最近的距离
                        cloest_distance = distance
                        # 设置最近的卫星
                        closest_satellite = satellite
            # 更新 mapping
            if closest_satellite.container_name not in satellite_gsl_mapping.keys():
                satellite_gsl_mapping[closest_satellite.container_name] = {ground_station.container_name}
            else:
                satellite_gsl_mapping[closest_satellite.container_name].add(ground_station.container_name)
            # -----------------------------------------------------

            if (ground_station.connected_satellite is None) or (ground_station.connected_satellite.container_name != closest_satellite.container_name):
                # 如果之前没有连接过

                # step1 更新最近卫星
                ground_station.connected_satellite = closest_satellite

                # step2 创建新的星地链路
                gsl = lkm.Link(link_type=cm.LinkTypeGSL,
                               link_id=1,
                               band_width=100,
                               source_node=ground_station,
                               target_node=closest_satellite,
                               source_iface_name=f"{cm.GroundStationPrefix}{ground_station.node_id}_idx{1}",
                               # 当前给的 idx 是错误的 idx
                               target_iface_name=f"{cm.SatellitePrefix}{closest_satellite.node_id}_idx{1}")  # 当前给的 idx 是错误的 idx

                # step3 将 gsl 添加到 gsl 列表之中
                gsls.append(gsl)
            else:
                pass

        # 放到 etcd 之中
        self.etcd_api.set_gsls(gsls)

    def update_isls(self):
        """
        进行星间链路的更新
        :return:
        """
        for isl in self.isls:
            # 首先进行延迟的更新
            isl.update_delay()
            # 获取源和目的的 pid
            source_node = isl.source_node
            target_node = isl.target_node
            # 获取源和目的的接口名称
            source_iface_name = isl.source_iface_name
            target_iface_name = isl.target_iface_name
            # 存放到 delay map
            source_node.interface_delay_map[source_iface_name] = isl.delay_in_ms
            target_node.interface_delay_map[target_iface_name] = isl.delay_in_ms

    def update_interfaces_delay(self):
        """
        进行各个接口的信息的更新
        :return:
        """
        # 更新所有卫星接口的延迟
        self.etcd_api.set_satellites_position_and_interface_delay(self.satellites)
        # 更新所有地面站接口的延迟
        self.etcd_api.set_ground_stations_interface_delay(self.ground_stations)
