import json
import requests
import pandas as pd
from nltk.probability import FreqDist


# Получение номера отрасли или специализации (в зависимости от того в какой области вы хотите искать),
# в которой будет происходить поиск для получения вакансий
def get_all_fields():
    response = requests.get("https://api.hh.ru/specializations")
    with open("specializations.txt", "wb") as outfile:
        outfile.write(response.content)

    response = requests.get("https://api.hh.ru/industries")
    with open("industries.txt", "wb") as outfile:
        outfile.write(response.content)


# Получение названий вакансий, границ заработной платы и ключевых навыков с сайта hh
def get_vacancies():
    # Область '4' - Новосибирская область
    # Отрасль '7' - 'Информационные технологии, системная интеграция, интернет'
    # Запрос - "python"
    req = \
        requests.get(
            'https://api.hh.ru/vacancies?text=python&industry=7&area=4&per_page=100&only_with_salary=true').json()[
            'items']
    '''# Специализация '21' - 'Транспорт, логистика' по запросу «курьер»
    req = \
        requests.get(
            'https://api.hh.ru/vacancies?text=курьер&specialization=21&area=4&per_page=100&only_with_salary=true').json()[
            'items']
    # Специализация '9' - 'Высший менеджмент'
    req = \
        requests.get(
            'https://api.hh.ru/vacancies?specialization=9&area=4&per_page=100&only_with_salary=true').json()[
            'items']'''
    name = []
    salary_from = []
    salary_to = []
    key_skills = []
    for element in req:
        req = requests.get(element['url']).json()
        for key_skill in req['key_skills']:
            key_skills.append(key_skill['name'])
            name.append(element['name'])
            salary_from.append(element['salary']['from'])
            salary_to.append(element['salary']['to'])
    df = pd.DataFrame({'name': name, 'salary_from': salary_from, 'salary_to': salary_to, 'key_skills': key_skills})
    df.to_excel('./vacancies_python.xlsx')
    return req


# Построение графика с ключевыми навыками
def analysis():
    excel_data = pd.read_excel('vacancies_python.xlsx')
    key_skills_list = excel_data['key_skills'].tolist()
    fdist = FreqDist(key_skills_list)
    fdist.plot(30, cumulative=False)


if __name__ == '__main__':
    get_all_fields()
    get_vacancies()
    analysis()
