# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
# Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия. ### По желанию можно добавить ещё параметры вакансии
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json

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
    jobs = []
    for item in job_list:
        job_data = {}
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
                job_salary_min = job_salary.split(' ')[1]
                job_salary_cur = job_salary.split(' ')[2]
            elif job_salary[0] == 'д':
                job_salary_min = None
                job_salary_max = job_salary.split(' ')[1]
                job_salary_cur = job_salary.split(' ')[2]
            else:
                job_salary_min = job_salary.split('-')[0]
                job_salary = job_salary.split(' ')
                job_salary_cur = job_salary[1]
                job_salary_max = job_salary[0].split('-')[1]
        job_data['name'] = job_name
        job_data['link'] = job_link
        job_data['salary_min'] = job_salary_min
        job_data['salary_max'] = job_salary_max
        job_data['salary_cur'] = job_salary_cur
        job_data['site'] = 'https://hh.ru'
        jobs.append(job_data)

pprint(jobs)
with open('hh_parc.json', 'w') as f:
    json.dump(jobs, f)
