from django.urls import reverse


def test_admin_login_view(client):
    url = reverse('admin:login')
    response = client.get(url)
    assert response.status_code == 200
