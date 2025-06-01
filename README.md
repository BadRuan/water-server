# 鸠江防汛水位小助手 后端部分

Python + FastApi + TDEngine
  
## 功能简介

1. 方便获取指定时间水位表；
2. api支持获取本站访问量、水位数据量；
3. 记录每次访问、下载水位表的ip地址

## Docker部署

```shell
docker build -t water-server .
docker run -itd --name=water-server -p=80:80 water-server
```
