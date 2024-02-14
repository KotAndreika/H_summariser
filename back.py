from flask import Flask
from flask import request
import time
import requests
from threading import Thread

app = Flask('')

@app.route('/')
def home():
   return ('Hello, I know all')

def run():
  app.run(host='0.0.0.0', port=80)

def keep_alive():
  t = Thread(target=run)
  t.start()
