from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import datetime
import time
import menu as m
import controller as c
import campeonatos as camp
import options as o

# Criando os parâmetros de conexão e iniciando uma instância oculta do navegador
hoje = datetime.date.today()
inicio = time.time()
service = Service()
driver = webdriver.Chrome(service=service, options=o.chrome_options)

campeonato = c.mostrarMenuCampeonatos(camp.campeonatos)
print(f"Você escolheu: {campeonato['nome']}\n-----\n")

listaTimes = c.obterListaDeTimes(driver, campeonato)
timeEscolhido = c.mostrarMenuTimes(listaTimes)
print(f"Você escolheu: {timeEscolhido['nomeTime']}\n-----\n")

link = f"{timeEscolhido['link']}/todos-os-jogos?compet_id_jogos={campeonato['id']}&epoca_id=153&epoca_id_fim=153&edicao_id={campeonato['edicao']}"

c.obterListaDeJogos(driver, link, hoje, campeonato['nome'])
    
#Encerrando o driver e o programa
driver.quit()
fim = time.time()
tempo_total = (fim - inicio)/60

print(f'Tempo total de execução: {tempo_total:.2f} m')