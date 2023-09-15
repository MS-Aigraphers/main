from mailsend import *
from datetime import datetime

# test= Test()
receivers =['skcksdnr@naver.com',
            # 이메일 주소입력,
            # 이메일 주소입력,
            ]

send_email(receivers, content= 'naver.com', title= '도난감지', start_time=datetime.now())

# datetime.now()에 변수 입력해주시면 됩니다.