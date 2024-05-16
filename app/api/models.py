from django.db import models

# Create your models here.
class Subscriber(models.Model):
    first_name = models.CharField(max_length= 100)
    last_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=70, unique=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
