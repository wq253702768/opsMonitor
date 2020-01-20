# -*- coding:utf-8 -*-
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from monitor.api.templates.check_http_api import CheckHttpInterface
from monitor.models import ComponentsAssets, MonitorTask
from monitor.api.tools.dingding import DingdingAPI
from monitor.api.tools.redis import RedisApi
from monitor.utils import get_models_obj
import datetime
import uuid
import json


@shared_task
def check_http_api():
    '''
    如果监控设置为True,即is_monitor=1,为开始监控
    :return:
    '''
    monitor_event_obj = ComponentsAssets.objects.filter(is_monitor=1)
    for i in monitor_event_obj:
        for asset in i.assets.all():
            print (asset.ip)
            result = CheckHttpInterface(http_host=asset.ip,port=i.http_port,interface=i.monitor_interface).run()
            if not result.get('result'):
                message = '【菜小秘监控】【告警通知】【%s】【%s】，信息如下:\n告警时间: %s,\n告警模块: %s\n告警主机: %s\n告警端口: %s\n告警接口: %s\n告警message: \n\t%s' % (i.get_env_display() ,i.m_template.name,datetime.datetime.now(), i.component, asset.ip, i.http_port, i.monitor_interface,result.get('message'))
                dingding_status = DingdingAPI(i.m_template.send_tools.tool_url, message=message).run()
                print ('dadasdsadsadsa',dingding_status)
                if dingding_status.get('errmsg') in ["ok"]:

                    send_status = 'y'
                else:
                    send_status = 'n'
                # set redis key value
                key = "%s-%s-%s-%s" % (i.env, i.component,asset.ip, i.http_port)
                value = {
                    'env': i.env,
                    'component': i.component.name,
                    'send_tool_templates': i.m_template.name,
                    'send_url': i.m_template.send_tools.tool_url,
                    'host': asset.ip,
                    'http_port': i.http_port,
                    'interface': i.monitor_interface,
                    'uuid_lable': key
                }

                RedisApi().set_redis(key,value)
                # print ( i.m_template.id, i.id, i.get_env_display(), send_status, message, uuid.uuid1())
                # 插入数据
                # 检查数据是否存在，且是否已恢复
                filter_model = MonitorTask.objects.filter(env=i.get_env_display(), components_assets_id=i.id, components_host=asset.ip)
                if filter_model:
                    print (filter_model[0].recover_status)
                    if filter_model[0].recover_status:
                        print ("create")
                        MonitorTask.objects.create(
                            send_tool_templates_id = i.m_template.id,
                            components_assets_id = i.id,
                            env = i.env,
                            send_status = send_status,
                            send_context = message,
                            redis_key = key,
                            components_host = asset.ip,
                        )
                else:
                    MonitorTask.objects.create(
                        send_tool_templates_id=i.m_template.id,
                        components_assets_id=i.id,
                        env=i.env,
                        send_status=send_status,
                        send_context=message,
                        redis_key=key,
                        components_host=asset.ip,
                    )

    return '正在监控中的项有: [%s]' % len(monitor_event_obj)


@shared_task
def check_monitor_status():
    '''
    获取redis中db 5中所有的key,即服务报警的时候会将key插入到redis db5中;
    将key和value信息拿到，并通过CheckHttpInterface，再次检测，若服务恢复，即更新monitor_task表中的recover_status字段，表示已经恢复
    :return:
    '''
    # 获取所有的key
    keys = RedisApi().get_all_keys()
    if len(keys) > 0:
        for key in keys:
            #获取对应的value
            value = eval(RedisApi().get_redis(key=key))
            print ('adadsadasd:%s' % value)
            # print (json.loads(value))
            #再次检测http接口UUID
            result = CheckHttpInterface(http_host=value.get('host'),port=value.get('http_port'),interface=value.get('interface')).run()
            print ('monitor_status',result)
            if result.get('result'):
                MonitorTask.objects.filter(redis_key=key).update(recover_status=True)
                RedisApi().del_redis(key)
                message = '【菜小秘监控】【告警恢复通知】【%s】【%s】，信息如下:\n告警时间: %s,\n告警模块: %s\n告警主机: %s\n告警端口: %s\n告警接口: %s\n恢复信息: %s' % (
                    value.get("env"),
                    value.get("send_tool_templates"),
                    datetime.datetime.now(),
                    value.get('component'),
                    value.get('host'),
                    value.get('http_port'),
                    value.get("interface"),
                    result.get('message')
                )
                try:
                    dingding_status = DingdingAPI(value.get('send_url'), message=message).run()
                    if not dingding_status.get('errmsg') in ["ok"]:
                        send_status = 'n'
                        MonitorTask.objects.filter(uuid_lable=key).update(send_status=send_status)
                except Exception as e:
                    print ('钉钉故障恢复检测钉钉发送失败!!!')
    return "目前故障报警为: [%s]" % len(keys)
