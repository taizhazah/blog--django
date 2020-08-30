from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db import models
from django.forms import EmailField
from captcha.fields import CaptchaField
from django import forms


class UserProfile(AbstractUser):

    tel = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    icon = models.ImageField(upload_to='uploads/%Y/%m/%d', default="/media/uploads/article/2020/01/22/TIM图片20191102092926_NfOKn2D.jpg")

    class Meta:
        db_table = 'userprofile'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class CaptchaTestForm(forms.Form):
    email = EmailField(required=True, error_messages={'required': '必须填写邮箱'}, label='邮箱')
    captcha = CaptchaField()



