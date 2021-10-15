from django.contrib import admin
from .models import MessageReason, Message

# Register your models here.

admin.site.register(Message)
admin.site.register(MessageReason)