"""
# @project : alone_blog
# @Time : 2020/1/16 19:56
# @FileName urls.py
# @Author : Alone
"""
from django.urls import path

import article
from .views import *

app_name = 'article'
urlpatterns = [
    # 进入详情页
    path('detail', article_detail, name='detail'),
    # 全部博客
    path('list', list, name='list'),
    # 写博客
    path('write', write_article, name='write'),
    # 评论
    path('comment', article_comment, name='comment'),
    # 留言
    path('message', blog_message, name='message')

]
