from django.http import JsonResponse
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir='/home/harim/service/instantclient_21_6')


def empCnt(request):
    connections = cx_Oracle.Connection("USERNAME", "password", "dsn")

    cursor = connections.cursor()
    employeeName = request.GET.get('employeeName')

    cursor.execute(
        """
        SELECT MAX(EMP_NO) AS EMP_NO
      , COUNT(*)    AS CNT  
        FROM PA_PM_WAGE_MST A
        WHERE 1=1
            AND CO_DVCD  = '10'                   
             AND HANGL_NM = :employeeName  -- 성명(PARAM1)
              AND RETR_YMD = '99991231'             
        """, {'employeeName': str(employeeName), }
    )

    rows = cursor.fetchmany(10)
    return JsonResponse(data={'text': rows}, json_dumps_params={'ensure_ascii': False})


def empList(request):
    connections = cx_Oracle.Connection("USERNAME", "password", "dsn")

    cursor = connections.cursor()
    employeeName = request.GET.get('employeeName')

    cursor.execute(
        """
               SELECT A.CO_DVCD
     		, A.EMP_NO
     		, A.HANGL_NM
     		, A.NOW_DEPT_NO
     		, (SELECT DEPT_NM FROM BA_DEPT_BAS WHERE DEPT_NO = A.NOW_DEPT_NO) AS DEPT_NM
     		, (SELECT DTCD_NM FROM BA_DTCD WHERE HDCD = 'PA000131' AND DTCD = A.NOW_DTY_CD) AS NOW_DTY_CD_NM  
  		FROM PA_PM_WAGE_MST A
 		WHERE 1=1
   		AND CO_DVCD  = '10'                    -- 회사구분코드
   		AND HANGL_NM = :employeeName           -- 성명(PARAM1)
   		AND RETR_YMD = '99991231'              -- 재직여부 
        """, {'employeeName': str(employeeName), }
    )

    rows = cursor.fetchmany(10)

    return JsonResponse(data={'text': rows}, json_dumps_params={'ensure_ascii': False})


def empInfo(request):
    connections = cx_Oracle.Connection("USERNAME", "password", "dsn")

    cursor = connections.cursor()
    employeeId = request.GET.get('employeeId')

    cursor.execute(
        """
             SELECT A.EMP_NO                                                           AS EMP_NO                       -- 사원번호
     		, A.HANGL_NM                                                         AS HANGL_NM                     -- 성명
     		, A.NOW_DEPT_NO                                                      AS NOW_DEPT_NO                  -- 부서번호
     		, D.DEPT_NM                                                          AS NOW_DEPT_NM                  -- 부서명
     		, A.NOW_DTY_CD                                                       AS NOW_DTY_CD                   -- 직책코드
     		, FC_SA_GET_DTCD_NM(A.CO_DVCD, 'PA000131', A.NOW_DTY_CD)             AS NOW_DTY_CD_NM                -- 직책명
     		, A.NOW_OPOS_CD                                                      AS NOW_OPOS_CD                  -- 직위코드
     		, FC_SA_GET_DTCD_NM(A.CO_DVCD, 'PA000140', A.NOW_OPOS_CD)            AS NOW_OPOS_CD_NM               -- 직위명
     		, A.NOW_CPOS_CD                                                      AS NOW_CPOS_CD                  -- 직급코드
     		, FC_SA_GET_DTCD_NM(A.CO_DVCD, 'PA000130', A.NOW_CPOS_CD)            AS NOW_CPOS_CD_NM               -- 직급명
     		, A.NOW_JGRP_CD                                                      AS NOW_JGRP_CD                  -- 직군코드
     		, FC_SA_GET_DTCD_NM(A.CO_DVCD, 'PA000132', A.NOW_JGRP_CD)            AS NOW_JGRP_CD_NM               -- 직군명
     		, A.NOW_OCPN_CD                                                      AS NOW_OCPN_CD                  -- 직종코드
     		, FC_SA_GET_DTCD_NM(A.CO_DVCD, 'PA000180', A.NOW_OCPN_CD)            AS NOW_OCPN_CD_NM               -- 직종명
     		, FC_PA_GET_WORKTM(A.EMP_NO, '20220625', '1')                        AS WORK_ATOT_TM                 -- 누계근무시간
  		FROM PA_PM_WAGE_MST A
     		, BA_EMP_BAS     B
     		, BA_USER_INF    C
     		, BA_DEPT_BAS    D
 		WHERE 1=1
   		AND A.EMP_NO      = B.EMP_NO
   		AND A.EMP_NO      = C.USER_ID
   		AND A.NOW_DEPT_NO = D.DEPT_NO
   		AND A.NOW_OCPN_CD NOT IN ('B', 'C')
   		AND A.RETR_YMD    = '99991231'
   		AND A.EMP_NO      = :employeeId     -- 사원번호(PARAM1) 
        """, {'employeeId': str(employeeId), }
    )

    rows = cursor.fetchmany(10)

    return JsonResponse(data={'text': rows}, json_dumps_params={'ensure_ascii': False})


def execDoc(request):
    connections = cx_Oracle.Connection("USERNAME", "password", "dsn")

    cursor = connections.cursor()

    apvDvs = request.GET.get('apvDvs')  # '결재구분코드'
    empNo = request.GET.get('empNo')  # '사원번호'
    dnlYmd = request.GET.get('dnlYmd')  # '근무일자'
    lastApvEmpNo = request.GET.get('lastApvEmpNo')  # '결재자 사원번호'
    atndYhm = request.GET.get('atndYhm')  # '출근시간'
    looYhm = request.GET.get('looYhm')  # '퇴근시간'
    eatBgnTm = request.GET.get('eatBgnTm')  # '휴게시작시간'
    eatEndTm = request.GET.get('eatEndTm')  # '휴게종료시간'
    workTm = request.GET.get('workTm')  # '근무시간'
    workAtotTm = request.GET.get('workAtotTm')  # '근무누계시간 '
    sstHldyYn = request.GET.get('sstHldyYn')  # '보상휴가여부'
    sstHldyYmd = request.GET.get('sstHldyYmd')  # '보상휴가일자1'
    cpnsVctnYmd = request.GET.get('cpnsVctnYmd')  # '보상휴가일자2'
    dnlRsn = request.GET.get('dnlRsn')  # '업무내용'
    drftNo = request.GET.get('drftNo')  # '기안문번호'
    out1 = cursor.var(str)
    out2 = cursor.var(str)

    rows = cursor.callproc('PKG_GW_IF_TEST.SP_GW_DNL_INSERT', [str(apvDvs)
        , str(empNo)
        , str(dnlYmd)
        , str(lastApvEmpNo)
        , str(atndYhm)
        , str(looYhm)
        , str(eatBgnTm)
        , str(eatEndTm)
        , str(workTm)
        , str(workAtotTm)
        , str(sstHldyYn)
        , str(sstHldyYmd)
        , str(cpnsVctnYmd)
        , str(dnlRsn)
        , str(drftNo)
        , out1
        , out2
                                                               ]

                           )
    connections.commit()

    return JsonResponse(data={'text': rows}, json_dumps_params={'ensure_ascii': False})