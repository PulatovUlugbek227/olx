from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.

class Region(models.Model):
    title = models.CharField('Регион',max_length=50)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField('Ссылка',unique=True, max_length=50, null=1)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Регион"
        verbose_name_plural="Регионы"
    
    def link(self):
        return reverse('region_detail_url', kwargs={'slug': self.slug})

class Category(models.Model):
    title = models.CharField('Категории',max_length=50)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField('Ссылка',unique=True, max_length=50, null=1)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Категории"
        verbose_name_plural="Категории"
    
    def link(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})
    
    


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=250,verbose_name='Название объявление' )
    description = models.TextField(max_length=1800, verbose_name='Описание' )
    slug = models.SlugField('Ссылка', unique=True, null=True)
    image = models.ImageField('Фото товара', upload_to='posts/', null=False, blank=True)
    publish = models.BooleanField('Публикация', default=True)
    moderation = models.BooleanField('Модерация', default=False)
    date = models.DateTimeField('Дата', default=timezone.now)
    category = models.ManyToManyField(Category, verbose_name='Категория', related_name='posts')
    region = models.ManyToManyField(Region, verbose_name='Регион', related_name='posts')
    price = models.IntegerField(verbose_name='Цена')
    phone_views = models.IntegerField(default=0, verbose_name='Просмотры телефона')

    class Meta:
        verbose_name="Объявление"
        verbose_name_plural="Объявление"
    
    def __str__(self):
        return self.title

    def link(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField('Аватар', blank=True, null=True, upload_to="users/avatars/")
    phone = models.CharField('Телефон', blank=True, null=True, max_length=13)
    latitude = models.CharField('Широта', blank=True, null=True, max_length=13)
    longtitude = models.CharField('Долгота', blank=True, null=True, max_length=13)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name="Профиль"
        verbose_name_plural="Профиль"

    def latest_posts(self):
        return self.user.post_set.order_by('-date')
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' | ' + self.user.username

    def link(self):
        return reverse('profile_detail_url', kwargs={'slug': self.slug})

class Gallery(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост", null=True)
    title = models.CharField('Название', max_length=255)
    image = models.ImageField('Картинка', upload_to="gallery/", null=True)
    date = models.DateTimeField('Время', default=timezone.now)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return self.title


class View(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class Favourite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

class Chat(models.Model):
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever_chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_chats')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Сообщение' )
    date = models.DateTimeField(default=timezone.now)
    readed = models.BooleanField('Прочитаные', default=False)
    
