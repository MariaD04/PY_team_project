from random import randrange
from config import TOKEN_BOT, TOKEN
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from table.vkinder_base import show_list_favorites, show_links_user, load_client
from table.vkinder_base import check_client_existing, check_clientuser_exist
from interaction.button import create_keyboard_first, create_keyboard_second
from interaction.vk_loader import VKLoader


vk = VkApi(token=TOKEN_BOT)
longpoll = VkLongPoll(vk)
vkinder = VKLoader(TOKEN)


def write_msg(user_id, message=None, foto=None, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
        'attachment': foto,
        'keyboard': keyboard
    }
    if keyboard is not None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post
    vk.method('messages.send', post)


def interaction():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower()
                user_id = event.user_id
                if request == 'привет':
                    write_msg(
                        user_id,
                        message=f"Привет, {vkinder.get_user_params(user_id)[0]['first_name']}"
                    )
                    if check_client_existing(vkinder.get_user_params(user_id)[0]):
                        load_client(vkinder.get_user_params(user_id)[0])
                    write_msg(
                        user_id,
                        message='Найдем вам друзей?',
                        keyboard=create_keyboard_first()
                    )
                elif request in ['искать']:
                    flag = True
                    dict_client = vkinder.get_user_params(user_id)[0]
                    for item in vkinder.get_vk_list(vkinder.get_user_params(user_id)[1]):
                        if flag:
                            status = ''
                            dict_user = {
                                'id_user': item['id'],
                                'first_name': item['first_name'],
                                'last_name': item['last_name'],
                                'link_profile': 'https://vk.com/' + item['domain']
                            }
                            if 'city' in item:
                                dict_user['city'] = item['city']['title']
                            else:
                                dict_user['city'] = 'Не указан'
                            if 'sex' in item:
                                dict_user['gender'] = item['sex']
                            else:
                                dict_user['gender'] = None
                            if 'bdate' in item:
                                dict_user['age'] = vkinder.get_age(item['bdate'])
                            else:
                                dict_user['age'] = None

                            list_links = vkinder.get_foto(dict_user['id_user'])
                            if check_clientuser_exist(
                                    dict_client['id_client'],
                                    dict_user['id_user']) == 2:
                                continue
                            if check_clientuser_exist(
                                    dict_client['id_client'],
                                    dict_user['id_user']) == 1:
                                status = '❤️В избранном'
                            foto = None
                            status_text = '(закрытый профиль)'
                            if list_links != []:
                                foto = {','.join(vkinder.get_foto(dict_user['id_user']))}
                                status_text = ''
                            write_msg(
                                user_id,
                                message={
                                    f"{dict_user['first_name']} {dict_user['last_name']} {status} {status_text}\n"
                                    f"{dict_user['city']}, {str(dict_user['age'])} лет \n"
                                    f"Ссылка на профиль {dict_user['link_profile']}"
                                },
                                foto=foto
                            )
                            write_msg(
                                user_id,
                                message='Куда добавить человека?',
                                keyboard=create_keyboard_second()
                            )

                            for this_event in longpoll.listen():
                                if this_event.type == VkEventType.MESSAGE_NEW:
                                    if this_event.to_me:
                                        request = this_event.text.lower()
                                        if request == 'в избранное':
                                            status = 1
                                            vkinder.load_base(status, dict_user, dict_client, list_links)
                                            write_msg(
                                                user_id,
                                                message=f"{dict_user['first_name']} {dict_user['last_name']} теперь в списке избранных"
                                            )
                                            break
                                        elif request == 'в черный список':
                                            status = 2
                                            vkinder.load_base(status, dict_user, dict_client, list_links)
                                            write_msg(
                                                user_id,
                                                message=f"{dict_user['first_name']} {dict_user['last_name']} теперь в черном списке"
                                            )
                                            break
                                        elif request == 'не добавлять':
                                            break
                                        elif request == 'остановить поиск':
                                            flag = False
                                            write_msg(
                                                user_id,
                                                message='Поиск остановлен, для возобновления жми Искать'
                                            )
                                            break
                        else:
                            break
                elif request == 'показать избранных':
                    for item in show_list_favorites(vkinder.get_user_params(user_id)[0]):
                        foto = None
                        if show_links_user(item[0]) != [None]:
                            foto = {','.join(show_links_user(item[0]))}
                        write_msg(
                            user_id,
                            message={
                                f"{item[1]} {item[2]} \n"
                                f"{str(item[4])}, {str(item[5])} лет \n"
                                f"Ссылка на профиль: {item[3]}"},
                            foto=foto)
                    write_msg(user_id, message='Продолжим? жми Искать')

                elif request in ['пока']:
                    write_msg(user_id, message='Пока((')
                else:
                    write_msg(user_id, message='Не поняла вашего ответа...')
