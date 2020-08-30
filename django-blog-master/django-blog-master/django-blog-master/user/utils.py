"""
# @project : alone_blog
# @Time : 2020/1/20 19:02
# @FileName utils.py
# @Author : Alone
"""

# 发送邮件
import uuid
from django.core.mail import send_mail
from alone_blog.settings import EMAIL_HOST_USER
from user.models import UserProfile


def send_email(email, request):
    subject = '个人博客找回密码'
    # 查找email对应的用户
    user = UserProfile.objects.filter(email=email).first()
    # 产生随机码
    ran_code = uuid.uuid4()
    # 转换为字符串
    ran_code = str(ran_code)

    ran_code = ran_code.replace('-', '')
    # 将随机产生的码与用户id进行绑定
    request.session[ran_code] = user.id
    message = '''
     可爱的用户:
            <br>
            您好！此链接用户找回密码，请点击链接: <a href='http://127.0.0.1:8000/user/update_pwd?c=%s'>更新密码</a>，
            <br> 
            如果链接不能点击，请复制：<br>
            http://127.0.0.1:8000/user/update_pwd?c=%s
            
           个人博客团队
    ''' % (ran_code, ran_code)
    # 发送邮件send_mail
    result = send_mail(subject, "", EMAIL_HOST_USER, [email], html_message=message)
    return result