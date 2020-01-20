# Generated by Django 3.0.2 on 2020-01-09 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorTemplates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='监控模板名称')),
                ('m_time', models.IntegerField(default=30, verbose_name='监控触发时间间隔')),
            ],
        ),
        migrations.CreateModel(
            name='ComponentsAssets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('env', models.CharField(blank=True, choices=[('dev', '开发'), ('test', '测试'), ('pre', '预生产'), ('prod', '生产')], max_length=10, null=True, verbose_name='所属环境')),
                ('monitor_interface', models.TextField(verbose_name='监控接口地址')),
                ('http_port', models.IntegerField(verbose_name='启动端口')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('assets', models.ManyToManyField(related_name='assets_comp', to='assets.Assets', verbose_name='主机')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Component', verbose_name='组件')),
                ('m_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.MonitorTemplates', verbose_name='监控模板')),
            ],
        ),
    ]
