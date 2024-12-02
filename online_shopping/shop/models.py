from django.db import models

# Create your models here.
class todoitem(models.Model):
    title=models.CharField(max_length=200)
    comleted= models.BooleanField(default=False)