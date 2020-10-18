import os
import re
import sys
import time
import json
import datetime
import threading
import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib import request, parse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore, Back, Style

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def rover():
  # Reading config.ini
  print(Style.BRIGHT + 'Loading config.ini... ', end='')
  sys.stdout.flush()
  try:
    with open('config.ini') as f:
      config = configparser.ConfigParser()
      config.read_file(f)
  except IOError as e:
    print(Fore.RED + 'fail\n' + str(e))
    sys.exit()
  print(Fore.GREEN + 'OK')
  sys.stdout.flush()
  
  # Loading Selenium driver
  print(Fore.RESET + 'Loading driver... ', end='')
  sys.stdout.flush()
  try:
    driver = webdriver.Chrome(executable_path=config['rover']['driver'], options=chrome_options)
  except selenium.common.exceptions.WebDriverException as e:
    print(Fore.RED + 'fail\n' + str(e))
    sys.exit()
  print(Fore.GREEN + 'OK')
  sys.stdout.flush()
  
  # Loading login page
  print(Fore.RESET + 'Loading login page... ', end='')
  sys.stdout.flush()
  try:
    driver.get('https://www.ros-bot.com/user/login')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'edit-submit')))
  except selenium.common.exceptions.TimeoutException as e: 
    print(Fore.RED + 'fail\n' + str(e))
    sys.exit()
  print(Fore.GREEN + 'OK')
  sys.stdout.flush()
  
  # Attempting login
  print(Fore.RESET + 'Attempting login... ', end='')
  sys.stdout.flush()
  try:
    driver.find_element(By.ID, 'edit-name').send_keys(config['user']['id'])    
    driver.find_element(By.ID, 'edit-pass').send_keys(config['user']['pw'])
    driver.find_element(By.ID, 'edit-pass').submit()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/head/link[@rel='shortlink']")))
    usercode = re.search('\/user\/(\d{6})', driver.find_element(By.XPATH, "/html/head/link[@rel='shortlink']").get_attribute('href')).group(1)
  except:
    print(Fore.RED + 'fail')
    print(sys.exc_info()[0])
    sys.exit()
  print(Fore.GREEN + 'OK')
  sys.stdout.flush()
  
  crawler(driver, config, usercode, set())
  
def crawler(driver, config, code, timeline):
  # Crawling item info
  print(Fore.RESET + 'Crawling item info... ', end='')
  sys.stdout.flush()
  try:
    driver.get('https://www.ros-bot.com/user/' + code + '/bot-activity')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "edit-item-destination")))
    Select(driver.find_element(By.ID, 'edit-item-destination')).select_by_visible_text('Stashed')
    driver.find_element(By.ID, 'edit-item-destination').submit()
    # Getting timeline points
    timepoints = driver.find_elements(By.CSS_SELECTOR, 'div.timeline-item div.row')
    print(Fore.GREEN + 'OK')
    sys.stdout.flush()

    for point in timepoints:
      soup = BeautifulSoup(point.get_attribute('innerHTML'), 'html.parser')
      elem = soup.select_one('div.date').findAll(text=True, recursive=False)
      date = None
      # Identifying timeline point
      for el in elem:
        date = re.sub('\n', '', el).strip()
        if date: break
      # Getting timeline detail if new timeline appears
      if not timeline.issuperset({ date }):
        payload = { 'destination': config['user']['telegram'], 'date': date, 'contents': [] }
        timeline.add(date)
        items = soup.select_one('div.content').select('div p span')
        for item in items:
          payload['contents'].append({ 'title': item['data-title'], 'detail': re.sub('<br />\n', '\n', item['data-content']) })
          
        # Sending data to server
        print(Fore.RESET + 'Transmitting data... ', end='')
        sys.stdout.flush()
        try:
          req = request.Request('https://luftaquila.io/api/telepath/report', data=parse.urlencode(payload).encode())
          res = request.urlopen(req)
        except urllib.error.HTTPError as e:
          print(Fore.RED + 'fail')
          print(e)
          continue
        print(Fore.GREEN + 'OK')
        sys.stdout.flush()
        
  except:
    print(Fore.RED + 'fail')
    print(sys.exc_info()[0])
    sys.exit()
    
  try:
    target_time = datetime.datetime.now() + datetime.timedelta(0, int(config['rover']['refresh']))
    print(Fore.RESET + 'Waiting for next execution: ', end='')
    print(Fore.CYAN + str(target_time))
    while(target_time - datetime.datetime.now()).total_seconds() > 0 :
      print(Fore.RESET + '  Countdown: ', end='')
      print(Fore.CYAN + str(target_time - datetime.datetime.now()), end='\r')
      sys.stdout.flush()

    print(Fore.RESET + '  Countdown: ', end='')
    print(Fore.CYAN + '0:00:00.000000\n')
    sys.stdout.flush()
  except:
    print(Fore.RED + 'fail')
    print(sys.exc_info()[0])
    sys.exit()
    
  crawler(driver, config, code, timeline)
  #threading.Timer(int(config['rover']['refresh']), crawler, [driver, config, code, timeline]).start()

rover()