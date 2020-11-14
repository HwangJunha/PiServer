import schedule
import time

def job():
    print('working')
    
def job2():
    print('junha')


schedule.every().day.at("00:56").do(job2)
schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)