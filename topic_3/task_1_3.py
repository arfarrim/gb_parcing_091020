# task 1 + 3
# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД.
#
# Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
# №3 реализовано в основном теле, скрапер не выделен в функцию

from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bs

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy']
collection = db['vacancy_list_hh']


def mongodb_update(db_collection, condition, data):
    db_collection.update_one(condition, {'$set': data}, upsert=True)


def mongodb_vacancy_salary_search_more_then(db_collection, limit):
    return db_collection.find({'$or': [{'salary_min': {'$gte': limit}}, {'salary_max': {'$gte': limit}}]})


main_link = 'https://hh.ru/search/vacancy'
vacancy = input('введите должность')
page = 0
params = {
    'clusters': 'true',
    'enable_snippets': 'true',
    'st': 'searchVacancy',
    'text': vacancy,
    'page': page
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

response = requests.get(main_link, params=params, headers=headers)
soup = bs(response.text, 'html.parser')
end_page = soup.find('div', {'data-qa': 'pager-block'})
end_page = end_page.find('script')
end_page = end_page.get('data-params').replace(' ', '')
end_page = int(end_page[(end_page.find('pagesCount":'))+12:].split("\n")[0])

for n_page in (0, end_page-1):
    params['page'] = n_page
    response = requests.get(main_link, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    job_list = soup.findAll('div', {'data-qa': 'vacancy-serp__vacancy'})
    for item in job_list:
        job_name = item.find('a')
        job_name = job_name.getText()
        job_link = item.find('a')['href']
        job_link = job_link.split('?')[0]
        job_salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not job_salary:
            job_salary_min = None
            job_salary_max = None
            job_salary_cur = None
        else:
            job_salary = job_salary.getText()
            job_salary = job_salary.replace(u'\xa0', '')
            if job_salary[0] == 'о':
                job_salary_max = None
                job_salary_min = int(job_salary.split(' ')[1])
                job_salary_cur = job_salary.split(' ')[2]
            elif job_salary[0] == 'д':
                job_salary_min = None
                job_salary_max = int(job_salary.split(' ')[1])
                job_salary_cur = job_salary.split(' ')[2]
            else:
                job_salary_min = int(job_salary.split('-')[0])
                job_salary = job_salary.split(' ')
                job_salary_cur = job_salary[1]
                job_salary_max = int(job_salary[0].split('-')[1])

        jobs_dict = {'link': job_link,
                     'name': job_name,
                     'salary_min': job_salary_min,
                     'salary_max': job_salary_max,
                     'salary_cur': job_salary_cur,
                     'site': 'https://hh.ru'
                     }
        mongodb_update(collection, {'link': jobs_dict.get('link')}, jobs_dict)
client.close()
