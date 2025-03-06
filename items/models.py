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
    status = models.CharField(max_length=50, choices=[('lost', 'Lost'), ('found', 'Found')], default='lost')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items', null=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)


    def __str__(self):
        return f"Comment by {self.author.username} on {self.item.title}"