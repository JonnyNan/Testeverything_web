from django.db import models

# Create your models here.


class ApiTestCase(models.Model):
    name = models.CharField(max_length=30)
    create_time = models.DateTimeField('创建日期',auto_now_add=True)
    case_abspath = models.CharField(max_length=100)