from django.contrib import admin
from django.urls import path
from service.views import empCnt, fetch_erp_data2

urlpatterns = [
    path('api/empCnt/',empCnt),
    path('vacation/',fetch_erp_data2),
]