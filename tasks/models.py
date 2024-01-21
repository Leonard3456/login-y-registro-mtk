from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model): #crea una tabla en sql
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True) #para la fecha que se creo
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE) #para poder vincular dos tablas 

  def __str__(self):
    return self.title + ' - ' + self.user.username
