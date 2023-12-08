from selenium.webdriver.common.by import By
import datetime
import csv
import os

def obterListaDeJogos(driver, link, hoje, campeonato):
    driver.get(link)
    jogos = driver.find_elements(By.CSS_SELECTOR, '#team_games > table > tbody > tr.parent')
    nomeTime = driver.find_element(By.TAG_NAME, 'h1').text
    listaDeJogos = []
    tabela = []
    
    # armazenando os links em uma lista
    for jogo in jogos:
        dia = jogo.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
        local = jogo.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text
        adversario = jogo.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
        placarFull = jogo.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text
        
        if placarFull == "ADI":
            pass
        else:
            placar = placarFull.split('-')
            
        if local == "(C)":
            golsPro = placar[0]
            golsContra = placar[1]
        else:
            golsPro = placar[1]
            golsContra = placar[0]
        
        resultado = jogo.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text
        linkJogo = jogo.find_element(By.CSS_SELECTOR, 'td:nth-child(6) > a').get_attribute('href')
        listaDeJogos.append({
            "campeonato": campeonato,
            "nomeTime": nomeTime,
            "linkJogo": linkJogo,
            "dia": dia,
            "local": local,
            "adversario": adversario,
            "resultado": resultado,
            "golsPro": golsPro,
            "golsContra": golsContra,
            "finalizacaoPro": 0,
            "finalizacaoContra": 0,
            "chuteAGolPro": 0,
            "chuteAGolContra": 0,
            "escanteios": 0,
            "cartoesAmarelos": 0,
            "cartoesVermelhos": 0,
            "except": False
        })
    # percorrendo essa lista armazenada
    for jogo in listaDeJogos:
        if datetime.date.fromisoformat(jogo["dia"]) < hoje:
            driver.get(jogo["linkJogo"])
            obterDadosDoJogo(driver, jogo, tabela)
    salvarArquivo(campeonato, f'{nomeTime}.csv', tabela)

def obterDadosDoJogo(driver, jogo, tabela):
    driver.get(jogo["linkJogo"])
    try:
        right_bar = driver.find_element(By.CSS_SELECTOR, "#page_rightbar > div:nth-child(3) > div > div")
        elemento_pai_finalizacoes = right_bar.find_element(By.XPATH, "//div[@class='box']//div[@class='verysmallheader' and text()='Chutes']/..")
        elemento_pai_chutes_a_gol = right_bar.find_element(By.XPATH, "//div[@class='box']//div[@class='verysmallheader' and text()='Chutes a gol']/..")
        elemento_pai_escanteios = right_bar.find_element(By.XPATH, "//div[@class='box']//div[@class='verysmallheader' and text()='Escanteios']/..")
        if jogo["local"] == "(C)":
            jogo["finalizacaoPro"] = int(elemento_pai_finalizacoes.find_element(By.XPATH, ".//div[@class='box']//div[1]").text)
            jogo["chuteAGolPro"] = int(elemento_pai_chutes_a_gol.find_element(By.XPATH, ".//div[@class='box']//div[1]").text)
            jogo["finalizacaoContra"] = int(elemento_pai_finalizacoes.find_element(By.XPATH, ".//div[@class='box']//div[4]").text)
            jogo["chuteAGolContra"] = int(elemento_pai_chutes_a_gol.find_element(By.XPATH, ".//div[@class='box']//div[4]").text)
        else:
            jogo["finalizacaoPro"] = int(elemento_pai_finalizacoes.find_element(By.XPATH, ".//div[@class='box']//div[4]").text)
            jogo["chuteAGolPro"] = int(elemento_pai_chutes_a_gol.find_element(By.XPATH, ".//div[@class='box']//div[4]").text)
            jogo["finalizacaoContra"] = int(elemento_pai_finalizacoes.find_element(By.XPATH, ".//div[@class='box']//div[1]").text)
            jogo["chuteAGolContra"] = int(elemento_pai_chutes_a_gol.find_element(By.XPATH, ".//div[@class='box']//div[1]").text)
                    
        jogo["cartoesAmarelos"] = len(right_bar.find_elements(By.XPATH, "//*[@id='game_report']//span[contains(@class, 'icn_zerozero') and contains(@class, 'yellow')]"))
        jogo["cartoesVermelhos"] = len(right_bar.find_elements(By.XPATH, "//*[@id='game_report']//span[contains(@class, 'icn_zerozero') and contains(@class, 'red')]"))
        jogo["escanteios"] = int(elemento_pai_escanteios.find_element(By.XPATH, ".//div[@class='box']//div[1]").text) + int(elemento_pai_escanteios.find_element(By.XPATH, ".//div[@class='box']//div[4]").text)
        
        print(f"{jogo['nomeTime']} {jogo['golsPro']}-{jogo['golsContra']} {jogo['adversario']}")
    except:
        print("Não encontrei o componente")
        jogo["except"] = True
    finally:
        tabela.append(jogo)
    
def salvarArquivo(local, arquivo, jogo):
    cabecalhos = jogo[0].keys()
    if not os.path.exists(local):
        try:
            os.mkdir(local)
        except OSError as e:
            print(f'Deu erro na criação da pasta {e}')
    with open(f'./{local}/{arquivo}', 'w', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=cabecalhos)
        
        # Escrever o cabeçalho
        escritor_csv.writeheader()
        
        # Escrever os dados
        escritor_csv.writerows(jogo)
    print(f'Arquivo CSV "{arquivo}" criado com sucesso.\n-----\n')

def mostrarMenuCampeonatos(campeonatos):
    print("Escolha um campeonato:")
    for id, campeonato in enumerate(campeonatos, 1):
        print(f"{id}. {campeonato['nome']}")
    campeonatoEscolhido = int(input('Digite o ID do campeonato: '))
    return campeonatos[campeonatoEscolhido - 1]

def obterListaDeTimes(driver, campeonato):
    # acessar o link do campeonato
    driver.get(campeonato["link"])
    # obter a lista de times (não fiz em ordem alfabética ainda, tá na ordem da classificação)
    tabela = driver.find_element(By.ID, "DataTables_Table_0")
    tabelaTbody = tabela.find_element(By.TAG_NAME, 'tbody')
    tabelaTr = tabelaTbody.find_elements(By.TAG_NAME, 'tr')
    times = []

    # pra cada time, eu pego o nome e o link dele pra armazenar na lista de times

    for i, coluna in enumerate(tabelaTr, start=1):
        nomeTime = coluna.find_element(By.CSS_SELECTOR, "td:nth-child(3) > a").text
        link = coluna.find_element(By.CSS_SELECTOR, "td:nth-child(3) > a").get_attribute('href').split("?")[0]
        times.append({"id": i, "nomeTime": nomeTime, "link": link})
    
    return times

def mostrarMenuTimes(times):
    print('Escolha o time: ')
    
    for i, time in enumerate(times, 1):
        print(f"{i}. {time['nomeTime']}")
    id = int(input('Digite o número do time desejado:'))
    
    return times[id - 1]