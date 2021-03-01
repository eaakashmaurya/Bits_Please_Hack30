from django.contrib import admin
from django.urls import path, include
from .views import *

#template tagging
app_name = 'myapp'

urlpatterns = [
    path('', calculate_heatmap_view, name='heatmap'),
]
