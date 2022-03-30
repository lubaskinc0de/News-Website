from django.db import models
from django.forms import BooleanField
from django.urls import reverse

# Create your models here.

#представление модели в базе данных
#пишем наш класс
#id - INT
#title - VARCHAR
#content - TEXT
#created_at - DateTime
#upd_at - DateTime
#photo - Image
#is_published - Boolean
# news4 = News.objects.create(title='новость 4', content='контент новости 4')
# News.objects.all() # читаем все
# News.objects.get(pk=4) # по id
#news3.title = 'новость 3' #upd
#news3.delete() # del
#News.objects.order_by('title') сортировка по алфавиту
#News.objects.exclude(pk=5) я не хочу видеть 5 айди

class Code(models.Model):
    user_name = models.CharField(max_length=150)
    user_code = models.IntegerField()

class News(models.Model):
    title = models.CharField(max_length=150,verbose_name='Название') # стр поле для строк малых и больш размеров
    content = models.TextField(blank=True,verbose_name='Текст') # тип данных текст, blank = необязательно к заполнению
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="NewsPaper-created_at") # дата и время # автоматически указывает дату при создании новости
    updated_at = models.DateTimeField(auto_now=True,verbose_name='NewsPaper-updated_at')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',verbose_name='NewsPaper-photo',blank=True) # изображение
    is_published = models.BooleanField(default=True,verbose_name='Опубликовать?',blank=True)
    category = models.ForeignKey('Category',on_delete=models.PROTECT,null=True,verbose_name='Категория') # связь моделей
    views = models.IntegerField(default=0)
    #создали модель (таблицу бд)

    def get_absolute_url(self):
        return reverse('view_news',kwargs={'news_id':self.pk})

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

class Category(models.Model):
    title = models.CharField(max_length=150,db_index=True,verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('category',kwargs={'category_id':self.pk})
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Comment(models.Model):
    news = models.ForeignKey(News,related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    body = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f'От {self.name} на {self.news}'
    class Meta:
        ordering = ['created']








