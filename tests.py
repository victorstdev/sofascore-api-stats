import options as o
import menu as m
import campeonatos as cmp
import controller as c
from selenium.webdriver.common.by import By
           
campeonato = m.obter_escolha(cmp.campeonatos)
times = c.obterListaDeTimes(o.driver, campeonato)
time = m.obter_escolha(times)
link = f"{time['link']}/todos-os-jogos?compet_id_jogos={campeonato['id']}&epoca_id=153&epoca_id_fim=153&edicao_id={campeonato['edicao']}"

lista_de_jogos = c.obterListaDeJogos(o.driver, link, o.hoje, campeonato['nome'])