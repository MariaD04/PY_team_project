from random import randrange
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_loader import VKLoader
from vkinder_base import show_list_favorites, load_client, load_user, load_clientuser, load_user_links
from vkinder_base import check_client_existing, check_clientuser_exist, check_user_existing
from button import send_

with open(r'D:\Python\Python now\VKinder\token.txt', encoding='utf-8') as file:
    token_bot = file.readline().rstrip('\n') # токен бот-приложения
   # user_id = file.readline().rstrip('\n') #клиент для которого ищем пару
    access_token = file.readline().rstrip('\n') # токен личный

vk = VkApi(token=token_bot)
longpoll = VkLongPoll(vk)

vkinder = VKLoader(access_token)

def write_msg(self, user_id, message):
    self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

if __name__ == '__main__':
    for event in vkinder.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower()
                user_id = str(event.user_id)
                msg = event.text.lower()
                send_(user_id, msg.lower())
                if request == "привет":
                    write_msg(user_id, f"Привет, {event.user_id}")
                    # проверка существования клиента в базе.
                    # Если клиент есть, то проверяется актуальность данных и при необходимости данные обновляются
                    if check_client_existing(vkinder._get_user_params(user_id)[0]):
                        load_client(vkinder._get_user_params(user_id)[0])  # если нет в базе, то добавить

                elif request in ['начать поиск', 'продолжить поиск', 'да']:
                    random_list = vkinder.dict_user_list(user_id)  # перебор потенциальной пары и добавление в БД
                    #random_list = []
                    # random_user_data = bot.random_user(bot._get_user_params(user_id), user_id)
                    # random_list.append(random_user_data)

                   # if random_list[0]['id_user'] not in chosen_users:
                    write_msg(user_id, {random_list[0]['first_name'] + ' ' + random_list[0]['last_name']},
                                  {','.join(vkinder.get_foto(random_list[0]['id_user']))})
                    write_msg(user_id, f"Ссылка на профиль {random_list[0]['link_profile']}")
                    write_msg(user_id, f'Занести пользователя в список избранных?')

                    for this_event in vkinder.longpoll.listen():
                        if this_event.type == VkEventType.MESSAGE_NEW:
                            if this_event.to_me:
                                message = this_event.text

                    if message == 'да':
                        status = 1
                        vkinder._load_base(status, random_list[0], random_list[1], random_list[2])
                        write_msg(user_id, f'Пользователь занесён в список избранных')
                        # bot.like_list(random_list)
                    elif message == 'нет':
                        status = 2
                        vkinder._load_base(status, random_list[0], random_list[1], random_list[2])
                        write_msg(user_id, f'Пользователь добавлен в чс')
                        # bot.dislike_list(random_list)
                    write_msg(user_id, f'Продолжить поиск?')
                else:
                    break

            elif request == 'показать избранных':
                show_list_favorites(vkinder._get_user_params(user_id)[0])
                # bot.write_msg(user_id, f'')
                write_msg(user_id, f'Продолжить поиск?')
            elif request in ['пока', 'нет']:
                write_msg(event.user_id, "Пока((")
                break
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
