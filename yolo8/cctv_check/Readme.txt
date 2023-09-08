1. main.py 코드 실행
2. 동영상 경로 설정 
3. 사용할 model.pt 설정
4. 동영상 저장 시 이름 설정
5. 라벨이 추가,삭제 되었을 시 classes.txt 를 model의 yaml파일과 동일한 라벨 형태로 만들어주어야 함
< classes.txt >
    0 person
    1 weapon
   과
< cctv.yaml >
    0 person
    1 weapon
   이 동일해야 함

 

6. 코드 실행 시 재생되는 동영상은 중간에 esc로 탈출할 수 있고, 탈출한 시점까지의 영상이 저장됨
