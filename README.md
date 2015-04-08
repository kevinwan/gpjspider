Gongpingjia Spider System
============================

Gongpingjia Spider System, is called `GSS` or `gss` for short.

**Please don't run scrapy directly.**

## Deploy ##

1. if show 'mysql_config not found', please install `libmysqlclient-dev`. 
```
sudo apt-get install libmysqlclient-dev
```
2. To resolve the error "error: libxml/xmlversion.h: No such file or directory", run the command:
```
sudo apt-get install libxml2-dev libxslt-dev
sudo apt-get install python-lxml
```
3. To resolve the error: "fatal error: ffi.h: 没有那个文件或目录", run the command:
```
sudo apt-get install libffi-dev
```
4. To resolve the error: "fatal error: openssl/aes.h: 没有那个文件或目录", run the command:
```
sudo apt-get install libssl-dev
```
5. install `supervisor`, run the command:
```
sudo apt-get install supervisor
```
6. install `redis`, run the command:
```
sudo apt-get install redis-server
```

To deploy `gss`, run the command:
```
fab deploy
```
If not installed fabric, run `pip install fabric`, then run the above command.


## Run ##

## Directory ##
- `bin`           各种命令，目前为空
- `deplay`        部署用的配置等，被 fabfile.py 使用
- `docs`          文档，restructtext 格式，可以用 sphinx 生成 html、PDF 格式
- `gpjspider`     主要代码目录
- `tools`         一些工具脚本
- `.gitignore`    git 文件
- `fabfile.py`    部署工具
- `scrapy.cfg`   项目文件

## Architecture ##
