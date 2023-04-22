# sa_labor_project/projectApp/urls.py : API urls.py
from django.urls import path, include
from .views import (
    projectAppApiView,
)

urlpatterns = [
    path('api', projectAppApiView.as_view()),
]