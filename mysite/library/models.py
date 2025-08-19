from django.db import models
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=100)
    last_name = models.CharField(verbose_name="Last Name", max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(verbose_name="Title", max_length=100)
    summary = models.TextField(verbose_name="Summary", max_length=2000)
    isbn =  models.IntegerField(verbose_name="ISBN Number")
    author = models.ForeignKey(to="Author", verbose_name="Author", on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ManyToManyField(to="Genre", verbose_name="Genres")

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    uuid = models.UUIDField(verbose_name="UUID Code", default=uuid.uuid4)
    book = models.ForeignKey(to="Book", verbose_name="Book", on_delete=models.CASCADE)
    due_back = models.DateField(verbose_name="Due Back", null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Administered'),
        ('t', 'Taken'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(verbose_name="Status", choices=LOAN_STATUS, max_length=1, blank=True, default='d')

    def __str__(self):
        return f"{self.book.title} ({self.uuid})"

