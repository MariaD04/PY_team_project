from random import randrange
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_loader import VKLoader
from vkinder_base import show_list_favorites, show_links_user, load_client
from vkinder_base import check_client_existing, check_clientuser_exist
from button import create_keyboard_first, create_keyboard_second


with open(r'C:\Users\Home\Desktop\Speshilov\Python\VKinder\token.txt', encoding='utf-8') as file:
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
        'keyboard': keyboard,
        'attachment': foto
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
                        load_client(vkinder._get_user_params(user_id)[0])  # если нет в базе, то добавить
                    write_msg(user_id, message=f'Найдем вам друзей?', keyboard=create_keyboard_first())
                elif request in ['start_search', 'next_search']:
                    write_msg(user_id, message='Search')
                    # dict_client = vkinder._get_user_params(user_id)[0]
                    # for item in vkinder.get_vk_list(vkinder._get_user_params(user_id)[1]):
                    #     dict_user = {
                    #         'id_user': item['id'],
                    #         'first_name': item['first_name'],
                    #         'last_name': item['last_name'],
                    #         'link_profile': 'https://vk.com/' + item['domain']
                    #     }
                    #     if 'city' in item:
                    #         dict_user['city'] = item['city']['title']
                    #     else:
                    #         dict_user['city'] = None
                    #     if 'sex' in item:
                    #         dict_user['gender'] = item['sex']
                    #     else:
                    #         dict_user['gender'] = None
                    #     if 'bdate' in item:
                    #         dict_user['age'] = vkinder._get_age(item['bdate'])
                    #     else:
                    #         dict_user['age'] = None
                    #
                    #     list_links = vkinder.get_foto(dict_user['id_user'])
                    #     if check_clientuser_exist(dict_client['id_client'], dict_user['id_user']) == 2:
                    #         # print('Не показывать, ищем следующего')
                    #         continue
                    #
                    #     write_msg(user_id, {item['first_name'] + ' ' + item['last_name']},
                    #               {','.join(vkinder.get_foto(item['id']))})
                    #     write_msg(user_id, {str(dict_user['city']) + ', ' + str(dict_user['age']) + ' лет'})
                    #     write_msg(user_id, f"Ссылка на профиль {dict_user['link_profile']}")
                    #     write_msg(user_id, f'Занести пользователя в список избранных?',
                    #               keyboard=create_keyboard_second())
                    #     for this_event in longpoll.listen():
                    #         if this_event.type == VkEventType.MESSAGE_NEW:
                    #             if this_event.to_me:
                    #                 if request == 'да':
                    #                     status = 1
                    #                     vkinder._load_base(status, dict_user, dict_client, list_links)
                    #                     write_msg(user_id, f'Пользователь занесён в список избранных')
                    #                     #write_msg(user_id, f'Смотрим дальше?')
                    #                     break
                    #                 elif request == 'нет':
                    #                     break

                    # random_list = vkinder.dict_user_list(user_id)  # перебор потенциальной пары и добавление в БД
                    #
                    # write_msg(user_id, {random_list[0]['first_name'] + ' ' + random_list[0]['last_name']},
                    #           {','.join(vkinder.get_foto(random_list[0]['id_user']))})
                    # write_msg(user_id, {random_list[0]['city'] + ', ' + str(random_list[0]['age']) + ' лет'})
                    # write_msg(user_id, f"Ссылка на профиль {random_list[0]['link_profile']}")
                    # write_msg(user_id, f'Занести пользователя в список избранных?')

                        # for this_event in longpoll.listen():
                        #     if this_event.type == VkEventType.MESSAGE_NEW:
                        #         if this_event.to_me:
                        #             # write_msg(user_id, f'Занести пользователя в список избранных?',
                        #             #           keyboard=create_keyboard_second())
                        #             message = this_event.text
                        #
                        #             if message == 'да':
                        #                 status = 1
                        #                 vkinder._load_base(status, dict_user, dict_client, list_links)
                        #                 write_msg(user_id, f'Пользователь занесён в список избранных')
                        #                 write_msg(user_id, f'Смотрим дальше?')
                        #
                        #                 for this_event in longpoll.listen():
                        #                     if this_event.type == VkEventType.MESSAGE_NEW:
                        #                         if this_event.to_me:
                        #                             message = this_event.text
                        #
                        #                             if message == 'да':
                        #                                 break
                        #                 break
                                        # elif message == 'no':
                                        #     status = 2
                                        #     vkinder._load_base(status, random_list[0], random_list[1], random_list[2])
                                        #     write_msg(user_id, f'Пользователь добавлен в чс')
                                        #     write_msg(user_id, f'Смотрим дальше?')
                                        #     # bot.dislike_list(random_list)
                                        #     break
                                        #     #write_msg(user_id, f'Продолжить поиск?')


                elif request == 'show_favorite':
                    for item in show_list_favorites(vkinder._get_user_params(user_id)[0]):
                        write_msg(user_id, {item[1] + ' ' + item[2]}, {','.join(show_links_user(item[0]))})
                        write_msg(user_id, {'Ссылка на профиль: ' + item[3]})
                        write_msg(user_id, {str(item[4]) + ', ' + str(item[5]) + ' лет'})
                    write_msg(user_id, keyboard=create_keyboard_first())

                elif request in ['by']:
                    write_msg(event.user_id, message="Пока((")
                    break
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")
