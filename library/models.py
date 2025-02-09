from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    name = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT)
    description = models.TextField()
    published_year = models.CharField(max_length=4)
    stock = models.PositiveIntegerField()
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.name

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.name}"

class StatusDetail(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who updated the status
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request} - {self.status.name}"

