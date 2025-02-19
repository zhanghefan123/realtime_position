import ephem
from typing import List
from entities.node import common_info as cim
from datetime import datetime, timedelta
from entities.vars import consts as cm


class Satellite(cim.CommonInfo):
    def __init__(self, node_type: int, node_id: int,
                 container_name: str, pid: int,
                 tle: List[str], start_time: datetime):
        super().__init__(node_type=node_type, node_id=node_id, container_name=container_name, pid=pid)
        self.tle = tle
        self.start_time = start_time
        self.mobility_module = ephem.readtle(container_name, self.tle[0], self.tle[1])

    def update_position(self):
        """
        进行位置的更新
        :return:
        """
        self.start_time += timedelta(seconds=1)
        ephem_time = ephem.Date(self.start_time)
        self.mobility_module.compute(ephem_time)
        self.current_position = {
            cm.LATITUDE_KEY: self.mobility_module.sublat,
            cm.LONGITUDE_KEY: self.mobility_module.sublong,
            cm.ALTITUDE_KEY: self.mobility_module.elevation
        }
