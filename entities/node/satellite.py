import ephem
from typing import List, Dict
from entities.node import common_info as cim
from datetime import datetime, timedelta
from entities.vars import consts as cm


class GslIfIndexes:
    def __init__(self, start_gsl_ifidx: int, available_gsls: int):
        self.start_gsl_ifidx = start_gsl_ifidx
        self.available_gsls = available_gsls
        self.gsl_ifidx_mapping: Dict[int, bool] = {}
        self.set_gsl_ifidx_mapping()

    def set_gsl_ifidx_mapping(self):
        for index in range(self.available_gsls):
            self.gsl_ifidx_mapping[self.start_gsl_ifidx + index] = True

    def find_available_gsl_ifidx(self):
        """
        找到可用的 gsl ifidx
        """
        for ifidx, is_available in self.gsl_ifidx_mapping.items():
            if is_available:
                return ifidx
        return None

    def use_gsl_ifidx(self, ifidx: int):
        """
        使用 gsl ifidx
        """
        self.gsl_ifidx_mapping[ifidx] = False

    def release_gsl_ifidx(self, ifidx: int):
        """
        释放 gsl ifidx
        """
        self.gsl_ifidx_mapping[ifidx] = True


class Satellite(cim.CommonInfo):
    def __init__(self, node_type: int, node_id: int,
                 container_name: str, pid: int,
                 tle: List[str], start_time: datetime,
                 start_gsl_ifidx: int, available_gsls: int):
        """
        进行卫星的初始化
        :param node_type:  卫星的类型
        :param node_id:  卫星的 id
        :param container_name:  容器的名称
        :param pid:  卫星的 pid
        :param tle:  卫星的轨道参数
        :param start_time: 卫星的启动时间
        :param start_gsl_ifidx: 起始的 gsl 索引
        :param available_gsls: 可用的 gsl 数量
        """
        super().__init__(node_type=node_type, node_id=node_id, container_name=container_name, pid=pid)
        self.tle = tle
        self.start_time = start_time
        self.mobility_module = ephem.readtle(container_name, self.tle[0], self.tle[1])
        self.gsl_ifindexes = GslIfIndexes(start_gsl_ifidx=start_gsl_ifidx, available_gsls=available_gsls)

    def update_position(self, time_step: int):
        """
        进行位置的更新
        :param time_step: 时间步长
        """
        self.start_time += timedelta(seconds=time_step)
        ephem_time = ephem.Date(self.start_time)
        self.mobility_module.compute(ephem_time)
        self.current_position = {
            cm.LATITUDE_KEY: self.mobility_module.sublat,
            cm.LONGITUDE_KEY: self.mobility_module.sublong,
            cm.ALTITUDE_KEY: self.mobility_module.elevation
        }
