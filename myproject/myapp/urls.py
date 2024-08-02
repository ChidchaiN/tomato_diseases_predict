from django.urls import path
from .views import call_ml_api

urlpatterns = [
    path('api/predict/', call_ml_api, name='call_ml_api')
]
