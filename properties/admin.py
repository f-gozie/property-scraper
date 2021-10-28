from django.contrib import admin
from .models import Property, Broker

class PropertyAdmin(admin.ModelAdmin):

	list_display = ['name', 'description', 'price', 'address', 'broker']


admin.site.register(Property, PropertyAdmin)