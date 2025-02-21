import math
from tools import tools as tm

if __name__ == "__main__":
    lat1, lon1, alt1 = 30.1/180*math.pi, 120.1/180*math.pi, 0.0  # 地面站的纬度、经度、高度
    lat2, lon2, alt2 = 30.5/180*math.pi, 120.5/180*math.pi, 500000.0  # 卫星的纬度、经度、高度
    elevation = tm.calculate_elevation_inner(lon1, lat1, lon2, lat2, alt2)
    print(f"仰角: {elevation:.2f}°")