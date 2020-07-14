import json
from bs4 import BeautifulSoup

with open('product_info_LA2.json', 'r', encoding="utf-8") as file:
    product_list = json.loads(file.read())

# 清洗資料
for product in product_list:
    # 用BS處理HTML編碼，修改產品名稱內的亂碼，並去除換行符號
    product['name'] = BeautifulSoup(product['name'], 'lxml').text
    product['name'] = product['name'].replace("&amp;", "&").replace('\n', '')
    if '\n' in product['name']:
        print(product['name'])

    # 價格修改，先去除$符號和千分位逗號方便清洗
    product['price'] = product['price'].replace('$', '').replace(',', '')
    try:
        product['price'] = float(product['price'])
    except ValueError:
        if '-' in product['price']:
            # 取出區間的最大與最小值，算平均價格
            min = float(product['price'].partition('-')[0])
            max = float(product['price'].partition('-')[2])
            product['price'] = (min + max)/2
        else:
            print(product['price'])

    # 把評分改為tuple
    product['star_ratings'] = tuple(product['star_ratings'])

    # 重新寫成新的文字檔
    with open('product_info_LA2_cleansed', 'a', encoding='utf-8') as file_1:
        json.dump(product, file_1, indent=4, ensure_ascii=False)
        file_1.write(',')
