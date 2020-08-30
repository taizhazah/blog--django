"""
# @project : alone_blog
# @Time : 2020/1/16 19:56
# @FileName urls.py
# @Author : Alone
"""
from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    # 注册
    path('register', register, name='register'),
    # 登录
    path('login', Login, name='login'),
    # 注销
    path('logout', Logout, name='logout'),
    # 找回密码
    path('forget_pwd', forget_password, name='forget_pwd'),
    # 定义一个路由验证验证码
    path('valide_code', valide_code, name='valide_code'),
    # 更新密码
    path('update_pw', update_pwd, name='update_pwd'),
    # 个人用户
    path('center', center, name='center'),
]
