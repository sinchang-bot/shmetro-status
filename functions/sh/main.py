#!/usr/local/bin/python
# coding: utf-8

import requests
import os
import sqlite3

BOT_API_KEY = os.getenv('BOT_API_KEY')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

conn = sqlite3.connect('status.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS status
             (line integer, status integer)""")

def fetch_status():
  r = requests.post('http://service.shmetro.com/i/sm?method=doGetAllLineStatus')
  return r.json()

def send_message(text):
  url = 'https://api.telegram.org/bot' + BOT_API_KEY +'/sendMessage?chat_id=@' + CHANNEL_NAME + '&text=' + text
  requests.get(url)

def handle(event, context):
  try:
    status = fetch_status()
    for item in status:
      if item['status'] and item['status'] != '0':
        c.execute("SELECT * FROM status WHERE line=?", item['disLine'])
        conn.commit()
        if len(c.fetchall()) > 0:
          continue
        message = item['disLine'] + '号线运行出现异常，' + item['content']
        c.execute("INSERT INTO status VALUES (?, ?)", (item['disLine'], 1))
        conn.commit()
        send_message(message)
      else:
        c.execute("INSERT INTO status VALUES (?, ?)", (item['disLine'], 0))
        conn.commit()
    conn.close()
    return 'done'
  except Exception as e:
    print(e)
    return e