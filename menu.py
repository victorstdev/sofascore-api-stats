def show_menu(options):
  print('Choose an option')
  for id, item in enumerate(options, 1):
    print(f"{id}. {item['name']}")

def choose_option(options):
  while True:
    show_menu(options)
    try:
      choice = int(input('Enter the desired option: '))
      if 1 <= choice <= len(options):
        return options[choice - 1]
      else:
        print('Invalid option. Try again')
    except:
      print('Enter a valid value')