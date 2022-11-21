from django.db import models
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=40)
    subscribe = models.ManyToManyField(User,related_name='cat_subscribe')

    def __str__(self):
        return self.name

    def get_show_url(self):
        url = reverse("category_details", args=[self.id])
        return url

class Tag(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    def get_show_url(self):
        url = reverse("tag_details", args=[self.id])
        return url

class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="post/images",null=True)
    body = RichTextField(null=True,blank=True)
    post_date = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,related_name='post_category')
    tag = models.ManyToManyField(Tag,null=True,related_name='post_tag' )
    likes = models.ManyToManyField(User,related_name='post_like',blank=True)
    dislikes = models.ManyToManyField(User,related_name='post_dislike',blank=True )

    def __str__(self):
        return self.title

    def get_img_url(self):
        return f"/media/{self.image}"

    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
    
    def get_show_url(self):
        url = reverse("post_details", args=[self.id])
        return url

class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return f'Comment by {self.author}'

class fWord(models.Model):
    word = models.CharField(max_length=25)

    def __str__(self):
        return self.word