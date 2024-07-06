from django.urls import path
from .views import *

app_name='leads'
urlpatterns=[
    path('',leads,name='leads'),
    path('create_lead/',create_lead,name='create_lead'),
]