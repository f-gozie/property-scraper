from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK,
	HTTP_201_CREATED,
	HTTP_204_NO_CONTENT
)

from .models import Property, Broker
from .serializers import PropertySerializer, BrokerSerializer

from utils.scraper import retrieve_property_details, retrieve_property_urls


class UpdateProperties(APIView):
	permission_classes = [AllowAny,]

	def post(self, request):
		urls = retrieve_property_urls()
		properties = retrieve_property_details(urls)

		for prop in properties:
			broker, _ = Broker.objects.get_or_create(name=prop['broker_name'], license=prop['broker_license'])
			if not Property.objects.filter(name=prop['property_name']).exists():
				Property.objects.create(name=prop['property_name'], description=prop['property_description'], address=prop['property_address'], price=prop['property_price'], broker=broker)

		return Response("Successfully updated properties", status=HTTP_201_CREATED)


class GetProperties(generics.ListAPIView):

	queryset = Property.objects.all()
	serializer_class = PropertySerializer


class GetBrokers(generics.ListAPIView):

	queryset = Broker.objects.all()
	serializer_class = BrokerSerializer