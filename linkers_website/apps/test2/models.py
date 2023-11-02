from django.db import models
import json

# Create your models here.

class testdata(models.Model):
    id = models.CharField(primary_key=True, max_length=15,default='1')
    Sequence = models.CharField(max_length=100)
    backbone = models.CharField()
    average_flexibility=models.FloatField(default=0)


    def __str__(self):
        return self.id
