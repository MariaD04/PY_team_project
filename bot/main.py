from vk_loader import VKLoader
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from button import send_

token = input('Token: ')
user_token = input()
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

if __name__ == '__main__':
    chosen_users = []
    bot = VKLoader()
    for event in bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower()
                user_id = str(event.user_id)
                msg = event.text.lower()
                send_(user_id, msg.lower())
                if request == "привет":
                    bot.write_msg(user_id, f"Привет, {event.user_id}")

                elif request in ['начать поиск', 'продолжить поиск', 'да']:
                    random_list = []
                    #random_user_data = bot.random_user(bot._get_user_params(user_id), user_id)
                    #random_list.append(random_user_data)

                    if random_list[0]['id'] not in chosen_users:
                        bot.write_msg(user_id, {random_list[0]['first_name']+' '+random_list[0]['last_name']},
                                      {','.join(bot.final_fotos_list(bot.sort_foto(bot.get_foto(random_list[0]['id']))))})
                        bot.write_msg(user_id, f"Ссылка на профиль {random_list[0]['vk_link']}")
                        bot.write_msg(user_id, f'Занести пользователя в список избранных?')
                       
                        for this_event in bot.longpoll.listen():
                            if this_event.type == VkEventType.MESSAGE_NEW:
                                if this_event.to_me:
                                    message = this_event.text

                        if message == 'да':
                            bot.write_msg(user_id, f'Пользователь занесён в список избранных')
                            #bot.like_list(random_list)
                            chosen_users.append(random_list[0]['id'])
                        elif message == 'нет':
                            bot.write_msg(user_id, f'Пользователь добавлен в чс')
                            #bot.dislike_list(random_list)
                        bot.write_msg(user_id, f'Продолжить поиск?')
                    else:
                        break

                elif request == 'показать избранных':
                    #bot.write_msg(user_id, f'')
                    bot.write_msg(user_id, f'Продолжить поиск?')
                elif request in ['пока', 'нет']:
                    bot.write_msg(event.user_id, "Пока((")
                    break
                else:
                    bot.write_msg(event.user_id, "Не поняла вашего ответа...")