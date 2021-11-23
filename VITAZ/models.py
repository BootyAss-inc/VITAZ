from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=25)
    reg_date = models.DateField(auto_now_add=True)
    aproved = models.BooleanField(default=False)

    def __str__(self):
        return self.name