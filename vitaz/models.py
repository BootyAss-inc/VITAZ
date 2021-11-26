from django.db import models
from django.db.models.fields import IntegerField

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    reg_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return (self.id ,self.name)