from django.shortcuts import render
from service.models import *
from django.views import View
from django.http import JsonResponse
from django.db.models import *
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir='/home/harim/service/instantclient_21_6')

def empCnt(request):
    connections = cx_Oracle.Connection(user='UHATIS', password='UHATIS', dsn='203.235.173.218:1523/HATISDEV')

    cursor = connections.cursor()
    employee_name =request.GET.get('employee_name')

    cursor.execute(
        """
        SELECT MAX(EMP_NO) AS EMP_NO
      , COUNT(*)    AS CNT  
        FROM PA_PM_WAGE_MST A
        WHERE 1=1
            AND CO_DVCD  = '10'                   
             AND HANGL_NM = :employee_name  -- 성명(PARAM1)
              AND RETR_YMD = '99991231'             
        """,{'employee_name': str(employee_name),}
    )

    rows = cursor.fetchmany(10)

    return JsonResponse(data={'사번' : rows.EMP_NO, 'Count' : rows.CNT}, json_dumps_params={'ensure_ascii': False})


def fetch_erp_data2(request):
    connections = cx_Oracle.Connection(user='UHATIS', password='UHATIS', dsn='203.235.173.218:1523/HATISDEV')

    cursor = connections.cursor()
    employee_id =request.GET.get('employee_id')

    cursor.execute(
        """
                SELECT A.EMP_NO, A.HANGL_NM, D.DEPT_NM
                FROM PA_PM_WAGE_MST A, BA_DEPT_BAS D
                where A.NOW_DEPT_NO = D.DEPT_NO AND A.EMP_NO = :employee_id 
        """,{'employee_id': str(employee_id),}
    )

    rows = cursor.fetchmany(10)

    return JsonResponse(data={'text': rows}, json_dumps_params={'ensure_ascii': False})