import os
import random
import sys
import sqlite3
from random import sample, randrange
from math import floor
from datetime import datetime
import samsdaq.ml_news as ml
'''
보현 주석 테스트############ 민수가 덮어씀 덮어씀2
##주석 다시 덮기!
'''
'''
 sqlite 위치 
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print("BASE_DIR : ", BASE_DIR)
dbURL = os.path.join(BASE_DIR , 'db.sqlite3')
#print("dbURL : ", dbURL)
tradeAppURL = os.path.join(BASE_DIR , 'tradeApp')
#print("tradeAppURL : " , tradeAppURL)
sys.path.append(tradeAppURL)
#print(BASE_DIR)
con = sqlite3.connect(dbURL)

from views import query_sTrade_trade

'''
    가격 선택
'''
def price_list(now_price, b_or_s, d_state):
    print('가격 선택')
    print(now_price, b_or_s, d_state)
    price_list = []
    price_list.append(now_price)
    temp_price = now_price
    count = 1
    while count < 4 :  #시세에 따라 등락폭 조정
        count +=1
        if (temp_price <= 1000):
            temp_price -= 1
        elif (temp_price <= 5000):
            temp_price -= 5
        elif (temp_price <= 10000):
            temp_price -= 10
        elif (temp_price <= 50000):
            temp_price -= 50
        elif (temp_price <= 100000):
            temp_price -= 100
        elif (temp_price <= 500000):
            temp_price -= 500
        else :
            temp_price -= 5000
        price_list.append(temp_price)
    count = 1
    temp_price = now_price
    while count < 4:
        count += 1
        if (temp_price < 1000):
            temp_price += 1
        elif (temp_price < 5000):
            temp_price += 5
        elif (temp_price < 10000):
            temp_price += 10
        elif (temp_price < 50000):
            temp_price += 50
        elif (temp_price < 100000):
            temp_price += 100
        elif (temp_price < 500000):
            temp_price += 500
        else:
            temp_price += 5000
        price_list.append(temp_price)
    price_list.sort()
    #print("b_or_s, d_state : ", b_or_s, d_state)
    if(b_or_s == "B" and d_state == "GOOD") :
        select_price = random.choices(price_list, weights=[0, 0, 2, 5, 12, 8, 2], k=1)
        return select_price[0]
    if (b_or_s == "B" and d_state == "SOSO"):
        select_price = random.choices(price_list, weights=[1, 2, 10, 12, 10, 2, 1], k=1)
        return select_price[0]
    elif (b_or_s == "B" and d_state == "BAD"):
        select_price = random.choices(price_list, weights=[2, 8, 12, 5, 2, 0, 0], k=1)
        return select_price[0]
    elif (b_or_s == "S" and d_state == "GOOD"):
        select_price = random.choices(price_list, weights=[0, 0, 2, 5, 12, 8, 2], k=1)
        return select_price[0]
    elif (b_or_s == "S" and d_state == "SOSO"):
        select_price = random.choices(price_list, weights=[1, 2, 10, 12, 10, 2, 1], k=1)
        return select_price[0]
    elif (b_or_s == "S" and d_state == "BAD"):
        select_price = random.choices(price_list, weights=[2, 8, 12, 5, 2, 0, 0], k=1)
        return select_price[0]

cur = con.cursor()

b_or_s_list = ["B","S","B","S","B","S","S","S","B","S","B","S"]
user_list = []
comp_list = []
countB = 0
countS = 0

'''
    유저세팅
'''
def list_setting():
    global user_list
    global comp_list

    sql_select = "select user_id from userApp_webuser where user_name like '%_Bot'"
    cur.execute(sql_select)

    for row in cur.fetchall():
        user_list.append(row[0])


'''
    AUTO트레이딩
