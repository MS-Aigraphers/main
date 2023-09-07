from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def access_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # 빈 칸과 개행 문자 제거
            if line and '=' in line:  # 빈 줄이 아니고, '=' 기호가 있는 경우에만 처리
                key, value = line.split('=')
                keys[value] = key.strip("'")
    return keys

#code url  https://kauth.kakao.com/oauth/authorize?client_id=자신의 rest key값&redirect_uri=https://example.com/oauth&response_type=code
url = 'https://kauth.kakao.com/oauth/token'
FILE_PATH = "./kaokao_key_copy.txt"
rest_api_key = access_keys(FILE_PATH)  # rest_api
redirect_uri = 'https://example.com/oauth'

# return authorize_code 
# def get_authorize_code(rest_api_key, url):

# 크롬 드라이버 경로 설정 (본인 시스템에 맞게 수정)
driver_path = '/Users/iamseungman/Downloads/chromedriver_mac_arm64 (1)/chromedriver'
driver=None


try:
    # 웹 드라이버 시작
    # option = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(options = option)
    driver = webdriver.Chrome()

    # 카카오 OAuth 페이지 열기
    driver.get(f'https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri=https://example.com/oauth&response_type=code')

    # 로그인 페이지에서 로그인 정보 입력 (카카오 계정으로 로그인)
    driver.find_element(By.ID, 'id_email_2').send_keys('hsgn21@naver.com')
    # driver.find_element_by_id('id_email_2').send_keys('hsgn21@naver.com')
    driver.find_element(By.ID, 'id_password_3').send_keys('640409Hanm!')
    # driver.find_element_by_id('id_password_3').send_keys('640409Hanm!')
    driver.find_element(By.ID, 'id_password_3').send_keys(Keys.RETURN)
    # driver.find_element_by_id('id_password_3').send_keys(Keys.RETURN)

    # 권한 허용 페이지에서 권한 허용 버튼 클릭
    driver.find_element_by_id('auth_accept').click()

    # URL에서 코드 추출
    code = driver.current_url.split('code=')[1]

    # 코드 출력
    print('Received code:', code)

except Exception as e:
    print('An error occurred:', str(e))

finally:
    if driver:
        # 웹 드라이버가 정의되어 있을 때만 종료
        driver.quit()


