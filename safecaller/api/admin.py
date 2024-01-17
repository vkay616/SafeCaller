from django.contrib import admin
from .models import Contact, RegisteredUser, SpamReport


admin.site.register(Contact)
admin.site.register(RegisteredUser)
admin.site.register(SpamReport)
