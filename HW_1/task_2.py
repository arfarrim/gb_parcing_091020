# Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
# требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать
# в файл.

import requests
import json

main_link = 'https://api.vk.com/method/gifts.get?&count=1&offset=1&access_token='
token = '92422f0ab6a33587e9eaabee79d85ff060d3ab00d16cdfc16dc05fc8521915b4ab6637b3d896380718859'
vk_api_version = '&v=5.124'
file = 'task_2.json'

response = requests.get(f'{main_link}{token}{vk_api_version}')

with open(file, 'w') as f:
    json.dump(response.json(), f)
