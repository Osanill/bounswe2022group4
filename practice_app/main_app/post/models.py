from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

item_list=[]
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    location = models.CharField(default='not specified', max_length=100)
    date = models.DateTimeField(default=timezone.now)   # the date and time when the post is created.
    author = models.ForeignKey(User, on_delete=models.CASCADE) # if the user is deleted,their post will also be deleted.

    likes = models.ManyToManyField(User, related_name="blog_post")
    category = models.CharField(max_length=50, choices=item_list, default="General")#########33

    dislikes = models.ManyToManyField(User, related_name="blog_post_dislike")

    @property
    def total_likes(self):
        return self.likes.count()
    
    @property
    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

class Category(models.Model):
    post = models.ForeignKey(Post, related_name="categories", on_delete=models.DO_NOTHING)

    name = models.CharField(max_length=100,default='General')
    description = models.CharField(max_length=300,default="")
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-posts')

class Category(models.Model):
    post = models.ForeignKey(Post, related_name="categories", on_delete=models.DO_NOTHING,default=100)

    name = models.CharField(max_length=100,default='General')
    description = models.CharField(max_length=300,default="")
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-posts')

CHOICES = Category.objects.all().values_list('name','name')
#########33



for  item in CHOICES:
    item_list.append(item)



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)   # the date and time when the post is created.
    author = models.ForeignKey(User, on_delete=models.CASCADE) # if the user is deleted,their post will also be deleted.
    def __str__(self):
        return '%s - %s - %s - %s' % (self.title, self.content, self.date, self.author)
    def get_absolute_url(self):
        return reverse('home-page')