'''Файл моделей'''
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.core.mail import send_mail

class Blogs(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key = True)
    name_blog = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        data = super(Posts, self).save(*args, **kwargs)
        user_lst = User.objects.all()
        for user_p in user_lst:
            blog_user = BlogUser(user = user_p, blog = self, signed = False)
            blog_user.save()

    def __str__(self):
        return f"{self.name_blog}"

class Posts(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.PROTECT)
    title_post = models.CharField(max_length=140)
    text_post = models.TextField(null=True, blank=True)
    date_time_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_post
    
    def save(self, *args, **kwargs):
        data = super(Posts, self).save(*args, **kwargs)
        user_lst = User.objects.all()
        for user_p in user_lst:
            post_user = PostUser(user = user_p, post = self, read = False)
            post_user.save()
        user_lst_send = User.objects.filter(bloguser__blog = self.blog, bloguser__signed = True)
        print(user_lst_send)
        mess = 'Опубликован новый пост. Ссылка : /post_view/' + str(self.pk) + '/'
        for user_send in user_lst_send:
            if user_send.email is not None:
                send_mail('Новый пост', mess, settings.EMAIL_HOST_USER, [user_send.email])

class BlogUser(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    signed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.blog}"

class PostUser(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.post}"

