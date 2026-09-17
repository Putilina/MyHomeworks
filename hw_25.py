# Импорт списка городов из файла cities.py
from cities import cities_list

#  СОБИРАЕМ МНОЖЕСТВО ДОСТУПНЫХ ГОРОДОВ

available_cities = set()


for city_dict in cities_list:
    city_name = city_dict["name"]
    available_cities.add(city_name.lower())


#  ПОДГОТАВЛИВАЕМ ПЕРЕМЕННЫЕ ДЛЯ ИГРЫ

last_computer_city = ""

# Переменная флаг
is_first_move = True

#  ОСНОВНОЙ  ЦИКЛ ИГРЫ

print("Добро пожаловать в игру Города!")
print("\nПравила игры:")
print("- Введите название города: ")
print("- Город должен начинаться на последнюю букву предыдущего.")
print("- Повторять города нельзя.")
print("- Для выхода из игры введите 'стоп'.\n")


while True:
    
    player_input = input("Ваш ход: ")
    
    player_city = player_input.strip().lower()
    
    if player_city == "стоп":
        print("Игра завершена по вашему желанию. До свидания!")
        break  
    
    #  ПРОВЕРКИ ХОДА ЧЕЛОВЕКА

    if player_city not in available_cities:
        print(f"Ошибка! Города '{player_input}' нет в списке, или он уже был использован.")
        print("Вы проиграли!")
        break  
    
    # ПРОВЕРКА .Если это не первый ход, проверяем правило игры

    if not is_first_move:

        if player_city[0] != last_computer_city[-1]:
            print(f"Ошибка! Ваш город должен начинаться на букву '{last_computer_city[-1]}'!")
            print("Вы проиграли!")
            break  
    
    available_cities.remove(player_city)
    print(f"✓ Город '{player_input}' принят!")

    is_first_move = False
    

    # РЕАЛИЗУЕМ ХОД КОМПЬЮТЕРА

    needed_letter = player_city[-1]
    
    print(f"Компьютер ищет город на букву '{needed_letter}'...")
    
    computer_city = None 
    
    for city in available_cities:
        if city[0] == needed_letter:
            computer_city = city  
            break  
    

    if computer_city is not None:
        last_computer_city = computer_city
        available_cities.remove(computer_city)
        print(f"Компьютер называет город: {computer_city.capitalize()}")
        print(f"Осталось городов в игре: {len(available_cities)}\n")
        
    else:
        print(f"Компьютер не смог найти город на букву '{needed_letter}'!")
        print("Поздравляем! Вы победили! ")
        break  

# Сообщение о завершении игры
print("Игра окончена. Спасибо за игру!")