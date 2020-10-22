# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше
# введённой суммы. Запрос должен анализировать одновременно минимальную и максимальную зарплату
#
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy']
collection = db['vacancy_list_hh']
limit = int(input('введите желаемую зарплату'))


def mongodb_vacancy_salary_search_more_then(db_collection, limit):
    return db_collection.find({'$or': [{'salary_min': {'$gte': limit}}, {'salary_max': {'$gte': limit}}]})


list_search = mongodb_vacancy_salary_search_more_then(collection, limit)
print(1)
for item in list_search:
    pprint(item)
client.close()
