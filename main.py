"""
    asd
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Criando os parâmetros de conexão e iniciando uma janela do Chrome maximizada
service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)


#Encerrando o driver e o programa
driver.quit()