'''
def stock_auto_trade(d_state):
    ######################
    ######################
    ## K 값 조정하세요..!! ##
    ######################
    ######################
    global countB
    global countS
    global comp_list
    global b_or_s_list
    global user_list
    #트레이드할 유저선택
    trade_user_list = sample(user_list, k=1)

    sql_select = "select code from tradeApp_comp"
    cur.execute(sql_select)
    for row in cur.fetchall():
        comp_list.append([row[0]])

    for user_id in trade_user_list:
        if(user_id == "blackrock"): #시장지배자 
            continue
        #b_or_s = random.choice(b_or_s_list)
        b_or_s_list2 = sample(b_or_s_list, k=1)
        b_or_s = b_or_s_list2[0][0]
        #b_or_s_list = random.choices(b_or_s_list, weights=[1, 1], k=1)
        #b_or_s = b_or_s_list[0]

        # 회사선택
        if(b_or_s == "B"): 
            selected_comp = sample(comp_list, k=1)
            countB += 1
        else : # sell일때 회사선택
            countS += 1
            comp_list = []
            sql_select = "select code from tradeApp_ballance where user_id = ?"
            cur.execute(sql_select, (user_id,) )
            for row in cur.fetchall():
                comp_list.append([row[0]])

            if(len(comp_list) == 0):
                continue
            selected_comp = sample(comp_list, k=1)

        code = selected_comp[0][0]


        query_txt = " select A.code, A.d_1price, ifnull(B.price, A.d_1price) as price"
        query_txt += " from tradeApp_comp A"
        query_txt += " left join tradeApp_order B on(A.code = B.code and B.time1 > (select strftime('%Y-%m-%d', 'now', 'localtime'))"
        query_txt += "    and B.quan = B.tquan and B.tradeyn='Y')"
        query_txt += " where A.code = ?"
        query_txt += " order by B.time2 desc"

        cur.execute(query_txt, (code,))
        now_price = 0
        for row in cur.fetchall():
            now_price = row[2]

        price = price_list(now_price, b_or_s, d_state) # 가격 결정
        select_quan = 0
        if (b_or_s == "S"):
            query_txt = " select quan from tradeApp_ballance where user_id = ? and code = ?"
            cur.execute(query_txt, (user_id, code))
            have_quan = 0
            for row in cur.fetchall():
                have_quan = row[0]
            if (have_quan <= 50): # 100 주 아래로 가지고있으면 전량 판매
                select_quan = have_quan
            elif(have_quan > 300):
                have_quan = int(floor((have_quan/2)/10) * 10)
                select_quan = randrange(50, have_quan, 10)  # 수량 결정
            else:
                select_quan = randrange(50, have_quan, 10)  # 수량 결정
        else:
            select_quan = randrange(10, 100, 10)  # 수량 결정
        print('ID : ', user_id, ' 가격 : ', price, ' 수량 : ',  select_quan, ' 회사코드 : ', code, '매수/매도 : ', b_or_s)
        d_day = '-0 day'
        query_sTrade_trade(user_id, price, select_quan, code, b_or_s, d_day)
        #print("countB, countS, total1 : ", countB, countS, countB+countS)
    # 15초와 45초일때 5분지난(거래가 되지않은 order)삭제
    now = datetime.now()
    nowTime = now.strftime('%S')
    if (nowTime == "15" or nowTime == "45"):
        delete_not_sold()

def delete_not_sold():
    import datetime

    dt_now = datetime.datetime.now()
    #d_today = datetime.date.today()
    # datetime.datetime.now() - datetime.timedelta(minutes=15)
    stand_time = (dt_now - datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
    query_txt = " delete from tradeApp_order where tradeyn = 'N' and time1 < ?"
    #print("###############################")
    #print("##########  delete 시작 ########")
    cur.execute(query_txt, (stand_time,))
    con.commit()
    #print("##########  delete 끝 ##########")
    #print("###############################")

now_news = 0
def choice_d_state():
    d_state = 'SOSO'
    news = ["유럽증시 원자재상승으로 증시 10% ↓",
            "[Market Watch] '바닥의 시작일 뿐..아직 반도 안 왔다'",
            "삼성, 역대급 매출 '대만 반도체'에 자극? 칩 가격 진짜 올릴까",
            "3개월만에 기재부서 나온 초과세수 53조..최근 2년 세수오차 15배 늘었다",
            "초과세수로 나랏빚 갚아도 3년 뒤 1408조..채무비율 60% 육박",
            "['검은 코인' 테라 사태①] 휴지 조각 된 '루나', 폰지사기인가",
            "쌍용차·EMK 매각 작업 '가속도'..달아오르는 M&A 열기",
            "LCD 따라 잡은 중국..'OLED' 대거 선보였지만 '혹평'",
            "우크라 전쟁 어떻게 할겁니까? 푸틴에 묻고 싶네요 [뉴스 쉽게 보기]",
            "1분기 실적 눈물 '쓱' 이마트..이커머스 투자로 장기 실적 개선할까",
            "코스피 주저앉자 물타고 또 물타고..'빚투족' 늘었다",
            "전국 주유소 휘발윳값 1942.6원..'국제유가 영향에 전주比 상승'"]
    global now_news
    result = ml.sentiment_predict(news[now_news])
    if(result > 0.75):
        print("GOOD 일 확률이 높다 : ", result)
        d_state = random.choices(['GOOD', 'SOSO', 'BAD'], weights=[10, 3, 1], k=1)  # 그날의 상태 적용
    elif(result > 0.25):
        print("SOSO 일 확률이 높다 : ", result)
        d_state = random.choices(['GOOD', 'SOSO', 'BAD'], weights=[1, 10, 1], k=1)  # 그날의 상태 적용
    else:
        print("BAD 일 확률이 높다 : ", result)
        d_state = random.choices(['GOOD', 'SOSO', 'BAD'], weights=[1, 3, 10], k=1)  # 그날의 상태 적용
    print("현재 뉴스 : ", news[now_news], "     d_state : ", d_state)
    now_news += 1
    if len(news) == now_news:
        now_news = 0
    return d_state


list_setting() #유저세팅
while_count = 0
while True :
    if(True):
        d_state = choice_d_state()
        for idx in range(0, 10, 1):
            stock_auto_trade(d_state[0]) # 트레이딩
    #  2022-03-13 00:07














