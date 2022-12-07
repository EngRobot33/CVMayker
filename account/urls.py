from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('panel/', panel, name='panel'),
    path('export_excel/', export_excel, name='export-excel'),
    path('search_result/', search_result, name='search-result'),
    path('panel/sort/<str:field>', sort, name='sort'),
    path('resume/', resume, name='resume'),
    path('skill/create/', create_skill, name='create-skill'),
]