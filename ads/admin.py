from django.contrib import admin
from .models import Users, Ads, Category, Locations

admin.site.register(Users)
admin.site.register(Ads)
admin.site.register(Category)
admin.site.register(Locations)
