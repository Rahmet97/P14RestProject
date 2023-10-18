from django.db import models


class Hashtag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    hashtag = models.ManyToManyField(Hashtag)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
