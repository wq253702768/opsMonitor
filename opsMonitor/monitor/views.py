from django.shortcuts import render
from .models import ComponentsAssets, MonitorTask
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.


@login_required
def monitor_items(request):
    title1, title2, title3 = '监控事件管理', 'Items', '所有监控的Items事件'
    monitor_itmes_obj = ComponentsAssets.objects.all()
    return render(request,'monitor/items.html',locals())


@login_required
def alerts_items(request):
    title1, title2, title3 = '监控告警管理', 'Alerts', '所有监控告警'
    monitor_alerts_obj = MonitorTask.objects.all()
    return render(request,'monitor/alerts.html',locals())


@login_required
def alerts_detail(request, alert_id):
    title1, title2, title3 = '监控告警管理', 'Alerts detail', '告警详情'
    monitor_alerts_detail_obj = MonitorTask.objects.filter(id=alert_id)
    return render(request,'monitor/alerts_detail.html',locals())

@login_required
def alerts_flower(request):
    title1, title2, title3 = 'Celery进程监控', 'Flowers', 'Celery进程监控'
    url = settings.FLOWER_URL
    return render(request, 'monitor/flower.html', locals())
