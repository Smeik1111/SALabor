from dateutil import parser as time_parser
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from silk.profiling.profiler import silk_profile
from rest_framework import views
from rest_framework.response import Response
from .serializers import GeoJSONFileSerializer, CountrySerializer
from .models import Sentinel5PData, Scanline, CoValue, GeoJSONFile, Country
from .serializers import Sentinel5PDataSerializer, ScanlineSerializer, CoValueSerializer


class projectAppApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    @silk_profile(name='ViewApiGetScanlineByTime')
    def get(self, request, *args, **kwargs):
        # http://127.0.0.1:8000/projectApp/api?start_time=2018-12-28T23:59:59&end_time=2020-11-15T23:59:59
        # time should be in ISO 8601
        start_time_raw = request.GET.get('start_time', None)
        end_time_raw = request.GET.get('end_time', None)
        start_time = time_parser.parse(start_time_raw)
        end_time = time_parser.parse(end_time_raw)

        objects = Scanline.objects.filter(time__range=(start_time, end_time))
        serializer = ScanlineSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        else:
            start_date = time_parser.parse(start_date_raw)
            end_date = time_parser.parse(end_date_raw)
            files_obj = GeoJSONFile.objects.filter(country=country, date__range=(start_date, end_date))
        serializer = GeoJSONFileSerializer(files_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
