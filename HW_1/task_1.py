# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
# пользователя, сохранить JSON-вывод в файле *.json.
import requests
import json
# from pprint import pprint

main_link = 'https://api.github.com'
git_user = 'arfarrim'
file = 'task_1.json'

response = requests.get(f'{main_link}/users/{git_user}/repos')

for i in response.json():
    print(i['name'])

with open(file, 'w') as f:
    json.dump(response.json(), f)
