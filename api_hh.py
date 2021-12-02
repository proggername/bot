import requests
import json
import datetime

from bs4 import BeautifulSoup


def get_str_from_json_1(name: str, json_obj: json):
    try:
        result_str = json_obj[name]
        if result_str == 'None' or result_str is None:
            result_str = ' '
    except Exception:
        result_str = ' '

    return result_str


def get_str_from_json_2(name_1: str, name_2: str, json_obj: json) -> str:
    try:
        result_str = json_obj[name_1][name_2]
        if result_str == 'None' or result_str is None:
            result_str = ' '
    except Exception:
        result_str = ' '

    return result_str


def get_str_from_json_3(name_1: str, name_2: str, name_3: str, json_obj: json):
    try:
        result_str = json_obj[name_1][name_2][name_3]
        if result_str == 'None' or result_str is None:
            result_str = ' '
    except Exception:
        result_str = ' '

    return result_str


def get_vacancy(vacancy_id: int):
    url_vac = f'https://api.hh.ru/vacancies/{vacancy_id}'
    results = requests.get(url=url_vac)
    data = results.content.decode()
    vacancy = json.loads(data)
    oktl = get_str_from_json_1('alternate_url', vacancy)
    desc = get_str_from_json_1('description', vacancy)
    desc = str(desc).replace('<li><p>', '\n').replace('<li>', '\n').replace('</li>', '').replace('<p>', '\n').replace(
        '</p>', '').replace('<strong>', '<b>') \
        .replace('</strong>', '</b>').replace('<ul>', '').replace('</ul>', '\n').replace('<br />', '').replace('<br>',
                                                                                                               '\n')
    description = desc  # BeautifulSoup(vacancy['description'], 'lxml').text
    key_skills = get_str_from_json_2('key_skills', 'name', vacancy)
    schedule = get_str_from_json_2('schedule', 'name', vacancy)
    experience = get_str_from_json_2('experience', 'name', vacancy)

    address_city = get_str_from_json_2('address', 'city', vacancy)
    address_street = get_str_from_json_2('address', 'street', vacancy)
    address_building = get_str_from_json_2('address', 'building', vacancy)

    employment = get_str_from_json_2('employment', 'name', vacancy)
    salary_to = get_str_from_json_2('salary', 'to', vacancy)
    salary_from = get_str_from_json_2('salary', 'from', vacancy)
    name = get_str_from_json_1('name', vacancy)
    employer_photo_url = get_str_from_json_3('employer', 'logo_urls', 'original', vacancy)
    employer_name = get_str_from_json_2('employer', 'name', vacancy)
    contacts_name = get_str_from_json_2('contacts', 'name', vacancy)
    contacts_email = get_str_from_json_2('contacts', 'email', vacancy)
    contacts_code = get_str_from_json_3('contacts', 'phones', 'city', vacancy)
    contacts_number = get_str_from_json_3('contacts', 'phones', 'number', vacancy)
    working_days = get_str_from_json_2('working_days', 'name', vacancy)
    result_text = f'<b>Компания:</b> {employer_name}'
    if name != ' ':
        result_text = result_text + f'\n<b>Должность</b>: #{name}'
    if key_skills != ' ':
        result_text = result_text + f'\nkey_skils: {key_skills}'
    if schedule != ' ':
        result_text = result_text + f'\n<b>Занятость:</b> {schedule} {employment} '
    if working_days != ' ':
        result_text = result_text + f'\nworking_days: {working_days}'
    if experience != ' ':
        result_text = result_text + f'\nТребуемый опыт работы: {experience}'
    if salary_from != ' ':
        result_text = result_text + f'\n<b>Зарплата:</b> от {salary_from}'
    if salary_to != ' ':
        result_text = result_text + f' до {salary_to}'
    result_text = result_text + f'\n\n{description}'
    if contacts_name != ' ' or contacts_email != ' ' or contacts_number != ' ':
        result_text = result_text + f'\n\n<b>Контакт:</b> {contacts_email}, {contacts_name}, {contacts_code}, {contacts_number}'

    if address_city != ' ':
        result_text = result_text + f'\n<b>Адрес:</b> {address_city}, {address_street}, {address_building}'
    if oktl != ' ':
        result_text = result_text + f'\n<a href=\'{oktl}\'>Prosmotr</a>'
    photo_url = employer_photo_url

    return result_text


# Дата и время на компьютере



def get_id(vacant_name='Java'):
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    date_and_time_now = yesterday.strftime('%Y-%m-%d')
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': vacant_name,
        'area': 97,
        'per_page': 100,
        'specializations': {"specializations": [
                                                {"id": "1.400", "name": "Оптимизация сайта (SEO)", "laboring": False},
                                                {"id": "1.420", "name": "Администратор баз данных", "laboring": False},
                                                {"id": "1.474", "name": "Стартапы", "laboring": False},
                                                {"id": "1.475", "name": "Игровое ПО", "laboring": False},
                                                {"id": "1.536", "name": "CRM системы", "laboring": False},
                                                {"id": "1.9", "name": "Web инженер", "laboring": False},
                                                {"id": "1.25", "name": "Аналитик", "laboring": False},
                                                {"id": "1.110", "name": "Компьютерная безопасность", "laboring": False},
                                                {"id": "1.117", "name": "Тестирование", "laboring": False},
                                                {"id": "1.161", "name": "Мультимедиа", "laboring": False},
                                                {"id": "1.221", "name": "Программирование, Разработка", "laboring": False},
                                                {"id": "1.270", "name": "Сетевые технологии", "laboring": False},
                                                {"id": "1.273", "name": "Системный администратор", "laboring": False}]},
        'date_from': date_and_time_now,
        'host': 'hh.uz',

    }
    results = requests.get(url=url, params=params)

    objJson = json.loads(results.content.decode())
    
    array_of_id = []
    if len(objJson['items']) > 0:
        for item in objJson['items']:
            vacancy_id = item['id']
            array_of_id.append(vacancy_id)
    else:
        array_of_id = [0]
    return array_of_id
