from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from .models import Property, Broker


class PropertySerializer(serializers.ModelSerializer):

	class Meta:
		model = Property
		fields = '__all__'


class BrokerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Broker
		fields = '__all__'