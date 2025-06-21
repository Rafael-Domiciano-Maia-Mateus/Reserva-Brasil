from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserApp)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Property)
admin.site.register(Reservation)
