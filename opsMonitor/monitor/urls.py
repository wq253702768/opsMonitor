"""opsMonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import monitor_items, alerts_items,alerts_flower,alerts_detail

urlpatterns = [
    path('items/',monitor_items, name='monitor_itmes_url'),
    path('alerts/', alerts_items, name='monitor_alerts_url'),
    path('alerts_detail/<int:alert_id>', alerts_detail, name='monitor_alerts_detail_url'),
    path('flower/', alerts_flower, name='monitor_flower_url')
]
