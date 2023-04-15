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
                    dict_client = vkinder._get_user_params(user_id)[0]
                    random_list = vkinder.dict_user_list(user_id)  # перебор потенциальной пары и добавление в БД

                    write_msg(user_id, message={random_list[0]['first_name'] + ' ' + random_list[0]['last_name']},
                              foto={','.join(vkinder.get_foto(random_list[0]['id_user']))})
                    write_msg(user_id, message={random_list[0]['city'] + ', ' + str(random_list[0]['age']) + ' лет'})
                    write_msg(user_id, message=f"Ссылка на профиль {random_list[0]['link_profile']}")
                    write_msg(user_id, message=f'Куда добавить человека?', keyboard=create_keyboard_second())
                    for this_event in longpoll.listen():
                        if this_event.type == VkEventType.MESSAGE_NEW:
                            if this_event.to_me:
                                request = this_event.text.lower()
                                #print(request)
                                if request == 'в избранное':
                                    status = 1
                                    vkinder._load_base(status, random_list[0], random_list[1], random_list[2])
                                    write_msg(user_id, message=f'Пользователь занесён в список избранных')
                                    break
                                elif request == 'в черный список':
                                    status = 2
                                    vkinder._load_base(status, random_list[0], random_list[1], random_list[2])
                                    write_msg(user_id, message=f'Пользователь занесён в черный список')
                                    break

                elif request == 'показать избранных':
                    for item in show_list_favorites(vkinder._get_user_params(user_id)[0]):
                        if show_links_user(item[0]) == [None]:
                            write_msg(user_id, message={item[1] + ' ' + item[2]})
                            write_msg(user_id, message={'Ссылка на профиль: ' + item[3]})
                            write_msg(user_id, message={str(item[4]) + ', ' + str(item[5]) + ' лет'})
                        else:
                            write_msg(user_id, message={item[1] + ' ' + item[2]}, foto={','.join(show_links_user(item[0]))})
                            write_msg(user_id, message={'Ссылка на профиль: ' + item[3]})
                            write_msg(user_id, message={str(item[4]) + ', ' + str(item[5]) + ' лет'})
                    write_msg(user_id, message='продолжим?')

                elif request in ['пока']:
                    write_msg(event.user_id, message="Пока((")
                else:
                    write_msg(event.user_id, message="Не поняла вашего ответа...")
