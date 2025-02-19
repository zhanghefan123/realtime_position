import math
from typing import Dict
from entities.vars import consts as cm


class CommonInfo:
    def __init__(self, node_type: int, node_id: int, container_name: str, pid: int,
                 latitude: float = None, longitude: float = None, altitude: float = None):
        self.node_type = node_type
        self.node_id = node_id
        self.container_name = container_name
        self.pid = pid
        self.interface_delay_map: Dict[str, float] = {}
        if (latitude is not None) and (longitude is not None) and (altitude is not None):
            self.current_position: Dict[str, float] = {
                cm.LATITUDE_KEY: latitude,
                cm.LONGITUDE_KEY: longitude,
                cm.ALTITUDE_KEY: altitude
            }
        else:
            self.current_position: Dict[str, float] = {}
