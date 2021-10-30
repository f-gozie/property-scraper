from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED
)
from rest_framework.views import APIView

from utils.scraper import retrieve_property_details, retrieve_property_urls
from .models import Property, Broker
from .serializers import PropertySerializer, BrokerSerializer


class UpdateProperties(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        urls = retrieve_property_urls()
        properties = retrieve_property_details(urls)

        for prop in properties:
            broker, _ = Broker.objects.get_or_create(name=prop['broker_name'], license=prop['broker_license'])
            if not Property.objects.filter(name=prop['property_name']).exists():
                Property.objects.create(name=prop['property_name'], description=prop['property_description'],
                                        address=prop['property_address'], price=prop['property_price'], broker=broker)

        return Response("Successfully updated properties", status=HTTP_201_CREATED)


class GetProperties(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class GetBrokers(generics.ListAPIView):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
