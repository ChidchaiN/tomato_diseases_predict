# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('index/', views.index, name='index'),
]
