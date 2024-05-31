from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    categories = models.ManyToManyField(Category, related_name='images')
    created_date = models.DateField(auto_now_add=True)
    age_limit = models.PositiveIntegerField()

    def __str__(self):
        return self.title
