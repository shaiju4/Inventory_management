from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Items)
admin.site.register(Location)