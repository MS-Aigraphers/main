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
    def record_incident(self, incident_type, record_time, img, msg):
        
        # 각종 조건들
        # if emergency.check : 
        # if incident_type in ["fire", "weapon"]: 
        # if DB 신호
            self.incidents.append({
                "type": incident_type, #사건 종류
                "datetime": record_time, # 사건 발생 시간
                "highlight" : img, # 하이라이트 이미지
                "msg" : msg # 메세지 발송 여부
                
            })


# --------------------------

# dict 받아오는 경우
    def get_record(self, incident_type, record_time, img, msg): # 사건 종류, 시간, 영상, 메세지 발송 여부
            self.incidents.append({
                "type": incident_type,
                "datetime": record_time,
                "highlight" : img,
                "msg" : msg
            })

            
# db 수정
    def edit_record(self, idx, edit_type, edit_time, img, msg) : # idx = 인덱스, edit_type = 사건 수정, edit_time : 시간 수정
        
        # 새 딕셔너리 생성
        edit_data = {
            "type": edit_type,
            "datetime": edit_time,
            "highlight" : img,
            "msg" : msg
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





# 신고 기능
class Report :
    
    def __init__(self) -> None:
        # 대충 신고 유형 리스트
        self.incident_types = list(set(incident["type"] for incident in Emergency.incidents))
        
        self.reports = {} # 신고 목록을 위한 빈 딕셔너리
        
    
    
    # 신고 유형을 저장된 리스트에서 출력
    def select_incident_type(self):
        for i, incident_type in enumerate(self.incident_types, start=1):
            print(f"{i}. {incident_type}")

        while True:
            valid_choices = [str(i) for i in range(1, len(self.incident_types) + 1)]
            choice = input(f'선택 ({"/".join(valid_choices)}): ')
            if choice in valid_choices:
                return self.incident_types[int(choice) - 1]
            else:
                print("올바른 선택을 입력하세요.")


    # 상세 신고 내용 적을 수 있게
    def submit_report(self):
        incident_type = self.select_incident_type()  # 신고 유형 선택
        report_text = input("신고 내용을 입력하세요: ") # 빠른 이해를 위한 적당한 문장
        self.reports.append({"type": incident_type, "text": report_text, "date" : datetime.datetime.now()}) # 사건 종류, 신고 내용, 신고 시간
        print("신고가 제출되었습니다.") # 고객의 안심을 위한 보고


    # 신고를 끝마친 뒤 해당 신고 내역을 볼 수 있도록, 그냥 예시로 적어둔 내용
    def view_reports(self):
        print("신고 목록:")
        for i, report in enumerate(self.reports, start=1):
            print(f"{i}. 신고 유형: {report['type']}")
            print(f"   내용: {report['text']}")
            
    # 신고내역 삭제기능은 del 하나로 해결될 것 같으니 미작성
