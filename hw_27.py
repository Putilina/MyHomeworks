"""
Игра "Города" с разбиением на функции.
"""

from cities import cities_list


def build_cities_set(cities_data: list[dict]) -> set[str]:
    """
    Извлекает названия городов из списка словарей и возвращает множество.

    Args:
        cities_data: Список словарей с информацией о городах.
                    Каждый словарь должен содержать ключ "name".

    Returns:
        Множество названий городов в нижнем регистре.
    """
    cities_set: set[str] = set()
    for city_dict in cities_data:
        city_name: str = city_dict["name"].lower()
        cities_set.add(city_name)
    return cities_set


def check_city_rules(previous_city: str, current_city: str) -> bool:
    """
    Проверяет, соблюдается ли правило игры "Города".

    Правило: следующий город должен начинаться на последнюю букву предыдущего.

    Args:
        previous_city: Название предыдущего города.
        current_city: Название текущего города.

    Returns:
        True, если правило соблюдено, иначе False.
    """
    return previous_city[-1].lower() == current_city[0].lower()


def get_last_letter(city: str, bad_letters: set[str] | None = None) -> str:
    """
    Возвращает последнюю букву города для поиска ответа.

    Если город заканчивается на "плохую" букву (из множества bad_letters),
    возвращает предпоследнюю букву. Иначе возвращает последнюю.

    Args:
        city: Название города.
        bad_letters: Множество букв, на которые нельзя ответить.
                    Если None, плохие буквы не учитываются.

    Returns:
        Буква для поиска ответа.
    """
    last_char: str = city[-1]
    if bad_letters and last_char in bad_letters and len(city) > 1:
        return city[-2]
    return last_char


def find_computer_city(available_cities: set[str], letter: str) -> str | None:
    """
    Находит подходящий город для компьютера.

    Args:
        available_cities: Множество доступных городов.
        letter: Буква, на которую должен начинаться город.

    Returns:
        Название найденного города или None, если подходящий город не найден.
    """
    for city in available_cities:
        if city[0] == letter:
            return city
    return None


def get_bad_letters(cities_set: set[str]) -> set[str]:
    """
    Определяет "плохие" буквы - те, на которые нельзя ответить.

    Args:
        cities_set: Множество всех городов.

    Returns:
        Множество букв, на которые нет городов в списке.
    """
    first_letters: set[str] = set()
    last_letters: set[str] = set()

    for city in cities_set:
        first_letters.add(city[0])
        last_letters.add(city[-1])

    return last_letters - first_letters


def main() -> None:
    """
    Главная функция игры "Города".
    Запускает и контролирует игровой процесс.
    """
    # Подготовка данных
    available_cities: set[str] = build_cities_set(cities_list)
    bad_letters: set[str] = get_bad_letters(available_cities)

    # Переменные состояния игры
    last_city: str = ""
    is_first_move: bool = True

    # Вывод правил
    print("Добро пожаловать в игру Города!")
    print("Правила:")
    print("- Введите название города")
    print("- Город должен начинаться на последнюю букву предыдущего")
    print("- Повторять города нельзя")
    print("- Для выхода введите 'стоп'\n")

    # Основной игровой цикл
    while True:
        # Ввод игрока
        player_input: str = input("Ваш ход: ").strip()
        player_city: str = player_input.lower()

        # Проверка на команду "стоп"
        if player_city == "стоп":
            print("Игра завершена. До свидания!")
            break

        # Проверка существования города
        if player_city not in available_cities:
            print(
                f"Ошибка! Города '{player_input}' нет в списке или он уже был использован."
            )
            print("Вы проиграли!")
            break

        # Проверка правила (кроме первого хода)
        if not is_first_move and not check_city_rules(last_city, player_city):
            print(f"Ошибка! Город должен начинаться на букву '{last_city[-1]}'")
            print("Вы проиграли!")
            break

        # Принятие хода игрока
        available_cities.remove(player_city)
        print(f"✓ Город '{player_input}' принят!")
        is_first_move = False

        # Ход компьютера
        needed_letter: str = get_last_letter(player_city, bad_letters)
        print(f"Компьютер ищет город на букву '{needed_letter}'...")

        computer_city: str | None = find_computer_city(available_cities, needed_letter)

        if computer_city is not None:
            last_city = computer_city
            available_cities.remove(computer_city)
            print(f"Компьютер: {computer_city.capitalize()}")
            print(f"Осталось городов: {len(available_cities)}\n")
        else:
            print(f"Компьютер не нашел город на букву '{needed_letter}'!")
            print("Поздравляем! Вы победили!")
            break

    print("Игра окончена. Спасибо за игру!")


# Запуск игры
main()
