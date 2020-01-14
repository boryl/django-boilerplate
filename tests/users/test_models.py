import pytest


@pytest.mark.django_db
def test_user(client, create_user):
    user = create_user(email='user@example.com', password='secret')
    assert user.email == 'user@example.com'
    assert user.password != 'secret' and not None
    assert user.is_active is True
    assert user.is_staff is False


@pytest.mark.django_db
def test_superuser(client, create_superuser):
    admin_user = create_superuser(
        email='admin@example.com',
        password='topsecret'
    )
    assert admin_user.email == 'admin@example.com'
    assert admin_user.password != 'topsecret' and not None
    assert admin_user.is_active is True
    assert admin_user.is_staff is True
