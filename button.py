from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def create_keyboard_first():
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_button('Начать поиск', VkKeyboardColor.PRIMARY, payload=['start_search'])
    keyboard.add_button('Продолжить поиск', VkKeyboardColor.PRIMARY, payload=['next_search'])
    keyboard.add_button('Показать избранных', VkKeyboardColor.PRIMARY, payload=['show_favorite'])
    return keyboard #.get_keyboard()

def create_keyboard_second():
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_button('Да', VkKeyboardColor.POSITIVE, payload=['да'])
    keyboard.add_button('Нет', VkKeyboardColor.NEGATIVE, payload=['нет'])
    return keyboard  # .get_keyboard()

#print(create_keyboard())