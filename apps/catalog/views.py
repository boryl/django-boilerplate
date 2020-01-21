import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm


class AuthorListView(generic.ListView):
    model = Author
    ordering = ['last_name']
    paginate_by = 5


class AuthorDetailView(generic.DetailView):
    model = Author


class BookListView(generic.ListView):
    model = Book
    ordering = ['title']
    paginate_by = 5


class BookDetailView(generic.DetailView):
    model = Book


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan."""
    login_url = '/accounts/login/'
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.borrowed_books.filter()


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.borrowed_books.filter(borrower=self.request.user)


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a'
    ).count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_amps = Genre.objects.filter(name__contains='&').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_amps': num_amps,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate
        # it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (
            # here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_back_date =\
            datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'due_back': proposed_back_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('catalog:authors')
