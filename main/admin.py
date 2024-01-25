from django.contrib import admin
from .models import Room, Message, Registration, ResumeText, MatchForm, login


# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Registration)
admin.site.register(ResumeText)
admin.site.register(MatchForm)
admin.site.register(login)