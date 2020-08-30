"""
# @project : alone_blog
# @Time : 2020/1/23 17:51
# @FileName forms.py
# @Author : Alone
"""
from django import forms

from article.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        # 在写博客页面不显示的内容
        exclude = ['click_num', 'love_num','user']
