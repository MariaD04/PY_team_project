import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from table.models import Gender, Status, Users, Clients, LinksFoto, ClientsUsers
from table.models import create_tables


def load_client(dict_client):
    ''' добавление нового клиента '''
    client = Clients(
        id_client=dict_client['id_client'],
        first_name=dict_client['first_name'],
        last_name=dict_client['last_name'],
        link_profile=dict_client['link_profile'],
        city=dict_client['city'],
        age=dict_client['age'],
        id_gender=dict_client['gender']
    )
    session.add(client)
    session.commit()


def load_user(dict_user):
    ''' добавление найденного друга '''
    user = Users(
        id_user=dict_user['id_user'],
        first_name=dict_user['first_name'],
        last_name=dict_user['last_name'],
        link_profile=dict_user['link_profile'],
        city=dict_user['city'],
        age=dict_user['age'],
        id_gender=dict_user['gender'],
        id_status=dict_user['status']
    )
    session.add(user)
    session.commit()


def load_clientuser(id_client, id_user):
    ''' добавление связи в таблицу отношений '''
    client_user = ClientsUsers(
        id_client=id_client,
        id_user=id_user
    )
    session.add(client_user)
    session.commit()


def load_user_links(id_user, list_links):
    ''' добавление ссылок на фотографии из профиля '''
    if list_links == []:
        links = LinksFoto(
            link=None,
            id_user=id_user
        )
        session.add(links)
    else:
        for tuple in list_links:
            links = LinksFoto(
                link=tuple,
                id_user=id_user
            )
            session.add(links)
    session.commit()


def check_client_existing(dict_client):
    ''' проверка на существование клиента в БД и обновление данных '''
    existing = session.query(Clients).filter(
        Clients.id_client == dict_client['id_client']
    ).all()
    if existing == []:
        return True
    for attribute in existing:
        if dict_client['first_name'] != attribute.first_name:
            attribute.first_name = dict_client['first_name']
        if dict_client['last_name'] != attribute.last_name:
            attribute.last_name = dict_client['last_name']
        if dict_client['link_profile'] != attribute.link_profile:
            attribute.link_profile = dict_client['link_profile']
        if dict_client['city'] != attribute.city:
            attribute.city = dict_client['city']
        if dict_client['age'] != attribute.age:
            attribute.age = dict_client['age']
        if dict_client['gender'] != attribute.id_gender:
            attribute.id_gender = dict_client['gender']
        session.add(attribute)
        session.commit()
    return False


def check_user_existing(dict_user, list_links):
    ''' проверка на существование друга в БД и обновление данных '''
    update_user = session.query(Users).filter(
        Users.id_user == dict_user['id_user']
    ).all()
    if update_user == []:
        return True
    session.query(LinksFoto).filter(
        LinksFoto.id_user == dict_user['id_user']
    ).delete(synchronize_session='fetch')
    session.commit()
    load_user_links(dict_user['id_user'], list_links)
    for attribute in update_user:
        if dict_user['first_name'] != attribute.first_name:
            attribute.first_name = dict_user['first_name']
        if dict_user['last_name'] != attribute.last_name:
            attribute.last_name = dict_user['last_name']
        if dict_user['link_profile'] != attribute.link_profile:
            attribute.link_profile = dict_user['link_profile']
        if dict_user['city'] != attribute.city:
            attribute.city = dict_user['city']
        if dict_user['age'] != attribute.age:
            attribute.age = dict_user['age']
        if dict_user['gender'] != attribute.id_gender:
            attribute.id_gender = dict_user['gender']
        if dict_user['status'] != attribute.id_status:
            attribute.id_status = dict_user['status']
        session.add(attribute)
        session.commit()


def show_list_favorites(dict_client):
    ''' показ списка избранных для данного клиента '''
    list_favorites = (session.query(
        Users.id_user,
        Users.first_name,
        Users.last_name,
        Users.link_profile,
        Users.city,
        Users.age,
        Gender.title
    ).join(Gender).join(Status).join(ClientsUsers).filter(
        Users.id_status == 1,
        ClientsUsers.id_client == dict_client['id_client']
    ).all())
    return list_favorites


def show_links_user(user_id):
    ''' показ списка ссылок избранных '''
    favorite_links = []
    favorite_link_user = session.query(
        LinksFoto.link
    ).filter(LinksFoto.id_user == user_id).all()
    for item in favorite_link_user:
        favorite_links.append(item[0])
    return favorite_links


def __check_blacklist(id_user):
    ''' проверка на присутствие в черном списке '''
    blacklist = session.query(Users).filter(
        Users.id_user == id_user, Users.id_status == 2
    ).all()
    if blacklist == []:
        return False
    return True


def check_clientuser_exist(id_client, id_user, in_base=0):
    ''' проверка на существование данных таблице отношений '''
    existing = session.query(ClientsUsers).filter(
        ClientsUsers.id_client == id_client,
        ClientsUsers.id_user == id_user
    ).all()
    if existing != []:
        in_base = 1
        if __check_blacklist(id_user):
            in_base = 2
    return in_base


def __check_base_table_exists():
    ''' проверка наличия данных в таблицах Gender и Status '''
    is_exists_gender = session.query(Gender).count()
    is_exists_status = session.query(Status).count()
    return is_exists_gender, is_exists_status


def __load_base_table():
    ''' запись данных в таблицы Gender и Status '''
    gender1 = Gender(id_gender=1, title='женский')
    gender2 = Gender(id_gender=2, title='мужской')
    status1 = Status(id_status=1, title='Избранное')
    status2 = Status(id_status=2, title='Черный список')
    session.add_all([gender1, gender2, status1, status2])
    session.commit()


''' считывание пароля от postgres из файла по указанному пути '''
with open(r'D:\Python\pas.txt', encoding='utf-8') as file:
    pas = file.readline().rstrip('\n')

DSN = f'postgresql://postgres:{pas}@localhost:5432/vk_bot_base'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

if __check_base_table_exists() != (2, 2):
    __load_base_table()

session.close()
