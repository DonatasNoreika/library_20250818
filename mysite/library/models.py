from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name=_("Photo"), upload_to="profile_pics", null=True, blank=True)
    location = models.TextField(verbose_name=_("Location"))

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
    name = models.CharField(verbose_name=_("Name"), max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

class Author(models.Model):
    first_name = models.CharField(verbose_name=_("First Name"), max_length=100)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=100)
    description = HTMLField(verbose_name=_("Description"), max_length=2000, null=True, blank=True)

    def display_books(self):
        return ", ".join(book.title for book in self.books.all())

    display_books.short_description = _("Display Books")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

class Book(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    summary = HTMLField(verbose_name=_("Summary"), max_length=2000)
    isbn =  models.IntegerField(verbose_name=_("ISBN Number"))
    author = models.ForeignKey(to="Author", verbose_name=_("Author"), on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    genre = models.ManyToManyField(to="Genre", verbose_name=_("Genres"))
    cover = models.ImageField(verbose_name=_("Cover"), upload_to='covers', null=True, blank=True)

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all())

    display_genre.short_description = _("Genre")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['-pk']



class BookInstance(models.Model):
    uuid = models.UUIDField(verbose_name=_("UUID Code"), default=uuid.uuid4)
    book = models.ForeignKey(to="Book", verbose_name=_("Book"), on_delete=models.CASCADE, related_name="instances")
    due_back = models.DateField(verbose_name=_("Due Back"), null=True, blank=True)
    reader = models.ForeignKey(to="library.CustomUser", verbose_name=_("Reader"), on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('d', _('Administered')),
        ('t', _('Taken')),
        ('a', _('Available')),
        ('r', _('Reserved')),
    )

    status = models.CharField(verbose_name=_("Status"), choices=LOAN_STATUS, max_length=1, blank=True, default='d')

    def is_overdue(self):
        return self.due_back and self.due_back < timezone.now().date()

    is_overdue.short_description = _("Is Overdue")

    def __str__(self):
        return f"{self.book.title} ({self.uuid})"

    class Meta:
        verbose_name = _("Book Instance")
        verbose_name_plural = _("Book Instances")
        ordering = ['-pk']


class BookReview(models.Model):
    book = models.ForeignKey(to="Book", verbose_name=_("Book"), on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(to="library.CustomUser", verbose_name=_("Author"), on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(verbose_name=_("Content"))
    date_created = models.DateTimeField(verbose_name=_("Date Created"), auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.book}({self.date_created})"

    class Meta:
        ordering = ['-date_created']
        verbose_name = _("Book Review")
        verbose_name_plural = _("Book Reviews")
