[프로그램 제목]
서버별 wcar페이지 날짜 추출 프로그램

[제작자]
개발부 / 김홍연 사원

[팀 / 요청자]
개발부 / 이광헌 부장

[마지막 수정]


[출시일자]
2023-01-11

[마지막 수정일자]


[메인 파일]
main.py

[실행 파일]
run.bat

[관련 폴더]


[관련 파일]
output1 - 결과를 추출합니다. (서버 이름/ 서버 ip/ 날짜) 
Ex.1 aws104(탭)15.165.106.252(탭)2023-01-06 - 정상 데이터
Ex.2 aws146(탭)52.79.83.46(탭)서버연결x - 해당 서버와 통신되지 않음을 의미
Ex.3 aws147(탭)13.125.95.100(탭)파일 존재x - 해당 서버와 연결은 되었지만, 경로에 파일이 없음을 의미
Ex.4 aws147(탭)13.125.95.100(탭)날짜 존재x - 해당 서버와 연결 되어, 해당 파일에 접근 했으나, 파일에 날짜가 없음을 의미

error.txt - 서버 연결이 되지 않거나, 파일이 존재하지 않은 error 데이터를 넣음.

[프로그램 설명]
DB 서버에 접근해, use_flag 값이 1인 도메인이 1개라도 있는 category 가 [네이버사이트,네이버블로그,네이버포스트,네이버지식인]인
서버를 검사하여, 경로[wcar]에 index.html의 날짜를 추출하는 프로그램

[수정 내용]


