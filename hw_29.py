from utils import (
    read_config,
    create_client,
    send_request,
    extract_answer,
    get_user_prompt,
    save_answer,
)

# Константы
CONFIG_FILE = "./config.json"
ANSWERS_FILE = "./answers.txt"
DEFAULT_MESSAGE = "Расскажи смешной анекдот про Git и обезьянку!"
SEPARATOR = "=" * 60


def main() -> None:
    """
    Основная точка входа программы.

    Оркестрирует вызовы функций из модуля utils.
    Обрабатывает все исключения и выводит понятные сообщения об ошибках.
    """
    try:
        # Чтение конфигурации
        config = read_config(CONFIG_FILE)

        # Создание клиента OpenAI
        client = create_client(config)

        # Получение промпта от пользователя
        prompt = get_user_prompt(DEFAULT_MESSAGE)

        # Отправка запроса к модели
        completion = send_request(client, config["model"], prompt)

        # Извлечение ответа модели
        answer = extract_answer(completion)

        # Вывод ответа в консоль
        print(f"\n{answer}\n")

        # Сохранение ответа в файл
        save_answer(prompt, answer, ANSWERS_FILE, SEPARATOR)

    except Exception as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
