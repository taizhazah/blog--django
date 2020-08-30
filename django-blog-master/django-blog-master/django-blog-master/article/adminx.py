"""
# @project : alone_blog
# @Time : 2020/1/22 14:10
# @FileName adminx.py
# @Author : Alone
"""
import xadmin
from article.models import Article, Tag


class ArticleAdmin(object):
    # 预览时后台显示每条博客的哪些信息
    list_display = ['title', 'click_num', 'love_num', 'user']
    # 支持搜索的东西
    search_fields= ['title','id']
    # 可以实时编辑的
    list_editable= ['click_num','love_num']
    # 根据什么进行检索，即过滤器
    list_filter=['date','user']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Tag)