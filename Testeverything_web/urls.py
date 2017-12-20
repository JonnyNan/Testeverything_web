"""Testeverything_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Testeverything import views as testeverything_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', testeverything_views.login, name='login'),
    url(r'^$', testeverything_views.index, name='index'),
    url(r'^login_action/', testeverything_views.login_action, name='login_action'),
    url(r'^accounts/login/$', testeverything_views.login),
    url(r'^logout/$', testeverything_views.logout),
    url(r'^request/$', testeverything_views.api_request),
    url(r'^upload_file/$', testeverything_views.upload_file),
    url(r'^api_test/$', testeverything_views.api_test),
    url(r'^add_api_test/$', testeverything_views.add_api_test),
    url(r'^delete_test/(\d+)/$', testeverything_views.delete_test),
    url(r'^run_api_test/(\d+)/$', testeverything_views.run_api_test),
    url(r'^show_api_result/(\d+)/(.+)/$', testeverything_views.show_api_result),

]
