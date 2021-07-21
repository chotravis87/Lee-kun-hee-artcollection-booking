# 고故 이건희 회장 기증 명품전 자동 예약 봇

**만든이유**: 엄마가 부탁함

**필수**: 크롬 브라우저 및 파이썬이 꼭 설치 되어 있어야 합니다!

**참고**: 시간대를 정확히 설정해주시기 바랍니다!

## 사용방법
*파이썬 3.9버전 미만은 작동 여부를 확인하지 않았습니다*

1. `pip3 install -r requirements.txt`

2. `booking.py`를 입맞에 맞게 수정합니다.

3. `python3 booking.py`

## 사용방법 (고급)

4명까지 예약 가능하며 2명이상 예약하실려면 두번쨰분의 **이름**과 **휴대폰번호**가 필요합니다 

_(계정 소유자분의 이름과 휴대폰번호는 자동으로 입력됩니다)_

예를 들어

2명을 예약하면 필요한 변수는

``name2``, ``number2``

3명을 예약하면 필요한 변수는

``name2``, ``number2``, ``name3``, ``number3``

입니다

## Requirements
* [Selenium](https://pypi.org/project/selenium/)
* [chromedriver_autoinstaller](https://pypi.org/project/chromedriver-autoinstaller/)

## 문제제기
이슈나 제안할 점은 여기로 제보해주시기 바랍니다 :)
[이슈 제보하기](https://github.com/chotravis87/Lee-kun-hee-artcollection-booking/issues)
