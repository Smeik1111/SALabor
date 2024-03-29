from dateutil import parser as time_parser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from silk.profiling.profiler import silk_profile
from rest_framework import views
from rest_framework.response import Response
from .serializers import GeoJSONFileSerializer, CountrySerializer, AnswerSerializer, CountryBorderSerializer
from .models import GeoJSONFile, Country
from django.shortcuts import render


class projectAppApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

class CountriesAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GeoJSONFilesAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        start_date_raw = request.GET.get('start_date', None)
        end_date_raw = request.GET.get('end_date', None)
        country = Country.objects.get(name=kwargs['country'])
        if start_date_raw is None or end_date_raw is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            start_date = time_parser.parse(start_date_raw)
            end_date = time_parser.parse(end_date_raw)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        files_obj = GeoJSONFile.objects.filter(country=country, date__range=(start_date, end_date))
        #serializer = GeoJSONFileSerializer(files_obj, many=True)
        config = "example config"
        values = ["value1", "value2", "value3"]
        serializer = AnswerSerializer(data={
            'config': CountryBorderSerializer(country).data,
            'values': GeoJSONFileSerializer(files_obj, many=True).data
        })
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

class HomepageView(views.APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context=None)