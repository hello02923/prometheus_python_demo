FROM python:3.8.2

RUN mkdir prometheus_python_demo
WORKDIR prometheus_python_demo

COPY . ./

RUN apt-get update -y && apt-get install cron -y \
    && apt-get install vim -y
# 改成台北時區
RUN apt-get update \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
    
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 
# 下載套件
RUN pip install -r requirements.txt
# 設權限
RUN chmod -cR 700 *

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]