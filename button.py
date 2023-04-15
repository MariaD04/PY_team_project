from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def create_keyboard_first():
    keyboard = VkKeyboard(one_time=False, inline=False)
    keyboard.add_button('Искать', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Пока', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Показать избранных', VkKeyboardColor.PRIMARY)
    return keyboard

def create_keyboard_second():
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_button('В избранное', VkKeyboardColor.POSITIVE)
    keyboard.add_button('В черный список', VkKeyboardColor.NEGATIVE)
    return keyboard