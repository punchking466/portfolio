from django.shortcuts import render
from service.models import *
from .serializers import InformationSerializer
from django.views import View
from django.http import JsonResponse
from django.db.models import *

def getData(request):
     employee_id =request.GET.get('employee_id')
     if not employee_id:
          return JsonResponse({'error : 직원번호 값은 필수입니다.'})

     info = Information.objects.get(employee_id=employee_id)

     remain_days = info.remain_dayd - int(request.GET.get('days'), 0)

     print(info.name)
     print(info.remain_dayd)

     txt = f'{info.name}님의 연차는 {info.remain_dayd}이고  {request.GET["days"]}일 사용하여 잔여 연차는 {remain_days}일 입니다.'

     return JsonResponse(data={'text': txt}, json_dumps_params={'ensure_ascii': False})