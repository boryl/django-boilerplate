import pytest
import uuid


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def test_user_email():
    return 'user@example.com'


@pytest.fixture
def test_admin_email():
    return 'admin@example.com'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'email' not in kwargs:
            kwargs['email'] = str(uuid.uuid4()) + '@example.com'
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_superuser(db, django_user_model, test_password):
    def make_superuser(**kwargs):
        kwargs['password'] = test_password
        if 'email' not in kwargs:
            kwargs['email'] = str(uuid.uuid4()) + '@example.com'
        return django_user_model.objects.create_superuser(**kwargs)
    return make_superuser


# @pytest.fixture
# def auto_login_user(db, client, create_user, test_password):
#     def make_auto_login(user=None):
#         if user is None:
#             user = create_user(email='test@example.com', password="secret")
#         client.login(email=user.email, password=test_password)
#         return client, user
#     return make_auto_login
