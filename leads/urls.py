from django.urls import path
from .views import *

app_name='leads'
urlpatterns=[
    path('',leads,name='leads'),
    path('create_lead/',create_lead,name='create_lead'),
    path('edit_lead/<int:id>/',edit_lead,name='edit_lead'),
    path('delete_lead/<int:id>/',delete_lead,name='delete_lead'),
    path('won/',won,name='won'),
    path('new_lead/',new_leads,name='new_leads'),
    path('site_surveys/',site_surveys,name='site_surveys'),
    path('proposals/',proposals,name='proposals'),

]