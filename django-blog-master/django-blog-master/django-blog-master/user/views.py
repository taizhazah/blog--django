from captcha.models import CaptchaStore
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages  # 导入消息闪现

from article.models import Article, Tag
from user.models import *
# Create your views here.

# 首页
from user.utils import send_email


def index(request):
    # 获取用户模型，用来取用户的个人头像
    user = request.user
    # 用来获取标签
    tags = Tag.objects.all()
    # 按照点击量进行降序排列
    c_articles = Article.objects.all().order_by('-click_num')[:6]
    # 按日期进行降序排列,显示前6条
    d_articles = Article.objects.all().order_by('-date')[:6]
    return render(request, 'index.html', context={'c_articles': c_articles,'d_articles': d_articles, 'user': user, 'tags': tags})


# 注册
def register(request):
    if request.method == 'POST':
        # 接受表单传过来的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        # 与数据库中的数据进行对比，如果用户名和邮箱都不重复，则进入下一步
        if not UserProfile.objects.filter(Q(username=username) | Q(email=email)):
            password = make_password(password)  # 密码加密
            # 保存到django的用户表中，返回一个bool类型的值，保存成功，返回True
            a = UserProfile.objects.create(username=username, password=password, email=email, tel=tel)
            if a:
                # 消息闪现，弹窗
                messages.success(request,'恭喜你，注册成功，请立刻前往登录！')
                # 跳转到登录页面
                return render(request, 'user/login.html')

        else:
            return render(request, 'user/register.html', context={'msg': '用户名或邮箱已经存在！'})
    return render(request, 'user/register.html')


# 登录
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        # 认证成功返回对象 否则None
        if user:
            # 处理登录状态的维持
            login(request,user)
            messages.success(request, '登录成功')
            # 重定向到首页
            return redirect(reverse('index'))
        else:
            return render(request, 'user/login.html', context={'msg': '请输入正确的用户名和密码'})
    return render(request, 'user/login.html')


# 退出登陆
def Logout(request):
    logout(request)
    return redirect(reverse('index'))


# 忘记密码
def forget_password(request):
    if request.method == 'GET':
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})
    else:
        # 获取提交的邮箱，发送邮件，通过发送的邮箱链接设置新的密码
        email = request.POST.get('email')
        # 给此邮箱地址发送邮件
        result = send_email(email, request)
        if result:
            return HttpResponse("邮件发送成功！赶快去邮箱更改密码！<a href='/'>返回首页>>> </a>")


# 定义一个路由验证验证码
def valide_code(request):
    if request.is_ajax():
        # 每个验证码在数据库中对有对应的hasKey
        key = request.GET.get('key')
        code = request.GET.get('code')
        # 与数据库中的haskey进行对比
        captche = CaptchaStore.objects.filter(hashkey=key).first()
        # 再将对比所得的验证码统一转换为小写，然后再判断我们输入的验证码
        if captche.response == code.lower():
            # 正确
            data = {'status': 1}
        else:
            # 错误的
            data = {'status': 0}
        return JsonResponse(data)


# 更新密码
def update_pwd(request):
    if request.method == 'GET':
        # 通过修改密码的邮件的url的参数拿到随机码
        c = request.GET.get('c')
        return render(request, 'user/update_pwd.html', context={'c': c})
    else:
        # 接收前端传递过来的随机码
        code = request.POST.get('code')
        # 通过session拿到用户id
        uid = request.session.get(code)
        # 通过用户id查询该用户
        user = UserProfile.objects.get(pk=uid)
        # 获取密码
        pwd = request.POST.get('password')

        if user:
            # 对获取的新密码进行加密
            pwd = make_password(pwd)
            # 与原密码进行替换
            user.password = pwd
            # 保存
            user.save()
            # 进行消息闪现提示
            messages.success(request, '用户密码更新成功！')
            return render(request, 'user/login.html')
        else:
            return render(request, 'user/update_pwd.html', context={'msg': '更新失败！'})


@login_required
def center(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'user/center.html', context={'user': user})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        icon = request.FILES.get('icon')
        # 更新用户
        user.username = username
        user.email = email
        user.tel = tel
        user.icon = icon
        # 获取图片后缀
        suffix = user.icon.name.split('.')[-1]

        if suffix not in settings.ALLOWED_FILES:
            return render(request, 'user/center.html', context={'msg': '该文件类型不允许上传，可上传格式.img .jpg .png'})
        else:
            user.save()
            return render(request, 'user/center.html', context={'user': user})