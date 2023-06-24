# sa_labor_project/projectApp/urls.py : API urls.py
from django.urls import path, include
from .views import (
    projectAppApiView,
    GeoJSONFilesAPIView, CountriesAPIView, HomepageView,

)

urlpatterns = [
    path('api', projectAppApiView.as_view()),
    path('countries/<str:country>/', GeoJSONFilesAPIView.as_view(), name='files'),
    path('countries/', CountriesAPIView.as_view(), name='countries'),
    path('home/', HomepageView.as_view(), name='index')
]