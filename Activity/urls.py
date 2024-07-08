from django.urls import path
from .views import *

app_name = 'Activity'

urlpatterns = [
    path('', activity_view, name='activity_view'),
]
