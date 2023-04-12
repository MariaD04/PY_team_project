from random import randrange
from vk_loader import VKLoader
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = 'vk1.a.OFu2N4m4LKDWON6V6dtbwel4GiZJpCBLOPmAZFl8gIsQQxjGG0nveg6juu2sDwuzsOi5si-NrM12-6iErDJQbEkwhKJN_fHTkaGr4o3frOZgxbmmD0BBNhIhE5SOPZLBUZwGBk_TKIlG3vuOqABOo8BnmuMAF7TTAvZ43Iozxjwucg41TbMSlnFqIFonEnfU_w5_96KcdcSSHnrS27cgiQ'

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "привет":
                    write_msg(event.user_id, f"Хай, {event.user_id}")
                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")
