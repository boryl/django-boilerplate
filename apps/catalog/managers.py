from django.db import models


class BorrowedBooksManager(models.Manager):
    def get_queryset(self):
        return super(
            BorrowedBooksManager, self
        ).get_queryset().filter(
            status__exact='o'
        ).order_by('due_back')
