from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Post,Tag,Category,Comment,fWord
from mptt.admin import MPTTModelAdmin

# Register your models here.
class BlogAdmin(admin.AdminSite):
    site_header = 'Blog Admin'
    site_title = 'Blog'
    
blog_site = BlogAdmin(name='blogAdmin')


blog_site.register(Group)
blog_site.register(User)
blog_site.register(Post)
blog_site.register(Tag)
blog_site.register(Category)
blog_site.register(Comment,MPTTModelAdmin)
blog_site.register(fWord)
