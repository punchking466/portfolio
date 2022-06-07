from django.db.models import Sum, Avg, Count 
from django.db.models.functions import TruncDate 
from django.shortcuts import render 
from django.views import View 
from django.http import JsonResponse 
import cx_Oracle 
 
 
# Create your views here. 
from service.models import Order 
 
 
class ServiceView(View): 
 
    # cx_Oracle.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH) 
    # connections = cx_Oracle.Connection(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN) 
 
    def get(self, request): 
        remain = 10 
        employee_id = request.GET.get('employee_id') 
        if not employee_id: 
            return JsonResponse({'error': '직원번호는 필수 값입니다.'}) 
 
        tokend = {'PETFOOD': 'abc456ccc', 'HARIM': 'bbb555aaa'}
        if request.GET.get('token','') not in tokend.values():
            return JsonResponse({'error': '토큰 인증에 실패했습니다.'}, json_dumps_params={'ensure_ascii': False})

        remain_dayd = {'101010': 15, '101011': 20, '101012': 13}
        named ={'101010': '이승빈', '101011': '강주원', '101012': '나승민'}
        reasond = {'SICK': '병가', 'PERSONAL': '개인적인 사정'}

        remain_days =remain_dayd[employee_id] - int(request.GET.get('days', 0))

        cursor = self.connections.cursor()

        cursor.execute(
            """
                SELECT * FROM SA_Z_HRPF_LINK
                WHERE CD_COMPANY = '1000' AND CD_PLANT = '1000'
                AND DT_IO BETWEEN '20220314' and '20220315'
                AND CD_USERDEF5 = 'Y'
            """
        )
        results = cursor.fetchmany(10)

        reason = reasond[request.GET['reason']]
        txt = f'{named[employee_id]}님께서 {reason}(으)로 {request.GET["days"]}일을 사용하여, 잔여 연차일수는 {remain_days}일 입니다.'
        return JsonResponse(data={'remain': remain_days, 'text': txt, 'data': results}, json_dumps_params={'ensure_ascii': False})

