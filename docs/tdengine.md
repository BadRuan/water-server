# TDengine

## 如何修改TDengine时区
在 Linux 下，客户端配置文件目录为 ``/etc/taos/taos.cfg``，修改 ``timezone`` 属性为 ``UTC-8``

在 Linux/macOS 中，客户端会自动读取系统设置的时区信息。用户也可以采用多种方式在配置文件设置时区。

```
timezone UTC-8
timezone GMT-8
timezone Asia/Shanghai
```
均是合法的设置东八区时区的格式。

