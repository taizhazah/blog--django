# django-blog
django个人博客项目
django个人博客项目  
环境：django2.0  
           python3.6.0  
功能：注册、登录、找回密码  
           个人中心  
          写博客（支持markdown语法）、预览博客（自动生成博客目录）  
          留言、评论功能  
使用：将settings里面的数据库更换为自己的数据库账号和database  
      python manage.py makemigrations  
      python manage.py migrate  
      进行生成、迁移数据库  
      pip install -r requirements.txt  
      pip install -r r.txt  
      分别安装项目依赖包，和xadmin的依赖包  
      然后python manage.py runserver就可以在本地端口看到博客页面  
