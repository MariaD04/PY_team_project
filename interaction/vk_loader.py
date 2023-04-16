import re
import datetime
import vk_api
from vk_api import VkTools
from table.vkinder_base import load_user, load_clientuser, load_user_links
from table.vkinder_base import check_clientuser_exist, check_user_existing


class VKLoader:
    """ Класс предназначен для загрузки и обработки данных
     из VK используемых ботом """

    def __init__(self, token):
        self.token = token
        self.vk_session = vk_api.VkApi(token=self.token)
        self.api = self.vk_session.get_api()

    def get_age(self, bdate):
        """ Принимает дату рождения в любом формате,
        возвращает возраст пользователя"""
        current_year = datetime.datetime.now().year
        result = re.search(r'[\d]{4}', bdate)
        if result:
            age = current_year - int(result[0])
            return age
        else:
            return None

    def load_base(self, status, dict_user, dict_client, list_links):
        dict_user['status'] = status
        if check_clientuser_exist(
                dict_client['id_client'],
                dict_user['id_user']) == 1:
            check_user_existing(dict_user, list_links)
        elif check_clientuser_exist(
                dict_client['id_client'],
                dict_user['id_user']) == 0:
            if check_user_existing(dict_user, list_links):
                load_user(dict_user)
                load_user_links(dict_user['id_user'], list_links)
            load_clientuser(dict_client['id_client'], dict_user['id_user'])

    def get_vk_list(self, search_info):
        """ Принимает параметры для поиска пользователей VK """
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

    def get_user_params(self, user_id):
        """ Возвращает словарь с параметрами для поиска """

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
            dict_client['age'] = self.get_age(user_dict['bdate'])
        else:
            dict_client['age'] = None

        search_info['city'] = dict_client['city']
        search_info['sex'] = dict_client['gender']
        search_info['age'] = dict_client['age']
        return dict_client, search_info

    def get_foto(self, user_id):
        """ Возвращает список фото и их параметров из альбома "profile" """
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
                foto_list.append({
                    'likes': item['likes']['count'],
                    'url': item['sizes'][-1]['url']
                })
            sort_foto = sorted(
                foto_list,
                key=lambda x: x['likes'],
                reverse=True
            )
            foto_list.clear()
            for item in sort_foto[:3]:
                foto_list.append(item['url'])
            return foto_list
