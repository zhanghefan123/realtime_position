FROM python_env:latest

LABEL maintainer="HeFan ZHANG"

# 进行本文件夹内容的拷贝
COPY . ./realtime_position/

# 进行其他的镜像源的设置
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 进行到存在 requirements.txt 的目录并且执行 python 依赖的安装
RUN cd ./realtime_position/ && python -m pip install -r requirements.txt --verbose

# 入口函数
ENTRYPOINT ["python", "/realtime_position/main.py"]