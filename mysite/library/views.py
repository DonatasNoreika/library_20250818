from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from .models import Book, BookInstance, Author, CustomUser
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from .forms import BookReviewForm, CustomUserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy


def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': Book.objects.count(),
        'num_instances': BookInstance.objects.count(),
        'num_instances_available': BookInstance.objects.filter(status='a').count(),
        'authors': Author.objects.count(),
        'num_visits': num_visits,
    }
    return render(request, template_name="index.html", context=context)


def authors(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, per_page=2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        "authors": paged_authors,
    }
    return render(request, template_name="authors.html", context=context)


def author(request, author_id):
    context = {
        'author': Author.objects.get(pk=author_id),
    }
    return render(request, template_name="author.html", context=context)


def search(request):
    query = request.GET.get('query')
    context = {
        'query': query,
        'books': Book.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query) | Q(author__first_name__icontains=query) | Q(
                author__last_name__icontains=query)),
        'authors': Author.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query)),
    }
    return render(request, template_name='search.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 3


class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = "book.html"
    context_object_name = 'book'
    form_class = BookReviewForm

    # success_url = reverse_lazy('books')

    def get_success_url(self):
        return reverse('book', kwargs={"pk": self.get_object().pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.book = self.get_object()
        form.save()
        return super().form_valid(form)


class UserBookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'user_instances.html'
    context_object_name = 'instances'

    # queryset =

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('login')


@login_required
def profile(request):
    return render(request, template_name="profile.html")


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'photo', 'location']
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class BookInstanceListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = BookInstance
    template_name = "instances.html"
    context_object_name = "instances"

    def test_func(self):
        return self.request.user.is_staff


class BookInstanceDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = BookInstance
    template_name = "instance.html"
    context_object_name = "instance"

    def test_func(self):
        return self.request.user.is_staff


class BookInstanceCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = BookInstance
    template_name = 'instance_form.html'
    fields = ['book', 'due_back', 'reader', 'status']
    success_url = reverse_lazy('instances')

    def test_func(self):
        return self.request.user.is_staff