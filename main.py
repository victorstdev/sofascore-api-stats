import time
import controller as c
import menu as m
import campeonatos as camp
import options as o


campeonato = m.obter_escolha(camp.campeonatos)
listaTimes = c.obterListaDeTimes(o.driver, campeonato)
timeEscolhido = m.obter_escolha(listaTimes)
link = f"{timeEscolhido['link']}/todos-os-jogos?compet_id_jogos={campeonato['id']}&epoca_id=153&epoca_id_fim=153&edicao_id={campeonato['edicao']}"
c.obterListaDeJogos(o.driver, link, o.hoje, campeonato['nome'])
#Encerrando o driver e o programa
o.driver.quit()
fim = time.time()
tempo_total = (fim - o.inicio)/60

print(f'Tempo total de execução: {tempo_total:.2f} m')