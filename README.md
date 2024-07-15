# 鸠江水位小助手 WebServer

## 功能

1. 配合数据库、爬虫，构建Web服务
2. 读取数据库，生成定制水位表
3. 水位表样式可增设修改
4. 充分满足防汛需要

## 部署

```shell
docker build -t water-server:latest .
docker run -itd --name=water-server -p=80:80 --restart=always water-api:latest
```
