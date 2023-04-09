from vkinder_base import show_list_favorites, load_client, load_user, load_clientuser, load_user_links
from vkinder_base import check_client_existing, check_clientuser_exist, check_user_existing
# клиент начинает диалог с ботом

dict_client = {                         #бот формирует словарь с данными клиента
    'id_client': 10,
    'first_name': 'Svetlana',
    'last_name': 'Petranova',
    'link_profile': 'https:\\vk\id_used10',
    'city': 'Moskow',
    'gender': 1
}
#проверка существования клиента в базе.
# Если клиент есть, то проверяется актуальность данных и при необходимости данные обновляются
if check_client_existing(dict_client):
    load_client(dict_client)        #если нет в базе, то добавить

# поиск потенциального партнера
#бот формирует словарь с данными о партнере
dict_user = {
    'id_user': 12,
    'first_name': 'Vasily',
    'last_name': 'Ivanov',
    'link_profile': 'https:\\vk\id_user12',
    'city': 'Perm',
    'gender': 2
}
#бот формирует список ссылок на 3 фотографии из профиля
list_links = ['https:\\foto1', 'https:\\foto2', 'https:\\foto3']

#проверяем на отсутствие партнера в ЧС, получаем разрешение на показ
if check_clientuser_exist(dict_client['id_client'], dict_user['id_user']) == 2:
    print('Не показывать, ищем следующего')

#если получено разрешение, показываем клиенту партнера, если нет, то переходим к другому потенциальному партнеру

flag = 1  #сигнал от бота о том, что клиент сделал пометку (избранное или ЧС)
dict_user['status'] = 1 # в словарь дописывается поле статус (1- избранное, 2 - черный список)

#запись данных в БД
if flag == 1:
    if check_clientuser_exist(dict_client['id_client'], dict_user['id_user']) == 1:
        #если партнер для данного клиента есть в БД, обновит при необходимости информацию
        check_user_existing(dict_user, list_links)
    elif check_clientuser_exist(dict_client['id_client'], dict_user['id_user']) == 0:
        #если партнера для данного клиента нет в промежуточной таблице связи клиента и партнера
        if check_user_existing(dict_user, list_links):
            #если партнер есть в базе для других клиентов, обновит при необходимости данные или загрузит
            #нового партнера для данного клиента
            load_user(dict_user)
            load_user_links(dict_user['id_user'], list_links)
        #запишет данные в промежуточную таблицу, связь клиента и партнера
        load_clientuser(dict_client['id_client'], dict_user['id_user'])

print(show_list_favorites(dict_client)) #формирует список кортежей с партнерами из избранного для данного клиента






