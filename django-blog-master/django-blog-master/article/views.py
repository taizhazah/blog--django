import markdown
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from bs4 import BeautifulSoup
from article.forms import ArticleForm
from article.models import Article, Tag, Comment


# 文章详情
def article_detail(request):
    # 获取用户点击的文章对应的id
    global toc
    id = request.GET.get('id')
    # 在数据库中查询id对应的文章
    article = Article.objects.get(pk=id)
    article.content = markdown.markdown(article.content,
                                        extensions=[
                                            # 包含 缩写、表格等常用扩展
                                            'markdown.extensions.extra',
                                            # 语法高亮扩展
                                            'markdown.extensions.codehilite',
                                            # 允许我们自动生成目录
                                            'markdown.extensions.toc',
                                        ])
    soup = BeautifulSoup(article.content, "lxml")
    toc = soup.select(".toc")
    # 对下一篇的文章id进行查询，如果存在进行+1，如果不存在就按原来的
    a = Article.objects.filter(id__in=[article.id + 1])
    if a:
        art = article.id + 1
    else:
        art = article.id

    art = Article.objects.get(pk=art)
    # 点击一次，点击量增加1
    article.click_num += 1
    article.love_num += 1
    # 保存
    article.save()
    # 查询相关文章
    tags_list = article.tag.all()  # 添加（）
    list_about = []  # 存放相关文章的列表
    for tag in tags_list:
        for article in tag.article_set.all():
            # 如果文章该文章没在相关文章里面并且相关文章里面的数量不到6个。
            if article not in list_about and len(list_about) < 6:
                # 将该文章添加进去
                list_about.append(article)
    # 查询评论数
    comments = Comment.objects.filter(article_id=id)
    return render(request, 'article/info.html',
                  context={'article': article, 'list_about': list_about, 'art': art, 'comments': comments, 'toc': toc})


# 博客文章分页
def list(request):
    tags = Tag.objects.all()
    tid = request.GET.get('tid')  # None
    if tid:
        tag = Tag.objects.get(pk=tid)
        articles = Article.objects.filter(tag__name=tag.name).order_by('-date')
    else:
        articles = Article.objects.all().order_by('-date')
    # articles = Article.objects.all().order_by('-date')
    paginator = Paginator(articles, 6)  # Paginator(对象列表，每页几条记录)
    # 得到用户点击的第几页，默认为1
    page_number = request.GET.get('page', 1)
    # 得到分页后的总页码数
    page = paginator.get_page(page_number)

    return render(request, 'article/list.html', context={'page': page, 'tags': tags})


# 写博客
@login_required
def write_article(request):
    if request.method == 'GET':
        aform = ArticleForm()
        return render(request, 'article/write.html', context={'form': aform})
    else:
        aform = ArticleForm(request.POST, request.FILES)
        # 如果请求正常
        if aform.is_valid():
            # 重新获取当前时间
            data = aform.cleaned_data
            article = Article()
            article.title = data.get('title')
            article.desc = data.get('desc')
            article.content = data.get('content')

            article.image = data.get('image')
            article.desc = data.get('desc')
            article.user = request.user  # 1对多 直接赋值
            article.save()

            # 多对多 必须添加到文章保存的后面添加
            article.tag.set(data.get('tag'))
            return redirect(reverse('index'))
        return render(request, 'article/write.html', context={'form': aform})


def article_comment(request):
    # 　接收用户提交的
    nickname = request.GET.get('nickname')
    content = request.GET.get('saytext')
    aid = request.GET.get('aid')
    # 保存到数据库中
    comment = Comment.objects.create(nickname=nickname, content=content, article_id=aid)
    # 保存成功，返回1
    if comment:
        messages.success(request,'评论成功')
        data = {'status': 1}
    else:
        data = {'status': 0}
    # 向js提交上面判断返回的数据
    return JsonResponse(data)



# 留言
def blog_message(request):
    # 从数据库中拿数据
    # messages = Article.objects.all()
    comments = Comment.objects.filter()
    # # 将所有留言按3个一页进行
    # paginator = Paginator(comments, 3)
    # # 获取页码数
    # # page = request.GET.get('page', 1)
    # # 得到page对象
    # # page = paginator.get_page(page)

    if request.method == 'GET':
        return render(request, 'article/lmessage.html', context={'comments': comments})
    else:
        return render(request, 'article/lmessage.html')
