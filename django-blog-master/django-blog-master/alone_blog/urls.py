"""alone_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.conf.urls import include
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

import xadmin
from alone_blog.settings import MEDIA_ROOT
from user.views import index

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 改写admin后台
    path('xadmin/', xadmin.site.urls),
    path('', index, name='index'),
    path('user/', include('user.urls', namespace='user')),
    path('article/', include('article.urls', namespace='article')),
    # 验证码
    re_path(r'^captcha/', include('captcha.urls')),
    # 用户头像
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 加载ckeditor的urls
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # 加载mdeditor的urls
    re_path(r'mdeditor/', include('mdeditor.urls')),
]
