import smtplib
from email.mime.text import MIMEText
import json

# secrets.json 파일이 필요한 상태입니다 (깃 이그놀 처리 상태) 테스트가 필요하신분은 알려주세욥!
# secrets.json 파일을 엽니다.
with open("secrets.json", "r") as secrets_file:
    secrets_data = json.load(secrets_file)

# "APP_PASSWORD" 키의 값을 가져옵니다.
app_password = secrets_data.get("APP_PASSWORD")

# 가져온 암호를 출력하거나 사용할 수 있습니다.
print("APP_PASSWORD 값:", app_password)


def send_email(receiver, content, title):
    receiver = receiver
    content = f'{title} 문제가 발생 하였습니다. 자세한 내용은 {content}에서 확인해주세요'
    title = title

    # (*)메일의 발신자 메일 주소, 수신자 메일 주소, 앱비밀번호(발신자)
    sender = 'skcksdnr2@gmail.com'


    msg = MIMEText(content)
    msg['Subject'] = title
    # 세션 생성
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            # TLS 암호화
            s.starttls()

            # 로그인 인증과 메일 보내기
            s.login(sender, app_password)
            s.sendmail(sender, receiver, msg.as_string())
            print("이메일이 성공적으로 전송되었습니다.")

    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")


# class Test:
#     def __init__(self):
#         self.receiver = None
#         self.content = None
#         self.title = None
#
#     def send_email(self, receiver, content, title):
#         self.receiver = receiver
#         self.content = content
#         self.title = title
#
#         # (*)메일의 발신자 메일 주소, 수신자 메일 주소, 앱비밀번호(발신자)
#         sender = 'skcksdnr2@gmail.com'
#
#
#         msg = MIMEText(content)
#         msg['Subject'] = title
#         # 세션 생성
#         with smtplib.SMTP('smtp.gmail.com', 587) as s:
#             # TLS 암호화
#             s.starttls()
#
#             # 로그인 인증과 메일 보내기
#             s.login(sender, app_password)
#             s.sendmail(sender, receiver, msg.as_string())