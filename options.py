import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-proxy-certificate-handler")
chrome_options.page_load_strategy = 'eager'

hoje = datetime.date.today()
inicio = time.time()
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)