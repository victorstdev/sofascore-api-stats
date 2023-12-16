def exibir_menu(opcoes):
  print('Escolha sua opção')
  for id, item in enumerate(opcoes, 1):
    print(f"{id}. {item['nome']}")

def obter_escolha(opcoes):
  while True:
    exibir_menu(opcoes)
    try:
      escolha = int(input('Digite o número da opção desejada: '))
      if 1 <= escolha <= len(opcoes):
        return opcoes[escolha - 1]
      else:
        print('Opção inválida. Tente novamente')
    except:
      print('Digite um valor válido')