from django.contrib import admin
from .models import Property, Broker

class PropertyAdmin(admin.ModelAdmin):

	list_display = ['name', 'description', 'price', 'address', 'broker']
	list_per_page = 30

class BrokerAdmin(admin.ModelAdmin):

	def no_of_properties(self, obj):
		return obj.properties.count()

	list_display = ['name', 'license', 'no_of_properties']
	list_per_page = 30


admin.site.register(Property, PropertyAdmin)
admin.site.register(Broker, BrokerAdmin)