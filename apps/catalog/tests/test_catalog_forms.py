# from django import forms
from apps.catalog.forms import RenewBookForm
import pytest
from datetime import date, timedelta


# # class ExampleForm(forms.Form):
# #     name = forms.CharField(required=True)
# #     age = forms.IntegerField(min_value=18)


@pytest.mark.parametrize(
    'due_back, validity',
    [(date.today() + timedelta(days=1), True),
     (date.today() - timedelta(days=1), False),
     (date.today() + timedelta(weeks=5), False),
     ])
def test_renewbookform_form(due_back, validity):
    form = RenewBookForm(data={
        'due_back': due_back,
    })

    assert form.is_valid() is validity

###########################################

# @pytest.mark.parametrize(
#     'name, valid_name',
#     [
#         ('Hugo', True),
#         ('', False),
#         (None, False),
#     ]
# )
# @pytest.mark.parametrize(
#     'age, valid_age',
#     [
#         ('18', True),
#         ('17', False),
#         (None, False),
#     ]
#  )
# def test_example_form(name, age, valid_name, valid_age):
#     form = ExampleForm(data={
#         'name': name,
#         'age': age,
#     })

#     assert form.is_valid() is (valid_name and valid_age)
