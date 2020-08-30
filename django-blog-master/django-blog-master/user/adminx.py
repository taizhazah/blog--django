"""
# @project : alone_blog
# @Time : 2020/1/22 14:10
# @FileName adminx.py
# @Author : Alone
"""
import xadmin
from xadmin import views


class BaseSettings(object):
    # 是否设置主题
    enable_themes = True
    # 使用主题模板
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '博客后台管理'
    site_footer = "孙小兜"


xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
