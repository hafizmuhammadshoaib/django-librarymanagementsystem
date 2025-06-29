from django.db import models


class BorrowingHistory(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE)
    member = models.ForeignKey("member.Member", on_delete=models.CASCADE)
    borrowing_date = models.DateField()
    returning_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
