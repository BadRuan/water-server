# 水位数据 API 服务

## 项目技术栈
- 基础语言: [Python](https://www.python.org/)
- 框架：[FastAPI](https://fastapi.tiangolo.com/zh/)
- 数据库: [TDEngine](https://docs.taosdata.com/)
- 环境部署: [Docker](https://www.docker.com/)


## 开发进展
1. 提供TDengine数据库中最新的水位数据API
2. 提供三线水位数据，含最新水位数据API


## 后续开发计划
1. Dockerfile编写，方便部署


## Docker 部署
```shell
docker build -t water_api:v1 .
docker run -itd --name=water-api -p 9000:8000 --restart=always water_api:v1
```
