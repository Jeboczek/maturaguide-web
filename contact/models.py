from django.db import models
from django.db.models.fields import AutoField, CharField, EmailField
from django.db.models.fields.related import ForeignKey

class MessageReason(models.Model):
    id = AutoField(blank=False, null=False, primary_key=True, db_index=True)
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.name}"


class Message(models.Model):
    id = AutoField(blank=False, null=False, primary_key=True, db_index=True)
    firstname = CharField(max_length=128, blank=False, null=False)
    email = EmailField(blank=False, null=False)
    phonenumber = CharField(max_length=9, blank=True, null=True)
    content = CharField(max_length=1024, blank=False, null=False)
    reason = ForeignKey(MessageReason, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Message from {self.firstname}"