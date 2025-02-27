# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('lost', 'Lost'), ('found', 'Found')])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = 'lost'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item.title