import pytest
from django.urls import reverse


@pytest.mark.parametrize(
   'view, result', [
       ('index', 200),
       ('books', 200),
       ('authors', 200),
       ]
)
@pytest.mark.django_db
def test_catalog_views(view, result, client):
    url = reverse('catalog:' + view)
    response = client.get(url)
    assert response.status_code == result
    assert '<!DOCTYPE html>' in response.content.decode()


@pytest.mark.django_db
def test_catalog_detail_views(client, book, author):
    url = reverse('catalog:author-detail', kwargs={'pk': author.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in response.content.decode()

    url = reverse('catalog:book-detail', kwargs={'pk': book.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in response.content.decode()
