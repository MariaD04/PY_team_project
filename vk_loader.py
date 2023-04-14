import re
import datetime
import vk_api
from vk_api import VkTools
import random
from vkinder_base import show_list_favorites, load_client, load_user, load_clientuser, load_user_links
from vkinder_base import check_client_existing, check_clientuser_exist, check_user_existing

class VKLoader:
    """Класс предназначен для загрузки и обработки данных из VK используемых ботом."""

    def __init__(self, token):
        self.token = token
        self.vk_session = vk_api.VkApi(token=self.token)
        self.api = self.vk_session.get_api()

    def _get_age(self, bdate):
        """Принимает дату рождения в любом формате, возвращает возраст пользователя."""

        current_year = datetime.datetime.now().year
        result = re.search(r'[\d]{4}', bdate)
        if result:
            age = current_year - int(result[0])
            return age
        else:
            return None

    def _load_base(self, status, dict_user, dict_client, list_links):
        dict_user['status'] = status  # в словарь дописывается поле статус (1- избранное, 2 - черный список)
        if check_clientuser_exist(dict_client['id_client'], dict_user['id_user']) == 1:
            # если партнер для данного клиента есть в БД, обновит при необходимости информацию
            check_user_existing(dict_user, list_links)
        elif check_clientuser_exist(dict_client['id_client'], dict_user['id_user']) == 0:
            # если партнера для данного клиента нет в промежуточной таблице связи клиента и партнера
            if check_user_existing(dict_user, list_links):
                # если партнер есть в базе для других клиентов, обновит при необходимости данные или загрузит
                # нового партнера для данного клиента
                load_user(dict_user)
                load_user_links(dict_user['id_user'], list_links)
            # запишет данные в промежуточную таблицу, связь клиента и партнера
            load_clientuser(dict_client['id_client'], dict_user['id_user'])

    def dict_user_list(self, user_id):
        dict_client = self._get_user_params(user_id)[0]
        for item in self.get_vk_list(self._get_user_params(user_id)[1]):
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
                dict_user['age'] = self._get_age(item['bdate'])
            else:
                dict_user['age'] = None

            list_links = self.get_foto(dict_user['id_user'])
            if check_clientuser_exist(dict_client['id_client'], dict_user['id_user']) == 2:
                #print('Не показывать, ищем следующего')
                continue
            return [dict_user, dict_client, list_links]

    def get_vk_list(self, search_info):
        """Принимает параметры для поиска пользователей VK, """

        if search_info['sex'] == 1:
            search_sex = 2
        elif search_info['sex'] == 2:
            search_sex = 1
        else:
            search_sex = None
        vk_list = VkTools(self.api).get_all_iter(
            method='users.search',
            max_count=1000,
            values={
                'hometown': search_info['city'],
                'age_from': search_info['age'],
                'age_to': search_info['age'],
                'sex': search_sex,
                'fields': 'city, domain, sex, bdate'
            }
        )
        return vk_list

    def _get_user_params(self, user_id):
        """Принимает id пользователя, возвращает словарь с параметрами для поиска пары(город, противоположный пол, возраст)"""

        vk_user_info = self.api.users.get(
            user_ids=user_id,
            fields='city, sex, bdate, domain'
        )
        for item in vk_user_info:
            user_dict = dict(item)
        search_info = {}
        dict_client = {
            'id_client': user_dict['id'],
            'first_name': user_dict['first_name'],
            'last_name': user_dict['last_name'],
            'link_profile': 'https://vk.com/' + user_dict['domain']
        }

        if 'city' in user_dict:
            dict_client['city'] = user_dict['city']['title']
        else:
           dict_client['city'] = None
        if 'sex' in user_dict:
            dict_client['gender'] = user_dict['sex']
        else:
            dict_client['gender'] = None
        if 'bdate' in user_dict:
            dict_client['age'] = self._get_age(user_dict['bdate'])
        else:
            dict_client['age'] = None

        search_info['city'] = dict_client['city']
        search_info['sex'] = dict_client['gender']
        search_info['age'] = dict_client['age']

        return dict_client, search_info

    def get_foto(self, user_id):
        """Принимает ID пользователя, возвращает список фото и их параметров из альбома "profile"."""
        try:
            vk_user_foto = self.api.photos.get(
                owner_id=user_id,
                album_id='profile',
                count=50,
                extended=1,
                photo_sizes=1
            )
        except Exception:
            return []
        else:
            foto_list = []
            for item in vk_user_foto['items']:
                foto_list.append({'likes': item['likes']['count'], 'url': item['sizes'][-1]['url']})
            sort_foto = sorted(foto_list, key=lambda x: x['likes'], reverse=True)
            foto_list.clear()
            for item in sort_foto[:3]:
                foto_list.append(item['url'])
            return foto_list


