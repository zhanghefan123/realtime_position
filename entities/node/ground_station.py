from entities.node import common_info as cim


class GroundStation(cim.CommonInfo):
    def __init__(self, node_type: int, node_id: int,
                 container_name: str, pid: int,
                 latitude: float, longitude: float, altitude: float):
        super().__init__(node_type=node_type, node_id=node_id,
                         container_name=container_name, pid=pid,
                         latitude=latitude, longitude=longitude, altitude=altitude)
        # 用来存储连接的卫星
        self.connected_satellite = None
