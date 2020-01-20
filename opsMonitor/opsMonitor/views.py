#coding: utf-8
from django.shortcuts import render,redirect,reverse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,Group
from django.contrib.sessions.models import Session
from monitor.models import ComponentsAssets,MonitorTask, MonitorTemplates
from assets.models import Component
from monitor.api.tools.redis import RedisApi
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from monitor.utils import *
import datetime
import calendar
import json

@csrf_exempt
def login_view(request):
    error = ''
    if request.method == 'GET':
        return render(request, 'login.html', locals())
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print (username,password)
        if username and password:
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index_url'))
                else:
                    error = '用户未激活'
            else:
                error = '用户名或密码错误'
        else:
            error='用户名或密码错误'
    return render(request,'login.html',{'error': error})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login_url"))


@login_required
def index(request):
    # 所有用户数
    user_total = User.objects.all()
    # echarts 默认显示本月的数据
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    current_day = datetime.datetime.now().day
    # print(current_day,type(current_day))
    month_day_num = calendar.monthrange(year, month)[1]
    # print (month_day_num, year, month)

# 本月天数列表
    day_range_list = [d for d in range(1,month_day_num+1)]
# 本月告警数据
    #对应的环境
    env_list = []
    for i in ComponentsAssets.objects.all():
        if i.env not in env_list:
            env_list.append(i.env)

    #告警数据
    result = {}
    for env in env_list:
        result[env] = {}
        # 根据env和componentsAsset来获得componentsAsset.id
        for component in Component.objects.all():
            if component.name not in result[env].keys():
                try:
                    # 判断是否在监控中
                    monitor_true_component_assets = ComponentsAssets.objects.filter(component_id = component.id, env=env, is_monitor=1)
                    if monitor_true_component_assets:
                        monitor_asset_id = ComponentsAssets.objects.get(component_id = component.id, env=env, is_monitor=1).id
                        result[env][component.name] = {}
                        result[env][component.name]['result'] = []
                        for day in day_range_list:
                            # print (year, month, day, env, component.id)
                            range_alert_data = MonitorTask.objects.filter(env=env,components_assets_id=monitor_asset_id ,c_time__year=year, c_time__month=month, c_time__day=day)
                            # print ('rest',range_alert_data)
                            if range_alert_data:
                                # print("appned 0")
                                # result[env][component.name].append(0)
                                result[env][component.name]['result'].append(0)
                            else:
                                if day <= current_day:
                                    # print ("append 1")
                                    # result[env][component.name].append(1)
                                    result[env][component.name]['result'].append(1)
                            # print ('over')

                        try:
                            result_per = get_list_percent(result[env][component.name]['result'], 1)
                            # print({'env': env, 'components':component.name,'result_list': result[env][component.name], 'result': result_per})
                            result[env][component.name]['result_per'] = result_per
                        except Exception as e:
                            print ('exception', e)
                except Exception as e:
                    print ('[%s]环境没有[%s]监控，请检查!!!: %s ' % (env, component.name, e))


    # print (result)
    js_result = json.dumps(result)
    print ('dada',js_result)

    # 监控所有的event条数
    monitor_assets_total = ComponentsAssets.objects.all()
    # 所有正在监控的条数
    monitor_assets_true = ComponentsAssets.objects.filter(is_monitor=1)

    # 监控告警的总条数
    monitor_alert_total = MonitorTask.objects.all()

    # 当天天告警数据
    day_data_dict = {}
    print (year, month, current_day)
    monitor_alert = MonitorTask.objects.filter(c_time__year=year, c_time__month=month)
    print (monitor_alert)
    day = "{}.{}.{}".format(year, month, current_day)
    if day not in day_data_dict.keys():
        day_data_dict[day] = []
    if monitor_alert:
        #读取最近5条
        #获取时差

        for i in monitor_alert.values_list()[0:5]:
            time_lag = str(datetime.datetime.now() - i[9]).split('.')[0]
            time_lag = process_time_data(time_lag)
            i = list(i)
            i.append(time_lag) #取值秒开始
            day_data_dict[day].append(i)
    print (day_data_dict)

    # 未处理的监控条目
    no_process_monitor = RedisApi().get_all_keys()
    return render(request, 'index.html', locals())


def test_url(request):
    return render(request, 'test.html', locals())
