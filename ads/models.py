from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)



class Ads(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)