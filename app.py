# Import libraries
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tinydb import TinyDB
import schedule
import time
import requests


db = TinyDB('./db.json')
table = db.table('breakdown-counter')


def scraper():
    old_value = -1
    try:
        old_value = int(table.all()[-1]["value"])
    except:
        notify("ERROR", "DB error", 99)
    URL = "https://mental-breakdown-counter.s3.eu-central-1.amazonaws.com/index.html"

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        counter = int(soup.find('span', {"id": "breakdown-counter"}).getText())

        now = datetime.now()
        date_time = now.strftime("%Y/%m/%d-%H:%M:%S")

        table.insert({'date': date_time, 'value': counter})
        notify("Breakdown Counter", counter, 0)
        if(old_value < counter):
            notify("Breakdown Counter +1", "SEND HELP!!!", 99)
    except:
        notify("ERROR", "Scraper error", 99)


def notify(title, message, priority):
    try:
        url = 'http://notifications.wabyte.com/message?token=AR9_BD_Mz6IeHTC'
        d = {'title': title,
             "message": message,
             "priority": priority}
        requests.post(url, data=d)
    except:
        print("ERROR sending notification")


schedule.every(10).minutes.do(scraper)

scraper()
while 1:
    schedule.run_pending()
    time.sleep(1)
