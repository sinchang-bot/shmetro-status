import requests
import os

BOT_API_KEY = os.getenv('BOT_API_KEY')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

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
        message = item['disLine'] + '号线运行出现异常，' + item['content']
        send_message(message)
    return
  except Exception as e:
    print(e)
    return e
