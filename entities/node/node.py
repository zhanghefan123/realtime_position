import ephem
from typing import List, Dict
from datetime import datetime, timedelta
from entities.vars import consts as cm


class Node:
    def __init__(self, node_type, node_id: int, container_name: str, pid: int,
                 tle: List[str], startTime: datetime):
        """
        初始化节点
        :param node_type 节点类型
        :param node_id: 节点 id
        :param container_name: 容器名称
        :param tle: tle 两行
        """
        # ---- 由 protobuf 得到的属性 ----
        self.node_type = node_type
        self.node_id = node_id
        self.container_name = container_name
        self.pid = pid
        self.tle = tle
        self.current_time = startTime
        # ---- 由 protobuf 得到的属性 ----

        # -------- 计算得到的属性 ---------
        self.interface_delay_map: Dict[str, float] = {}
        self.mobility_module = ephem.readtle(container_name, self.tle[0], self.tle[1])
        self.current_position: Dict[str, float] = {}
        # -------- 计算得到的属性 ---------

    def update_position(self):
        """
        进行位置的更新
        :return:
        """
        self.current_time += timedelta(seconds=1)
        ephem_time = ephem.Date(self.current_time)
        self.mobility_module.compute(ephem_time)
        self.current_position = {
            cm.LATITUDE_KEY: self.mobility_module.sublat,
            cm.LONGITUDE_KEY: self.mobility_module.sublong,
            cm.ALTITUDE_KEY: self.mobility_module.elevation
        }

    def __str__(self):
        return f"node_id: {self.node_id} container_name: {self.container_name}"
