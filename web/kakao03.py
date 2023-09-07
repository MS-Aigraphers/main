import requests
import json


class Message:
    """
    카카오 메시지 API 클래스

    Parameters
    ----------
    service_key : str
        카카오 개발자 센터에서 발급받은 애플리케이션의 REST API 키
    """

    def __init__(self,file_path=None, redirect_uri="https://localhost:5000", scope="talk_message"):
        self.file_path=file_path
        self.service_key = self.access_keys()
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    def access_keys(self):
        keys = {}
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()  # 빈 칸과 개행 문자 제거
                if line and '=' in line:  # 빈 줄이 아니고, '=' 기호가 있는 경우에만 처리
                    key, value = line.split('=')
                    keys[value] = key.strip("'")
        return keys

    def get_url_for_generating_code(self):
        """
        카카오 인증코드 발급 URL 생성

        Returns
        -------
        str
            카카오 인증코드 발급 URL
        """
        # url = f"https://kauth.kakao.com/oauth/authorize?client_id={self.service_key}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}"
        url=f"https://kauth.kakao.com/oauth/authorize?client_id={self.service_key}&redirect_uri={self.redirect_uri}&response_type=code"
        res = requests.get(url).url
        return res

    def get_code_by_redirected_url(self, url):
        """
        카카오 인증코드 추출

        Parameters
        ----------
        url : str
            카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL

        Returns
        -------
        str
            카카오 인증코드
        """
        return url.split("code=")[1]

    def get_access_token_by_redirected_url(self, url):
        """
        카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL로 액세스 토큰 발급

        Parameters
        ----------
        url : str
            카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL

        Returns
        -------
        str
            액세스 토큰
        """
        code = self.get_code_by_redirected_url(url)
        api_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.service_key,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }
        r = requests.post(api_url, data=data)
        return r.json()['access_token']

    def set_access_token(self, access_token):
        """
        액세스 토큰 설정

        Parameters
        ----------
        access_token : str
            액세스 토큰
        """
        self.headers = {"Authorization": f"Bearer {access_token}"}
        print("액세스 토큰 설정 완료")

    def send_text(self, text, link, **kwargs):
        """
        텍스트 메시지 전송

        Parameters
        ----------
        text : str
            전송할 메시지 (최대 200자)
        """
        params = {
            "object_type": "text",
            "text": text,
            "link": link,
        }
        params.update(kwargs)
        data = {"template_object": json.dumps(params)}
        try:
            r = requests.post(self.url, headers=self.headers, data=data)
            r.raise_for_status()
        except Exception as e:
            print(f"메시지 전송 실패")
            print(e)
            return
        if r.json()['result_code'] == 0:
            print("메시지 전송 성공")
        else:
            print(f"메시지 전송 실패")
            print(r.json())       


if __name__ == "__main__":
    file_path='/Users/iamseungman/Aigrapher/main/web/kaokao_key_copy.txt'
    api=Message(file_path=file_path)
    auth_url=api.get_url_for_generating_code()
    print(auth_url)