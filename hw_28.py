# Первые декораторы — проверка пароля, декоратор с параметрами, `Callable` и исключения

from typing import Callable

users: list[dict[str, str]] = []

# ПРОСТОЙ ДЕКОРАТОР password_checker


def password_checker(func: Callable) -> Callable:
    """
    Простой декоратор для проверки пароля перед вызовом функции.

    Проверяет:
    - длина не менее 8 символов
    - наличие хотя бы одной цифры
    - наличие хотя бы одной заглавной буквы
    - наличие хотя бы одной строчной буквы

    Args:
        func: Декорируемая функция (ожидается, что она принимает пароль)

    Returns:
        Функция-обёртка, которая проверяет пароль перед вызовом func

    Примечание:
        Это "простая" версия декоратора, которая возвращает строку с ошибкой
        вместо того, чтобы выбрасывать исключение.
    """

    def wrapper(password: str) -> str:
        """
        Внутренняя функция-обёртка, выполняющая проверку пароля.

        Args:
            password: Пароль для проверки

        Returns:
            - Если пароль корректный: результат вызова исходной функции
            - Если пароль некорректный: строка с сообщением об ошибке
        """
        # Собираем все ошибки в список для понятного сообщения
        errors = []

        # Проверка 1: длина пароля
        if len(password) < 8:
            errors.append("Пароль должен содержать минимум 8 символов")

        # Проверка 2: наличие цифры
        if not any(char.isdigit() for char in password):
            errors.append("Пароль должен содержать хотя бы одну цифру")

        # Проверка 3: наличие заглавной буквы
        if not any(char.isupper() for char in password):
            errors.append("Пароль должен содержать хотя бы одну заглавную букву")

        # Проверка 4: наличие строчной буквы
        if not any(char.islower() for char in password):
            errors.append("Пароль должен содержать хотя бы одну строчную букву")

        # Если есть ошибки - не вызываем исходную функцию
        if errors:
            return "Ошибка: " + "; ".join(errors)

        # Если все проверки пройдены - вызываем исходную функцию
        return func(password)

    return wrapper


# ЧАСТЬ 2. ФУНКЦИЯ register_user


@password_checker
def register_user(password: str) -> str:
    """
    Регистрирует пользователя с проверкой пароля.

    Args:
        password: Пароль для регистрации

    Returns:
        Сообщение об успешной регистрации или ошибке

    Примечание:
        В этой части мы НЕ сохраняем пользователя в список.
        Просто демонстрируем работу декоратора.
    """
    # Функция выполнится ТОЛЬКО если декоратор пропустил проверку
    return "Пользователь успешно зарегистрирован"


# ЧАСТЬ 3. ДЕКОРАТОР С ПАРАМЕТРАМИ password_validator


