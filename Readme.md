# Документация

## Запуск программы
1. Установить необходимые библиотеки:
    - python-dotenv==1.0.0
    - SQLAlchemy==2.0.3
    - vk-api==11.9.9
2. Создать новый файл с именем '.env' и прописать там токены и пароли от БД
    - token_bot = '*****'
    - token = '*****'
    - pas_base = '*****'
3. Запустить файл main.py
4. Взаимодействие с ботом начинается с команды 'привет' в диалоге с сообществом.

## Список команд
1. 'привет' - бот выдаёт 'Привет' и предлагает найти друзей.
2. 'искать' - начинает поиск подходящих пользователей.
3. После нахождения подходящего пользователя,бот выводит информацию о нём и спрашивает, куда его добавить:
    - 'в избранное'
    - 'в чёрный список'
    - 'не добавлять'
4. 'остановить поиск' - бот останавливает поиск, для возобновления нужно нажать 'искать'.
5. 'показать изранных' - показывает список избранных.
6. 'пока' - отвечает 'Пока'.
7. Если ввести непонятную команду, бот выведет 'не поняла вашего ответа'.


