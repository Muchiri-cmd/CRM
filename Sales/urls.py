from django.urls import path
from .views import *

app_name='Sales'

urlpatterns = [
    path('funnel/',sales_funnel,name='sales_funnel'),
    path('analytics/',sales_analytics,name='sales_analytics'),
    path('pipeline/',sales_pipeline,name='sales_pipeline')
]
