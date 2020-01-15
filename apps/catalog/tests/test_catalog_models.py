class TestCatalogModels:
    def test_author_model(client, author):
        assert author.first_name
        assert author.last_name
        assert author.date_of_birth
        assert author.date_of_death
        assert author.pk

        assert author.get_absolute_url()

    def test_book_model(client, book):
        assert book.title
        assert book.summary
        assert book.isbn
        assert book.author
        assert book.pk

        # Language model
        assert book.language.name

        # Genre model
        genre_set = book.genre.all()
        assert genre_set[0].name

    def test_bookinstance_model(client, book_instance):
        assert book_instance.imprint
        assert book_instance.due_back
        assert book_instance.status
        assert book_instance.book.title
        assert book_instance.is_overdue
