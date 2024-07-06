from django.urls import path
from .views import home

app_name='leads'
urlpatterns=[
    path('',home,name='home')
]