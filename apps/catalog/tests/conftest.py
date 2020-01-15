import pytest
from apps.catalog.models import (
    Author,
    Book,
    BookInstance,
    Genre,
    Language
)


@pytest.fixture
def author(db):
    return Author.objects.create(
        first_name='Förnamn',
        last_name='Efternamn',
        date_of_birth='1900-12-31',
        date_of_death='2011-12-12'
    )


@pytest.fixture
def book(db, author):
    genre = Genre.objects.create(name='sci-fi')
    language = Language.objects.create(name='english')

    book = Book.objects.create(
        title='Book title',
        summary='Lorem ipsum',
        isbn='1234567890',
        language=language,
        author=author
    )
    book.genre.add(genre)
    return book


@pytest.fixture
def book_instance(db, book):
    return BookInstance.objects.create(
            imprint='Lorem ipsum',
            due_back='2019-12-14',
            status='o',
            book=book
        )
