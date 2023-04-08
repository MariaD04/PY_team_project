import re
import datetime
import vk_api
from vk_api import VkTools


def _get_age(bdate):
    """Принимает дату рождения в любом формате, возвращает возраст пользователя."""

    current_year = datetime.datetime.now().year
    result = re.search(r'(\d*.\d*.)?(\d\d\d\d)', bdate)
    if result:
        age = current_year - result.group(2)
        return age
    else:
        return None


class VKLoader:
    """Класс предназначен для загрузки и обработки данных из VK используемых ботом."""

    def __init__(self, token):
        self.token = token
        self.vk_session = vk_api.VkApi(token=TOKEN)
        self.api = self.vk_session.get_api()

    def get_vk_list(self, city=None, sex=None, age=20):
        """Принимает параметры для поиска пользователей VK, """

        if sex == 1:
            search_sex = 2
        elif sex == 2:
            search_sex = 1
        else:
            search_sex = None
        vk_list = VkTools(self.api).get_all_iter(
            method='users.search',
            max_count=1000,
            values={
                'city_id': city,
                'age_from': age,
                'age_to': age,
                'sex': search_sex
            }
        )
        return vk_list

    def _get_user_params(self, user_id):
        """Принимает id пользователя, возвращает словарь с параметрами для поиска пары(город, противоположный пол, возраст)"""

        vk_user_info = self.api.users.get(
            user_ids=user_id,
            fields='city, sex, bdate'
        )
        for item in vk_user_info:
            user_dict = dict(item)
        user_info = {}
        if 'city' in user_dict:
            user_info['city'] = user_dict['city']['id']
        else:
            user_info['city'] = None
        if 'sex' in user_dict:
            user_info['sex'] = user_dict['sex']
        else:
            user_info['sex'] = None
        if 'bdate' in user_dict:
            user_info['age'] = _get_age(user_dict['bdate'])
        else:
            user_info['age'] = None
        return user_info

    def get_foto(self, user_id):
        """Принимает ID пользователя, возвращает список фото и их параметров из альбома "profile"."""
        try:
            vk_user_foto = self.api.photos.get(
                owner_id=user_id,
                album_id='profile',
                count=3,
                extended=1,
                photo_sizes=1
            )
        except Exception:
            return 'Пользователь закрыл фото настройками приватности.'
        else:
            return vk_user_foto
