from django.db import models
import uuid
from django.contrib.auth.models import User, AbstractUser, UserManager
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image

class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name="Photo", upload_to="profile_pics", null=True, blank=True)
    location = models.TextField(verbose_name="Location")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)


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
    description = HTMLField(verbose_name="Description", max_length=2000, null=True, blank=True)

    def display_books(self):
        return ", ".join(book.title for book in self.books.all())

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"

class Book(models.Model):
    title = models.CharField(verbose_name="Title", max_length=100)
    summary = HTMLField(verbose_name="Summary", max_length=2000)
    isbn =  models.IntegerField(verbose_name="ISBN Number")
    author = models.ForeignKey(to="Author", verbose_name="Author", on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    genre = models.ManyToManyField(to="Genre", verbose_name="Genres")
    cover = models.ImageField(verbose_name="Cover", upload_to='covers', null=True, blank=True)

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
    book = models.ForeignKey(to="Book", verbose_name="Book", on_delete=models.CASCADE, related_name="instances")
    due_back = models.DateField(verbose_name="Due Back", null=True, blank=True)
    reader = models.ForeignKey(to="library.CustomUser", verbose_name="Reader", on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Administered'),
        ('t', 'Taken'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(verbose_name="Status", choices=LOAN_STATUS, max_length=1, blank=True, default='d')

    def is_overdue(self):
        return self.due_back and self.due_back < timezone.now().date()

    def __str__(self):
        return f"{self.book.title} ({self.uuid})"

    class Meta:
        verbose_name = "Knygos kopija"
        verbose_name_plural = "Knygų kopijos"


class BookReview(models.Model):
    book = models.ForeignKey(to="Book", verbose_name="Book", on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(to="library.CustomUser", verbose_name="Author", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(verbose_name="Content")
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.book}({self.date_created})"

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Knygos komentaras"
        verbose_name_plural = "Knygos komentarai"
