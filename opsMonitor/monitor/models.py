from django.db import models
from assets.models import Assets, Component
# Create your models here.


class MonitorTools(models.Model):
    send_tools_choice = (
        ('dingding','钉钉'),
        ('email','邮箱'),
    )
    name = models.CharField(verbose_name='名称',max_length=10)
    tool_name = models.CharField(choices=send_tools_choice, verbose_name='工具名称', max_length=10, default='dingding')
    tool_url = models.TextField(verbose_name='工具地址')

    class Meta:
        verbose_name = '监控工具'
        verbose_name_plural = "监控工具"


    def __str__(self):
        return self.name


class MonitorTemplates(models.Model):
    name = models.CharField(verbose_name='监控模板名称', max_length=64)
    m_time = models.IntegerField(verbose_name='监控触发时间间隔',default=30)
    send_tools = models.ForeignKey(MonitorTools, verbose_name='发送工具', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '监控模板'
        verbose_name_plural = "监控模板"

    def __str__(self):
        return self.name


class ComponentsAssets(models.Model):
    env_type_choice = (
        ('dev','开发'),
        ('test','测试'),
        ('pre','预生产'),
        ('prod','生产'),
    )

    component = models.ForeignKey(Component,verbose_name='组件', on_delete=models.CASCADE)
    env = models.CharField(choices=env_type_choice, max_length=10, null=True, blank=True, verbose_name='所属环境')
    assets = models.ManyToManyField(Assets, related_name='assets_comp', verbose_name='主机')
    monitor_interface = models.TextField(verbose_name='监控接口地址', null=True, blank=True)
    http_port = models.IntegerField(verbose_name='启动端口')
    m_template = models.ForeignKey(MonitorTemplates, verbose_name='监控模板', on_delete=models.CASCADE)
    is_monitor = models.BooleanField(verbose_name='是否监控', default=False)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '组件事件'
        verbose_name_plural = "组件事件"
        ordering = ['-c_time']

    def __str__(self):
        return "%s-%s" % (self.env, self.component)


class MonitorTask(models.Model):
    send_status_choice = (
        ('y','发送成功'),
        ('n','发送失败'),
    )
    env_type_choice = (
        ('dev','开发'),
        ('test','测试'),
        ('pre','预生产'),
        ('prod','生产'),
    )
    env = models.CharField(choices=env_type_choice, verbose_name='环境',max_length=12)
    components_assets = models.ForeignKey(ComponentsAssets, on_delete=models.CASCADE)
    components_host = models.CharField(verbose_name='告警主机', max_length=100, null=True,blank=True)
    send_tool_templates = models.ForeignKey(MonitorTemplates, verbose_name='发送模板', on_delete=models.CASCADE)
    send_status = models.CharField(choices=send_status_choice, null=True, blank=True,verbose_name='发送状态', max_length=4)
    send_context = models.TextField(verbose_name='发送内容')
    redis_key = models.CharField(verbose_name='redis_key',max_length=200)
    recover_status = models.BooleanField(verbose_name='是否恢复', default=False)
    c_time = models.DateTimeField(verbose_name='报警时间', auto_now_add=True)
    u_time = models.DateTimeField(verbose_name='恢复时间',auto_now=True)

    class Meta:
        verbose_name = '监控结果'
        verbose_name_plural = "监控结果"
        ordering = ['-c_time']