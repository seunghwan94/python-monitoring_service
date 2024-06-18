import requests
from slack_sdk import WebClient
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import configparser

def load_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def check_url(name, url):
    try:
        response = requests.get(url)
        # 상태 코드 확인
        if response.status_code == 200:
            status = f"{name} : O"
        else:
            status = f"{name} : X (returned status code: {response.status_code})"
    except requests.exceptions.RequestException as e:
        status = f"Failed to reach {url}: {e}"

    return status

def post_message(channel, text, SlackBotToken):
    client = WebClient(token=SlackBotToken)
    client.chat_postMessage(channel=channel, text=text)

def start_main(scheduler, config):
    global cnt

    urls = dict(config.items('URLs'))

    # 특정 시간 리스트
    special_times_str = config.get('TimeSettings', 'SpecialTimes')
    special_times = [time.strip() for time in special_times_str.split(',')]
    # 스케줄러 간격 설정
    value = int(config['StopScheduler']['Value'])
    stop_cnt = int(config['StopScheduler']['StopCnt'])
    # 슬랙
    SlackBotToken = config['Slack']['SlackBotToken']
    SlackBotChannel = config['Slack']['SlackBotChannel']

    msg = "#####################################\n 웹 서버 상태 #####################################\n\t\t\t"
    for name, url in urls.items():
        status = check_url(name, url)
        msg += status + '\n\t\t\t'

    current_time = datetime.datetime.now().strftime("%H:%M")

    # 특정시간엔 오류 여부와 상관없이 메시지 전송
    if current_time in special_times:
        post_message(SlackBotChannel, msg, SlackBotToken)

    elif 'Failed' in msg or ': X' in msg:
        post_message(SlackBotChannel, msg, SlackBotToken)
        cnt += 1

        if cnt >= stop_cnt:
            print('일시 중지')
            cnt = 0
            scheduler.pause_job('monitor')
            # date : 지정된 날짜 및 시간에 작업을 한 번 실행
            scheduler.add_job(restart_scheduler, 'date', run_date=datetime.datetime.now() + datetime.timedelta(minutes=value), args=[scheduler])

def restart_scheduler(scheduler):
    print('다시 시작')
    scheduler.resume_job('monitor')

if __name__ == "__main__":
    cnt = 0

    # APScheduler 설정
    scheduler = BlockingScheduler()
    # 설정 파일 로드
    config = load_config('config.ini')
    # 스케줄러 간격 설정
    unit = config['Scheduler']['Unit']
    value = int(config['Scheduler']['Value'])

    # start_main 함수를 주기적으로 실행
    scheduler.add_job(start_main, 'interval', **{unit: value}, id='monitor', kwargs={'scheduler': scheduler, 'config': config})

    try:
        print("모니터링 시작")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