def password_validator(
    min_length: int = 8,
    min_uppercase: int = 1,
    min_lowercase: int = 1,
    min_digits: int = 1,
    min_special_chars: int = 1,
) -> Callable:
    """
    Декоратор с параметрами для гибкой проверки пароля.

    Это ВНЕШНЯЯ функция, которая принимает параметры для настройки правил.
    Она возвращает НАСТОЯЩИЙ декоратор.

    Args:
        min_length: Минимальная длина пароля
        min_uppercase: Минимальное количество заглавных букв
        min_lowercase: Минимальное количество строчных букв
        min_digits: Минимальное количество цифр
        min_special_chars: Минимальное количество специальных символов

    Returns:
        Декоратор (функция, которая принимает функцию и возвращает обёртку)

    Примечание:
        Специальные символы: !@#$%^&*()_+-=[]{}|;:,.<>?
    """
    # Определяем множество специальных символов
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def decorator(func: Callable) -> Callable:
        """
        НАСТОЯЩИЙ декоратор, который применяет правила проверки.

        Это СРЕДНЯЯ функция, которая принимает декорируемую функцию.

        Args:
            func: Декорируемая функция

        Returns:
            Функция-обёртка
        """

        def wrapper(username: str, password: str) -> str:
            """
            ВНУТРЕННЯЯ функция-обёртка, выполняющая проверку.

            Args:
                username: Имя пользователя
                password: Пароль для проверки

            Returns:
                Результат вызова функции

            Raises:
                ValueError: Если пароль не соответствует требованиям
            """
            errors = []

            # Проверка длины
            if len(password) < min_length:
                errors.append(f"Пароль должен содержать минимум {min_length} символов")

            # Проверка количества заглавных букв
            uppercase_count = sum(1 for char in password if char.isupper())
            if uppercase_count < min_uppercase:
                errors.append(
                    f"Пароль должен содержать минимум {min_uppercase} заглавную букву(ы)"
                )

            # Проверка количества строчных букв
            lowercase_count = sum(1 for char in password if char.islower())
            if lowercase_count < min_lowercase:
                errors.append(
                    f"Пароль должен содержать минимум {min_lowercase} строчную букву(ы)"
                )

            # Проверка количества цифр
            digits_count = sum(1 for char in password if char.isdigit())
            if digits_count < min_digits:
                errors.append(f"Пароль должен содержать минимум {min_digits} цифру(ы)")

            # Проверка количества специальных символов
            special_count = sum(1 for char in password if char in special_chars)
            if special_count < min_special_chars:
                errors.append(
                    f"Пароль должен содержать минимум {min_special_chars} специальный(е) символ(ы)"
                )

            # Если есть ошибки - поднимаем исключение
            if errors:
                raise ValueError("Ошибка валидации пароля: " + "; ".join(errors))

            # Если все проверки пройдены - вызываем функцию
            return func(username, password)

        return wrapper

    return decorator


# ЧАСТЬ 4. ДЕКОРАТОР username_validator


def username_validator(func: Callable) -> Callable:
    """
    Декоратор для проверки имени пользователя.

    Проверяет:
    - имя не пустое
    - имя не содержит пробелов

    Args:
        func: Декорируемая функция

    Returns:
        Функция-обёртка

    Raises:
        ValueError: Если имя пользователя некорректно
    """

    def wrapper(username: str, password: str) -> str:
        """
        Обёртка, выполняющая проверку имени пользователя.

        Args:
            username: Имя пользователя для проверки
            password: Пароль пользователя

        Returns:
            Результат вызова функции

        Raises:
            ValueError: Если имя пользователя некорректно
        """
        # Проверка на пустое имя
        if not username or username.isspace():
            raise ValueError(
                "Ошибка валидации имени: Имя пользователя не может быть пустым"
            )

        # Проверка на наличие пробелов в имени
        if " " in username:
            raise ValueError(
                "Ошибка валидации имени: Имя пользователя не должно содержать пробелы"
            )

        # Если проверки пройдены - вызываем функцию
        return func(username, password)

    return wrapper


# ЧАСТЬ 5. ФУНКЦИЯ register_account С ДВУМЯ ДЕКОРАТОРАМИ


@username_validator
@password_validator(
    min_length=8, min_uppercase=1, min_lowercase=1, min_digits=1, min_special_chars=1
)
def register_account(username: str, password: str) -> str:
    """
    ОСНОВНАЯ функция регистрации аккаунта.

    Args:
        username: Имя пользователя
        password: Пароль пользователя

    Returns:
        Сообщение об успешной регистрации

    Raises:
        ValueError: При ошибках валидации (выбрасываются декораторами)

    Примечание:
        Функция выполняется ТОЛЬКО если:
        - Имя прошло проверку в username_validator
        - Пароль прошёл проверку в password_validator
    """
    # Добавляем пользователя в глобальный список users
    # Сохраняем и имя, и пароль
    users.append({"username": username, "password": password})

    # Возвращаем сообщение об успехе
    return f"Пользователь '{username}' успешно зарегистрирован"


# ЧАСТЬ 6. ПРОВЕРКА РАБОТЫ ЧЕРЕЗ try/except


