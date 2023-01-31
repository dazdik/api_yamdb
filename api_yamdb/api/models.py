from django.db import models
# # Create your models here.


class Title(models.Model):
    name = models.CharField(max_length=16)
    year = models.IntegerField()
    category = models.IntegerField()
