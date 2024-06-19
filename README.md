# 웹 서버 모니터링 스크립트

URL의 상태를 모니터링하고, 오류가 발생 할 경우 Slack에 메시지 전송하는 프로그램

## 설정

**config.ini**: 동작 설정
   - `[Scheduler]`: 간격 설정
      - `[Unit] = seconds`: `seconds` or `minutes` or `hours`
      - `[Value] = 5` (5초 or 5분 or 5시간)
   - `[StopScheduler]`: 오류 발생 시 일정 횟수 이상 스케줄러 일시 정지 설정
   - `[TimeSettings]`: 특정 시간 URL 상태와 관계없이 Slack에 메시지 전송
   - `[URLs]`: 모니터링 URL과 이름 정의
   - `[Slack]`: Slack API 토큰과 메시지 전송할 채널 설정
     [Slack Bot 설정 방법](https://gentle-chokeberry-d27.notion.site/Slack-Bot-6d82a379470543f1990fd032ed24fb77?pvs=4)

## 사용 방법

1. **설치**:
   - ```pip install -r requirements.txt```

2. **구성**:
   - `config.ini` 모니터링 할 URL, Slack 인증 정보, 스케줄링 설정

3. **실행**:
   - 스크립트를 실행: ```python monitor.py```
   - 설정된 스케줄에 따라 모니터링이 시작됩니다.

## 주의 

짧은 시간에 많은 트래픽을 주면 해당서버에서 ip 차단 또는 디도스랑 유사한 행위가 될수 있으므로 넉넉한 간격으로 실행하시길 바랍니다.
