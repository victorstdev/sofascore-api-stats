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
        idJogo = jogo.get_attribute('id')
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
            "id": idJogo,
            "campeonato": campeonato,
            "nome": nomeTime,
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
    for jogo in listaDeJogos:
        jogo_existe_no_arquivo = checar_jogo_existente(campeonato, f'{nomeTime}.csv', jogo)
        if datetime.date.fromisoformat(jogo["dia"]) < hoje:
            if not jogo_existe_no_arquivo:
                obterDadosDoJogo(driver, jogo, tabela)
    if len(tabela) == 0:
        print('Nenhum jogo novo pra adicionar')
    else:
        salvarArquivo(campeonato, f'{nomeTime}.csv', tabela)

def checar_jogo_existente(local, arquivo, jogo):
    try:
        caminho_arquivo = os.path.join(local, arquivo)
        with open(caminho_arquivo, 'r', newline='') as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            for linha in leitor:
                if jogo["id"] in linha:
                    return True
        return False
    except:
        return False

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
        
        print(f"{jogo['nome']} {jogo['golsPro']}-{jogo['golsContra']} {jogo['adversario']}")
    except:
        print("Não encontrei o componente")
        jogo["except"] = True
    finally:
        tabela.append(jogo)
    
def salvarArquivo(local, arquivo, jogo):
    cabecalhos = jogo[0].keys()
    
    # checar se a pasta existe
    if not os.path.exists(local):
        try:
            os.mkdir(local)
        except OSError as e:
            print(f'Deu erro na criação da pasta {e}')
    
    caminho_arquivo = os.path.join(local, arquivo)
    
    # caso o arquivo não exista, cria o arquivo com o cabeçalho e depois adiciona as linhas
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'w', newline='') as arquivo_csv:
            csvWriter = csv.DictWriter(arquivo_csv, fieldnames = cabecalhos)
            csvWriter.writeheader()
    with open(caminho_arquivo, 'a', newline='') as arquivo_csv:
        csvWriter = csv.DictWriter(arquivo_csv, fieldnames = cabecalhos)
        csvWriter.writerows(jogo)            
    
    print(f'Arquivo CSV "{arquivo}" criado com sucesso.\n-----\n')

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
        times.append({"id": i, "nome": nomeTime, "link": link})
    
    return times