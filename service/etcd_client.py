import etcd3
from config import loader as lm
from entities.link import link as lkm
from entities.protobuf.link import link_pb2 as lpb
from entities.protobuf.node import node_pb2 as npb
from entities.node import node as nm
from entities.vars import consts as cm
from typing import List


class EtcdClient:
    def __init__(self, config_loader: lm.Loader):
        """
        初始化 EtcdClient
        :param config_loader: 配置对象
        """
        # ----------------------- 初始化的属性 -----------------------
        self.config_loader = config_loader
        self.etcd_client = etcd3.client(host=config_loader.etcd_addr,
                                        port=config_loader.etcd_port)
        self.etcd_isls_prefix = config_loader.etcd_isls_prefix
        self.etcd_satellites_prefix = config_loader.etcd_satellites_prefix
        # ----------------------- 初始化的属性 -----------------------

    def load_satellites(self) -> List[nm.Node]:
        """
        load_satellites 加载卫星
        :return:
        """
        satellites = []
        pbSatellite = npb.Node()
        satellites_in_bytes = self.etcd_client.get_prefix(self.etcd_satellites_prefix)
        for satellite_in_bytes in satellites_in_bytes:
            pbSatellite.ParseFromString(satellite_in_bytes[0])
            satellite = nm.Node(pbSatellite.type,
                                pbSatellite.id,
                                pbSatellite.container_name,
                                pbSatellite.pid,
                                pbSatellite.tle,
                                self.config_loader.constellation_start_time)
            satellites.append(satellite)
        return satellites

    def load_inter_satellite_links(self, satellites: List[nm.Node]) -> List[lkm.Link]:
        """
        load_links 加载星间链路
        :return:
        """
        inter_satellite_links = []
        pbLink = lpb.Link()
        links_in_bytes = self.etcd_client.get_prefix(self.etcd_isls_prefix)
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

    def update_inter_satellite_link(self, inter_satellite_link: lkm.Link):
        """
        将链路的延迟更新到 etcd 之中
        :return:
        """
        linkPb = lpb.Link()
        linkPb.type = inter_satellite_link.link_type
        linkPb.link_id = inter_satellite_link.link_id
        linkPb.source_node_id = inter_satellite_link.source_node.node_id
        linkPb.target_node_id = inter_satellite_link.target_node.node_id
        linkPb.bandwidth = inter_satellite_link.bandwidth
        linkPb.delay = inter_satellite_link.delay_in_ms
        self.etcd_client.put(f"{self.config_loader.etcd_isls_prefix}/{inter_satellite_link.link_id}",
                             linkPb.SerializeToString())

    def update_satellite_delay_and_position(self, satellite: nm.Node):
        """
        进行节点的延迟的更新
        :return:
        """
        pbSatellite = npb.Node()
        pbSatellite.type = satellite.node_type
        pbSatellite.id = satellite.node_id
        pbSatellite.container_name = satellite.container_name
        pbSatellite.pid = satellite.pid
        pbSatellite.tle.extend(satellite.tle)
        pbSatellite.latitude = satellite.current_position[cm.LATITUDE_KEY]
        pbSatellite.longitude = satellite.current_position[cm.LONGITUDE_KEY]
        pbSatellite.altitude = satellite.current_position[cm.ALTITUDE_KEY]
        interface_delays = []
        # interface_delay_map 的 key 是接口的名称而 value 是接口的延迟
        for interfaceName in satellite.interface_delay_map.keys():
            interface_delay = f"{interfaceName}:{satellite.interface_delay_map[interfaceName]}"
            interface_delays.append(interface_delay)
        pbSatellite.interface_delay.extend(interface_delays)
        self.etcd_client.put(f"{self.config_loader.etcd_satellites_prefix}/{satellite.node_id}",
                             pbSatellite.SerializeToString())
        