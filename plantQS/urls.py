"""plantQS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.views.generic import TemplateView 
from django.views.generic import RedirectView 
from plantData.views import *

urlpatterns = [ 
    url(r'^admin/', admin.site.urls),
    url(r'^plant/expert/$',expert_login),
    url(r'^plant/expert/user/(\d{1,2})/[-]?(\d{1,2})/$',expert_userQue),
    url(r'^plant/expert/user/\d{1,2}/[-]?\d{1,2}/lookpic/(\d{1,2})/$',look_pic),
    url(r'^plant/expert/user/(\d{1,2})/expInfo/$',expertLookInfo),
    url(r'^plant/expert/user/(\d{1,2})/expHist/$',expertLookHist),    
    url(r'^plant/user/$',user_login),
    url(r'^plant/user/addPhoto/(\d{1,3})/$',add_photo),
    url(r'^plant/user/addPhoto/(\d{1,3})/submit/$',add_photo_submit),
    url(r'^plant/user/lookInfo/(\d{1,3})/$',userLookInfo),
    url(r'^plant/user/lookHist/(\d{1,3})/$',userLookHist),
    url(r'^plant/user/user_register/$',TemplateView.as_view(template_name="user/user_register.html")), 
    url(r'^plant/user/user_register/regi_Info/$',user_regiInfo), 
    url(r'^plant/user/user_register/regi_Info/backLogin/$',RedirectView.as_view(url='/plant/user/')), 
    url(r'^plant/user/user_register/backLogin/$',RedirectView.as_view(url='/plant/user/')), 
    #url(r'^site_media/(?P<path>.*)','django.views.static.serve',{'document_root':'D:/plant/plants/plants/plantData/static/userPic/'}),
]
