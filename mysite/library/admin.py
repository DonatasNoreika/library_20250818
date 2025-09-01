from django.contrib import admin
from .models import Genre, Author, Book, BookInstance

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'display_books']

class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0
    can_delete = False
    readonly_fields = ['uuid']
    fields = ['uuid', 'due_back', 'status', 'reader']

class BookAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'isbn', 'author', 'display_genre']
    readonly_fields = ['pk', 'display_genre']
    inlines = [BookInstanceInLine]

    fieldsets = [
        ('General', {'fields': ('pk', 'title', 'isbn', 'author', 'genre', 'cover', 'display_genre')}),
    ]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book', 'due_back', 'status', 'reader']
    list_filter = ['book', 'status', 'due_back', 'reader']
    list_editable = ['due_back', 'status', 'reader']
    search_fields = ['uuid', 'book__title', 'book__author__first_name']

    fieldsets = [
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'due_back', 'reader')}),
    ]

admin.site.register(Genre)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)