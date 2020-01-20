from django.contrib import admin
from monitor import models


# Register your models here.

class MonitorToolsAdmin(admin.ModelAdmin):
    list_display = ['name', 'tool_url']


class MonitorTemplatesAdmin(admin.ModelAdmin):
    list_display = ['name', 'm_time', 'send_tools']


class ComponentsAssetsAdmin(admin.ModelAdmin):
    list_display = ['component', 'env','monitor_interface','http_port','m_template','is_monitor','c_time']


class MonitorTaskAdmin(admin.ModelAdmin):
    list_display = ['env','send_tool_templates', 'send_status', 'send_context','recover_status','c_time', 'u_time']


admin.site.register(models.MonitorTools, MonitorToolsAdmin)
admin.site.register(models.MonitorTemplates, MonitorTemplatesAdmin)
admin.site.register(models.ComponentsAssets, ComponentsAssetsAdmin)
admin.site.register(models.MonitorTask, MonitorTaskAdmin)
