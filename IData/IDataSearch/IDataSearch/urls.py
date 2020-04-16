"""IDataSearch URL Configuration

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
from django.urls import path, include
from rest_framework import routers

from django.conf.urls import url
from backdoor import views
from backdoor.views import MessageViewSet, ExtractorViewset, RecommedViewset, SimplesearchViewset

router = routers.DefaultRouter()
router.register('messages', MessageViewSet)
router.register('extractors', ExtractorViewset)
router.register('recommends', RecommedViewset)
router.register('simplesearch', SimplesearchViewset)


app_name = 'backdoor'

urlpatterns = [

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    url('api/extract/', views.extract),

    url('api/recommend/', views.recommend),

    url('api/startspider/', views.startspider),

    # url('api/rawresult/', views.rawresult),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),
]