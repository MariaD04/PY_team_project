from main import vkinder

def get_button(text, color):
    return {
            "action":{
               "type":"text",
               "payload":"{\"button\": \"1\"}",
               "label": f"{text}"
            },
            "color": f"{color}"
            }

keyboard = {
    "one_time": False,
    "buttons": [
    [get_button('начать поиск', 'primary')],
    [get_button('продолжить поиск', 'primary')],
    [get_button('показать избранных', 'primary')],
    [get_button('да', 'positive')],
    [get_button('нет', 'negative')]
    ]
}

def send_(user_id, text):
    vkinder.vk.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': 0, 'keyboard': keyboard })

keyboard = str(keyboard.decode('utf-8'))