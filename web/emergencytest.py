from typing import Any
import datetime

class Emergency :

    def __init__(self, fire=False, weapon=False, firecount=None, weaponcount=None, todayfire=0, todayweapon=0) :
        
        # 외부에서 화재, 무장을 감지해서 신호를 받는 경우 (DB)
        self.fire = fire
        self.weapon = weapon
        
        # 이미 카운트 된 화재, 무장 횟수 (DB or python)
        self.firecount = firecount
        self.weaponcount = weaponcount
        
        # 사건 횟수를 날짜별로 파이썬 내에서 기록할 경우
        self.todayfire = todayfire
        self.todayweapon = todayweapon
        
        # dict 형태용 리스트
        self.incidents = []
    


    # 화재, 무장 중 하나라도 일어나면 True 반환
    def check(self, fire, weapon) :
        if fire or weapon : # fire == True or weapon == True
            return True



# dict로 {사건 : 사건시간} 형태로 기록

# # dict 저장방식1 : if 문 형식
#     def record_if(self, fire, weapon) :
#         if fire :
#             self.todayfire += 1
#             self.incidents.append({
#                 "type": "Fire",
#                 "datetime": datetime.datetime.now()
#             })
#             # 이후 화재 대응 방안
            
#         if weapon :            # 독립이므로 elif, else 사용 X
#             self.todayweapon += 1
#             self.incidents.append({
#                 "type": "weapon",
#                 "datetime": datetime.datetime.now()
#             })
#             # 이후 무장 대응 방안
            
            
            
# dict 저장방식2 : 화재, 무장 이외의 경우 도입 쉬움 if문 추가 필요 X
    def record_incident(self, incident_type):
        
        # 각종 조건들
        # if emergency.check : 
        # if incident_type in ["fire", "weapon"]: 
        # if DB 신호
            self.incidents.append({
                "type": incident_type,
                "datetime": datetime.datetime.now()
            })


# --------------------------

# dict 받아오는 경우
    def get_record(self, incident_type, record_time): # 사건 종류, 시간
            self.incidents.append({
                "type": incident_type,
                "datetime": record_time
            })

            
# db 수정
    def edit_record(self, idx, edit_type, edit_time) : # idx = 인덱스, edit_type = 사건 수정, edit_time : 시간 수정
        
        # 새 딕셔너리 생성
        edit_data = {
            "type": edit_type,
            "datetime": edit_time
        }
        
        # 해당 인덱스 딕셔너리 교체
        self.incidents[idx] = edit_data
        
        
        
# 사고별 총 집계
    def incident_counter(self):
        incident_counts = {}
        for incident in self.incidents:
            incident_type = incident["type"]
            if incident_type in incident_counts:
                incident_counts[incident_type] += 1
            else:
                incident_counts[incident_type] = 1

        for incident_type, count in incident_counts.items():
            print(f"{incident_type}: {count}")
            
            
            
    # 특정 날짜 구간 내의 사건을 집계하는 메서드
    def incident_counter(self, start_date, end_date):
        incident_counts = {}
        for incident in self.incidents:
            incident_type = incident["type"]
            incident_datetime = incident["datetime"]

            # 사건 발생일자가 주어진 날짜 구간에 속하는 경우만 고려
            if start_date <= incident_datetime <= end_date:
                if incident_type in incident_counts:
                    incident_counts[incident_type] += 1
                else:
                    incident_counts[incident_type] = 1

        for incident_type, count in incident_counts.items():
            print(f"{incident_type}: {count}")






######### 테스트 ########

# 클래스 인스턴스 생성
emergency_instance = Emergency()

# 사건 기록 (예시)
emergency_instance.record_incident("fire")
emergency_instance.record_incident("weapon")
emergency_instance.record_incident("fire")

# 특정 날짜 구간 설정
start_date = datetime.datetime(2023, 9, 1)  # 시작 날짜
end_date = datetime.datetime(2023, 9, 20)  # 종료 날짜

# 사건 카운트 출력 (특정 날짜 구간 내의 사건만 고려)
print(emergency_instance.incident_counter(start_date, end_date))

######### 테스트 ########
