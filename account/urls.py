from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('', index, name='index'),
]