from service.etcd import client as ecm
from entities.vars import consts as cm
from entities.node import satellite as sm
from entities.node import ground_station as gm
from entities.link import link as lkm
from entities.protobuf.node import node_pb2 as npb
from entities.protobuf.link import link_pb2 as lpb
from config import loader as lm
from typing import List


class EtcdApi:
    def __init__(self, etcd_client: ecm.EtcdClientWrapper, config_loader: lm.Loader):
        """
        根据传入的 etcd_client 初始化 etcd_api
        :param etcd_client: etcd 客户端
        :param config_loader: 配置加载对象
        """
        self.etcd_client = etcd_client
        self.config_loader = config_loader

    # 卫星, 地面站, 星间链路的加载是可以预先确定的
    # --------------------------------------------------------------------------------------------

    def load_satellites(self):
        """
        从 etcd 之中加载卫星
        :return: 加载的卫星
        """
        satellites: List[sm.Satellite] = []
        pb_satellite = npb.Node()
        # 从 etcd 键值对库里拿到所有卫星信息
        satellites_in_bytes = self.etcd_client.get_prefix(self.config_loader.etcd_satellites_prefix)
        for satellite_in_bytes in satellites_in_bytes:
            pb_satellite.ParseFromString(satellite_in_bytes[0])
            satellite = sm.Satellite(node_type=pb_satellite.type,
                                     node_id=pb_satellite.id,
                                     container_name=pb_satellite.container_name,
                                     pid=pb_satellite.pid,
                                     tle=pb_satellite.tle,
                                     start_time=self.config_loader.constellation_start_time,
                                     start_gsl_ifidx=pb_satellite.ifIdx,
                                     available_gsls=self.config_loader.satellite_available_gsls)
            satellites.append(satellite)
        return satellites

    def load_ground_stations(self) -> List[gm.GroundStation]:
        """
        在初始化的时候 load_ground_stations 从 etcd 之中加载地面站
        :return: 加载的地面站列表
        """
        ground_stations: List[gm.GroundStation] = []
        pbGroundStation = npb.Node()
        # 从 etcd 键值对库里拿到所有的地面站信息
        ground_stations_in_bytes = self.etcd_client.get_prefix(self.config_loader.etcd_ground_stations_prefix)
        for ground_station_in_bytes in ground_stations_in_bytes:
            pbGroundStation.ParseFromString(ground_station_in_bytes[0])
            ground_station = gm.GroundStation(node_type=pbGroundStation.type,
                                              node_id=pbGroundStation.id,
                                              container_name=pbGroundStation.container_name,
                                              pid=pbGroundStation.pid,
                                              latitude=pbGroundStation.latitude,
                                              longitude=pbGroundStation.longitude,
                                              altitude=pbGroundStation.altitude)
            ground_stations.append(ground_station)
        return ground_stations

    def load_isls(self, satellites: List[sm.Satellite]):
        """
        进行星间链路的加载
        :param satellites 需要卫星列表才能知道链路两端连接的是什么
        :return: 加载的星间链路
        """
        inter_satellite_links = []
        pbLink = lpb.Link()
        links_in_bytes = self.etcd_client.get_prefix(self.config_loader.etcd_isls_prefix)
        for link_in_bytes in links_in_bytes:
            pbLink.ParseFromString(link_in_bytes[0])
            link = lkm.Link(pbLink.type,
                            pbLink.link_id,
                            pbLink.bandwidth,
                            satellites[pbLink.source_node_id - 1],
                            satellites[pbLink.target_node_id - 1],
                            pbLink.source_iface_name,
                            pbLink.target_iface_name)
            inter_satellite_links.append(link)
        return inter_satellite_links

    # --------------------------------------------------------------------------------------------

    # 动态更新的部分
    # --------------------------------------------------------------------------------------------
    def set_gsls(self, gsls: List[lkm.Link]):
        """
        更新 gsls
        :param gsls:
        :return:
        """
        for gsl in gsls:
            # 创建 link in protobuf
            pb_link = lpb.Link()
            pb_link.type = cm.LinkTypeGSL
            pb_link.link_id = gsl.link_type  # 这个始终为 1
            pb_link.bandwidth = gsl.bandwidth
            pb_link.source_node_id = gsl.source_node.node_id
            pb_link.target_node_id = gsl.target_node.node_id
            pb_link.source_iface_name = gsl.source_iface_name
            pb_link.target_iface_name = gsl.target_iface_name
            # 设置好 link in protobuf 之后放到 etcd 之中
            print(f"{self.config_loader.etcd_gsls_prefix}/{gsl.link_id}", flush=True)
            self.etcd_client.set(f"{self.config_loader.etcd_gsls_prefix}/{gsl.link_id}",
                                 pb_link.SerializeToString())

    def set_satellites_position_and_interface_delay(self, satellites: List[sm.Satellite]):
        """
        更新卫星的位置和延迟
        :param satellites: 卫星
        :return: None
        """
        for satellite in satellites:
            # 创建 satellite in protobuf
            pb_satellite = npb.Node()
            pb_satellite.type = satellite.node_type
            pb_satellite.id = satellite.node_id
            pb_satellite.container_name = satellite.container_name
            pb_satellite.pid = satellite.pid
            pb_satellite.tle.extend(satellite.tle)
            pb_satellite.latitude = satellite.current_position[cm.LATITUDE_KEY]
            pb_satellite.longitude = satellite.current_position[cm.LONGITUDE_KEY]
            pb_satellite.altitude = satellite.current_position[cm.ALTITUDE_KEY]
            # 构建 interface_delays
            interface_delays = []
            for interfaceName in satellite.interface_delay_map.keys():
                interface_delay = f"{interfaceName}:{satellite.interface_delay_map[interfaceName]}"
                interface_delays.append(interface_delay)
            pb_satellite.interface_delay.extend(interface_delays)
            # 设置好 satellite in protobuf 之后放到 etcd 之中
            self.etcd_client.set(f"{self.config_loader.etcd_satellites_prefix}/{satellite.node_id}",
                                 pb_satellite.SerializeToString())

    def set_ground_stations_interface_delay(self, ground_stations: List[gm.GroundStation]):
        """
        更新地面站接口的延迟
        :param ground_stations: 地面站
        :return: None
        """
        for ground_station in ground_stations:
            # 创建 ground_station in protobuf
            pb_ground_station = npb.Node()
            pb_ground_station.type = ground_station.node_type
            pb_ground_station.id = ground_station.node_id
            pb_ground_station.container_name = ground_station.container_name
            pb_ground_station.pid = ground_station.pid
            pb_ground_station.latitude = ground_station.current_position[cm.LATITUDE_KEY]  # 这个不变可以不用设置
            pb_ground_station.longitude = ground_station.current_position[cm.LONGITUDE_KEY]  # 这个不变可以不用设置
            pb_ground_station.altitude = ground_station.current_position[cm.ALTITUDE_KEY]  # 这个不变可以不用设置
            # 还有延迟没有进行设置
            # <<等待进行完善>>
            # 设置好 pbGroundStation 之后放到 etcd 之中
            self.etcd_client.set(f"{self.config_loader.etcd_ground_stations_prefix}/{ground_station.node_id}",
                                 pb_ground_station.SerializeToString())
    # --------------------------------------------------------------------------------------------
