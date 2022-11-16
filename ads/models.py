from django.db import models



class Locations(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField(max_length=255, default=0)
    lng = models.FloatField(max_length=255,default=0)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.name





class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


    def __str__(self):
        return self.name

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=50)
    age = models.IntegerField()
    location = models.ManyToManyField(Locations)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username


class Ads(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='logos/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


    def __str__(self):
        return self.name


