from random import randrange
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_loader import VKLoader
from vkinder_base import show_list_favorites, show_links_user, load_client
from vkinder_base import check_client_existing, check_clientuser_exist
from button import create_keyboard_first, create_keyboard_second


with open(r'D:\Python\Python now\VKinder\token.txt', encoding='utf-8') as file:
    token_bot = file.readline().rstrip('\n') # токен бот-приложения
    user_id_test = file.readline().rstrip('\n') #клиент для которого ищем пару
    access_token = file.readline().rstrip('\n') # токен личный

vk = VkApi(token=token_bot)
longpoll = VkLongPoll(vk)

vkinder = VKLoader(access_token)

def write_msg(user_id, message=None, foto=None, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
        'attachment': foto,
        'keyboard': keyboard
    }
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post
    vk.method('messages.send', post)

if __name__ == '__main__':

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower()
                user_id = event.user_id
                if request == "privet":
                    write_msg(user_id, message=f"Привет, {vkinder._get_user_params(user_id)[0]['first_name']}")
                    if check_client_existing(vkinder._get_user_params(user_id)[0]):
                        load_client(vkinder._get_user_params(user_id)[0])
                    write_msg(user_id, message=f'Найдем вам друзей?', keyboard=create_keyboard_first())
                elif request in ['искать']:
                    flag = True
                    dict_client = vkinder._get_user_params(user_id)[0]
                    for item in vkinder.get_vk_list(vkinder._get_user_params(user_id)[1]):
                        if flag:
                            dict_user = {
                                'id_user': item['id'],
                                'first_name': item['first_name'],
                                'last_name': item['last_name'],
                                'link_profile': 'https://vk.com/' + item['domain']
                            }
                            if 'city' in item:
                                dict_user['city'] = item['city']['title']
                            else:
                                dict_user['city'] = None
                            if 'sex' in item:
                                dict_user['gender'] = item['sex']
                            else:
                                dict_user['gender'] = None
                            if 'bdate' in item:
                                dict_user['age'] = vkinder._get_age(item['bdate'])
                            else:
                                dict_user['age'] = None

                            list_links = vkinder.get_foto(dict_user['id_user'])
                            if check_clientuser_exist(dict_client['id_client'], dict_user['id_user']) == 2:
                                continue
                            write_msg(user_id,
                                      message={f"{dict_user['first_name']} {dict_user['last_name']} \n"
                                               f"{dict_user['city']}, {str(dict_user['age'])} лет \n"
                                               f"Ссылка на профиль {dict_user['link_profile']}"},
                                      foto={','.join(vkinder.get_foto(dict_user['id_user']))})
                            write_msg(user_id, message=f'Куда добавить человека?', keyboard=create_keyboard_second())

                            for this_event in longpoll.listen():
                                if this_event.type == VkEventType.MESSAGE_NEW:
                                    if this_event.to_me:
                                        request = this_event.text.lower()
                                        #print(request)
                                        if request == 'в избранное':
                                            status = 1
                                            vkinder._load_base(status, dict_user, dict_client, list_links)
                                            write_msg(user_id, message=f'Пользователь занесён в список избранных')
                                            break
                                        elif request == 'в черный список':
                                            status = 2
                                            vkinder._load_base(status, dict_user, dict_client, list_links)
                                            write_msg(user_id, message=f'Пользователь занесён в черный список')
                                            break
                                        elif request == 'не добавлять':
                                            break
                                        elif request == 'остановить поиск':
                                            flag = False
                                            write_msg(user_id, message=f'Поиск остановлен, для возобновления жми Искать')
                                            break
                        else:
                            break


                elif request == 'показать избранных':
                    for item in show_list_favorites(vkinder._get_user_params(user_id)[0]):
                        if show_links_user(item[0]) == [None]:
                            write_msg(user_id, message={f"{item[1]} {item[2]} \n"
                                                        f"{str(item[4])}, {str(item[5])} лет \n"
                                                        f"Ссылка на профиль: {item[3]}"})
                        else:
                            write_msg(user_id, message={f"{item[1]} {item[2]} \n"
                                                        f"{str(item[4])}, {str(item[5])} лет \n"
                                                        f"Ссылка на профиль: {item[3]}"},
                                                 foto={','.join(show_links_user(item[0]))})
                    write_msg(user_id, message='Продолжим? жми Искать')

                elif request in ['пока']:
                    write_msg(event.user_id, message="Пока((")
                else:
                    write_msg(event.user_id, message="Не поняла вашего ответа...")