def test_registration() -> None:
    """
    Тестирование функции регистрации с различными данными.
    """
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ СИСТЕМЫ РЕГИСТРАЦИИ")
    print("=" * 60)

    # Проверка 1: Успешная регистрация

    print("\n1. Успешная регистрация:")
    try:
        result = register_account("ivan", "SecureP@ss123")
        print(f"  ✓ {result}")
    except ValueError as e:
        print(f"  ✗ {e}")

    # Проверка 2: Имя с пробелом

    print("\n2. Регистрация с пробелом в имени:")
    try:
        result = register_account("ivan petrov", "SecureP@ss123")
        print(f"  ✓ {result}")
    except ValueError as e:
        print(f"  ✗ {e}")

    # Проверка 3: Слишком короткий пароль

    print("\n3. Регистрация с коротким паролем:")
    try:
        result = register_account("alex", "Short1!")
        print(f"  ✓ {result}")
    except ValueError as e:
        print(f"  ✗ {e}")

    # Проверка 4: Пароль без цифр

    print("\n4. Регистрация с паролем без цифр:")
    try:
        result = register_account("maria", "NoDigits@!")
        print(f"  ✓ {result}")
    except ValueError as e:
        print(f"  ✗ {e}")

    # Проверка 5: Пароль без заглавных букв

    print("\n5. Регистрация с паролем без заглавных букв:")
    try:
        result = register_account("petr", "nolower@123")
        print(f"  ✓ {result}")
    except ValueError as e:
        print(f"  ✗ {e}")

    # Проверка 6: Пароль без специальных символов

    print("\n6. Регистрация с паролем без специальных символов:")
    try:
        result = register_account("elena", "NoSpecial123")
        print(f"  ✓ {result}")
    except ValueError as e:
        print(f"  ✗ {e}")

    # Проверка 7: Пустое имя пользователя

    print("\n7. Регистрация с пустым именем:")
    try:
        result = register_account("", "SecureP@ss123")
        print(f"  ✓ {result}")
    except ValueError as e:
        print(f"  ✗ {e}")

    # Проверка 8: Вторая успешная регистрация
    # Добавляем ещё одного пользователя
    print("\n8. Вторая успешная регистрация:")
    try:
        result = register_account("dmitry", "StR0ngP@ssw0rd!")
        print(f"  ✓ {result}")
    except ValueError as e:
        print(f"  ✗ {e}")


# ЧАСТЬ 7. ВЫВОД ИТОГОВОГО СПИСКА ПОЛЬЗОВАТЕЛЕЙ


def print_users() -> None:
    """
    Вывод списка зарегистрированных пользователей.
    """
    print("\n" + "=" * 60)
    print("СПИСОК ЗАРЕГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ")
    print("=" * 60)

    # Проверяем, есть ли пользователи в списке
    if not users:
        print("  Список пользователей пуст")
    else:
        # Выводим всех пользователей с нумерацией
        for i, user in enumerate(users, 1):
            print(f"  {i}. Имя: {user['username']}, Пароль: {user['password']}")
    print()


# ЗАПУСК ВСЕХ ТЕСТОВ

if __name__ == "__main__":
    # ТЕСТИРОВАНИЕ ПРОСТОГО ДЕКОРАТОРА
    # Здесь мы проверяем работу password_checker на функции register_user
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ПРОСТОГО ДЕКОРАТОРА PASSWORD_CHECKER")
    print("=" * 60)

    # Проверка 1.1: Пароль короче 8 символов
    print("\n1. Пароль короче 8 символов:")
    result = register_user("Short1!")
    print(f"  Результат: {result}")

    # Проверка 1.2: Пароль без цифры
    print("\n2. Пароль без цифры:")
    result = register_user("NoDigitsHere")
    print(f"  Результат: {result}")

    # Проверка 1.3: Пароль без заглавной буквы
    print("\n3. Пароль без заглавной буквы:")
    result = register_user("nocapital1")
    print(f"  Результат: {result}")

    # Проверка 1.4: Корректный пароль
    print("\n4. Корректный пароль:")
    result = register_user("ValidP@ss123")
    print(f"  Результат: {result}")

    print("\n")

    # ТЕСТИРОВАНИЕ ОСНОВНОЙ СИСТЕМЫ РЕГИСТРАЦИИ

    test_registration()

    # ВЫВОД ИТОГОВОГО СПИСКА ПОЛЬЗОВАТЕЛЕЙ
    print_users()
