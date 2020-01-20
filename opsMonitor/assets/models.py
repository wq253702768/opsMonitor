from django.db import models

# Create your models here.


class Assets(models.Model):
    env_type_choice = (
        ('dev','开发'),
        ('test','测试'),
        ('pre','预生产'),
        ('prod','生产'),
    )
    ip = models.GenericIPAddressField(verbose_name='主机IP',
                                      null=True,
                                      blank=True,
                                      unique=True,
                                      )
    username = models.CharField(verbose_name='用户名', max_length=12)
    password = models.CharField(verbose_name='登录密码',max_length=12)
    rsa_key = models.TextField(verbose_name='秘钥',null=True, blank=True)
    env = models.CharField(choices=env_type_choice, max_length=10, null=True,blank=True, verbose_name='所属环境')

    class Meta:
        verbose_name = '主机资产'
        verbose_name_plural = "主机资产"

    def __str__(self):
        return self.ip


class Component(models.Model):
    component_choice_type = (
        ('service', '后端Service'),
        ('other', '其他')
    )
    name = models.CharField(verbose_name='组件', unique=True, max_length=32)
    component_type = models.CharField(choices=component_choice_type, max_length=12,verbose_name='组件类型')
    memo = models.TextField(verbose_name='备注')

    class Meta:
        verbose_name = '组件'
        verbose_name_plural = "组件"

    def __str__(self):
        return self.name

