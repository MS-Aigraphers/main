# plt는 그래프를 파이썬에서 그리지 않는 이상 안쓰일 예정
# import matplotlib.pyplot as plt
from datetime import date, timedelta
import sqlite3
# https://dacon.io/codeshare/1994 pandas 이용방안

# 범죄 횟수 카운트 및 날짜, 시간대별 통계
class TimeSeriesPlotter:
    def __init__(self):
        self.x_data = []  # 날짜 데이터
        self.y_theft_counts = []  # theft 범죄 횟수 데이터
        self.y_weapon_counts = []  # weapon 범죄 횟수 데이터
        
# 해당 부분은 추후 DB와 연동하는 식으로 수정해서 사용
    def set_theft_crime_counts(self, theft_crime_counts):
        self.y_theft_counts = theft_crime_counts

    def set_weapon_crime_counts(self, weapon_crime_counts):
        self.y_weapon_counts = weapon_crime_counts


# 날짜를 어떻게 표현하느냐에 따라 천차만별
    def set_date_range(self, start_date, end_date):
        # 날짜 범위 생성
        if start_date <= end_date : # 보려고 하는 시간대가 꼬이지 않도록
            pass
        else :  # 마지막 시간대가 첫 시간대보다 앞에 오는 잘못된 경우
            pass

# 그래프 부분 삭제



# 판매량 - 막대 데이터
class items :
    def __init__(self, DB) -> None:
        self.DB_path = DB # 가져올 데이터
        # 판매 물품 목록 작성
        '''
        예상도 (DB 형태에 따라서)
        ice = {}
        snack = {}
        drink = {}
        '''
        pass
    

    def item_counts(self, ice, snack, drink):
        self.ice_counts = ice
        self.snack_counts = snack
        self.drink_counts = drink



# 날짜
    def set_date_range(self, start_date, end_date):
        # 날짜 범위 생성
        if start_date <= end_date : # 보려고 하는 시간대가 꼬이지 않도록
            pass
        else :  # 마지막 시간대가 첫 시간대보다 앞에 오는 잘못된 경우
            pass


    
# 데이터 삭제 (DB을 가져오는게 우선, 그 뒤 SQL 방식으로 데이터 조작)
class delete_data :

    def delete_data_from_db(db_file, table_name, condition):
        # 데이터베이스에 연결
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # SQL DELETE 쿼리 생성 및 실행
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        cursor.execute(delete_query)
        
        # 변경사항을 커밋하고 연결을 닫음
        conn.commit()
        conn.close()

    # 예제
    db_file = 'my_database.db'  # 데이터베이스 파일 경로
    table_name = 'my_table'     # 테이블 이름
    condition = 'age < 30'      # 삭제할 조건

    delete_data_from_db(db_file, table_name, condition)
    
    
    
    
# DB에서 날짜 따오는 기능 분리
def fetch_dates_from_db(db_file, table_name):
    # 데이터베이스에 연결
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # SQL SELECT 쿼리를 사용하여 날짜 데이터 가져오기
    select_query = f"SELECT date_column FROM {table_name}"
    cursor.execute(select_query)
    
    # 결과 가져오기
    dates = cursor.fetchall()
    
    # 연결 닫기
    conn.close()

    return dates

# 예제
db_file = 'my_database.db'  # 데이터베이스 파일 경로
table_name = 'my_table'     # 테이블 이름

dates = fetch_dates_from_db(db_file, table_name)
for date in dates:
    print(date[0])  # 날짜 데이터 출력
    
    

