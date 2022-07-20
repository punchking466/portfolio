from django.contrib import admin
from django.urls import path
from service.views import empCnt,empList,empInfo,execDoc

urlpatterns = [
    path('api/empCnt/',empCnt),
    path('api/empList/',empList),
    path('api/empInfo/',empInfo),
    path('api/execDoc/',execDoc),
]