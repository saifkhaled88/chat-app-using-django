from django.contrib import admin
from .models import CustomUser, ChatMessage

admin.site.register(CustomUser)
admin.site.register(ChatMessage)