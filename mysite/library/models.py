from django.db import models
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"

class Author(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=100)
    last_name = models.CharField(verbose_name="Last Name", max_length=100)
    description = models.TextField(verbose_name="Description", max_length=2000, null=True, blank=True)

    def display_books(self):
        return ", ".join(book.title for book in self.books.all())

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"

class Book(models.Model):
    title = models.CharField(verbose_name="Title", max_length=100)
    summary = models.TextField(verbose_name="Summary", max_length=2000)
    isbn =  models.IntegerField(verbose_name="ISBN Number")
    author = models.ForeignKey(to="Author", verbose_name="Author", on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    genre = models.ManyToManyField(to="Genre", verbose_name="Genres")

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all())

    display_genre.short_description = "Genre"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Knyga"
        verbose_name_plural = "Knygos"
        ordering = ['-pk']



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

    class Meta:
        verbose_name = "Knygos kopija"
        verbose_name_plural = "Knygų kopijos"