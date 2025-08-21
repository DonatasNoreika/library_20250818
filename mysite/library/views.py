from django.shortcuts import render
from .models import Book, BookInstance, Author

def index(request):
    context = {
        'num_books': Book.objects.count(),
        'num_instances': BookInstance.objects.count(),
        'num_instances_available': BookInstance.objects.filter(status='a').count(),
        'authors': Author.objects.count(),
    }
    return render(request, template_name="index.html", context=context)