import json
from bs4 import BeautifulSoup

with open('product_info_LA2.json', 'r', encoding="utf-8") as file:
    product_list = json.loads(file.read())

# 修改產品名稱內的亂碼，並去除換行符號
for product in product_list:
    product['name'] = BeautifulSoup(product['name'], 'lxml').text
    product['name'] = product['name'].replace("&amp;", "&").replace('\n', '')
    if '\n' in product['name']:
        print(product['name'])

    # 重新寫成新的文字檔
    with open('product_info_LA2_cleansed', 'a', encoding='utf-8') as file_1:
        json.dump(product, file_1, indent=4, ensure_ascii=False)
        file_1.write(',')
