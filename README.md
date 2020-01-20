# opsMonitor
端口监控和Http接口地址监控

## 1、背景介绍
```
需要对线上业务的组件进行监控，直接对每个服务的http接口进行监控，防止进程假死，造成服务伪健康状态

```

## 2、部署安装
2.1 安装环境
  
```
  python3.6 + django2.2.0 + celery + django-celery=3.3.1 + redis (具体版本查看requirements.txt)
  
```       
2.2 安装python3.6环境 
    
```
    tar -zxvf Python-3.6.8.tgz && cd Python-3.6.8 && ./configure --prefix=/usr/local/python26 && make && make install
    
```
2.3 创建venv虚拟环境
   
 ```
   python3.6 -m venv /home/ops/py3 
 
 ```      
>  注：/home/ops/py3/ 为虚拟python环境路径，可以保证跟系统py环境不冲突


2.4 执行以下命令，进入虚拟py环境
  
    ```
    source /home/ops/py3/bin/active
    ```
    
2.5 安装插件
    
      ```
      pip install -r requirements.txt
      
      ```
2.6 创建数据库和权限
        ```
        
        CREATE DATABASE IF NOT EXISTS opsmonitor  DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
        
        GRANT ALL PRIVILEGES ON *.* TO 'cxm'@'%' IDENTIFIED BY 'Cxm@2019' WITH GRANT OPTION;
        flush privileges;
        ```   
2.7 安装redis
    ```
    yum install -y redis*
    
    ```
2.8 项目配置(/home/ops/opsMonitor/opsMonitor的setting.py文件里面配置)
   
```
    #数据库配置mysql:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'opsmonitor', #连接数据库
        'USER': 'cxm',  #连接用户
        'PASSWORD': 'Cxm@2019', #连接密码
        'HOST': '172.19.95.227', #连接地址
        'PORT': '3306', #连接端口
    }
}

#redis配置

#celery
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://172.19.95.227:6379/11'
CELERY_IMPORTS = ('monitor.tasks', )
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_BACKEND = 'redis://172.19.95.227:6379/12'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


#redis queue(作为监控故障队列推送数据)
REDIS_URL = '172.19.95.227'
REDIS_PORT = 6379
REDIS_DB = 13

```

## 3、开始同步数据库

```
cd /home/ops/opsMonitor &&  /home/ops/py3/bin/python manage.py makemigrations &&   /home/ops/py3/bin/python manage.py migrate

``` 

## 4、通过supervisord管理celery进程服务
> 注：以下操作切到py3的虚拟环境变量 source /home/ops/py3/bin/active
4.1 安装 supervisord
```
pip install supervisor
```
4.2 生成配置文件
```
echo_supervisord_conf > /etc/supervisord.conf

#修改配置文件：
vim /etc/supervisord.conf
#最下面两行注释去掉

[include]
files = supervisord.d/*.conf

```
4.3 创建配置目录和配置文件

```
在/etc/下创建supervisord.d文件夹存放配置文件

cd /etc/supervisord.d

#celery_beat.conf
[program:celery-beat]
command=/home/ops/py3/bin/python /home/ops/opsMonitor/manage.py celery beat
autostart=true
autorestart=true
user=root
numprocs=1
redirect_stderr=true
stdout_logfile=/home/ops/opsMonitor/logs/celery_beat.log


#celery_worker.conf
[program: celery-worker]
command=/home/ops/py3/bin/celery -A opsMonitor worker -c 3 -l info 
directory=/home/ops/opsMonitor/
autorestart=true
autostart=true
numprocs=1
stderr_logfile=/home/ops/opsMonitor/logs/celery_work.err.log
stdout_logfile=/home/ops/opsMonitor/logs/celery_work.out.log
user=root
stopsignal=INT
startsecs=1

#runserver.conf
[program:runserver]
command=/home/ops/py3/bin/python /home/ops/opsMonitor/manage.py runserver 172.19.95.227:8000
autostart=true
autorestart=true
user=root
numprocs=1
redirect_stderr=true
stdout_logfile=//home/ops/opsMonitor/logs/runserver.log
```

4.4 启动supervisord服务
```
/home/ops/py3/bin/python3.6 /home/ops/py3/bin/supervisord -c /etc/supervisord.conf

```

## 5、平台信息
```
前台地址登录地址：http://monitor.ops.caixm.cn/login

后台登录地址：http://monitor.ops.caixm.cn/admin

用户名和密码:admin/wenqi19891017

```

## 6、安装报错如下：
```
  File "C:\Users\zlhwu\PycharmProjects\ops-monitor\venv\lib\site-packages\django\db\backends\mysql\base.py", line 36, in <module>
    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.

解决方案：

打开编辑 C:\Users\zlhwu\PycharmProjects\ops-monitor\venv\lib\site-packages\django\db\backends\mysql\base.py，注释如下几行：
#if version < (1, 3, 13):
 #   raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
 
```
```
  File "C:\Users\zlhwu\PycharmProjects\ops-monitor\venv\lib\site-packages\django\db\backends\mysql\operations.py", line 146, in last_executed_query
    query = query.decode(errors='replace')
AttributeError: 'str' object has no attribute 'decode'

解决办法：打开上面的文件operations.py，在146行修改如下
 query = query.decode(errors='replace') 修改为 query = query.encode('utf-8').decode(errors='replace')

```
