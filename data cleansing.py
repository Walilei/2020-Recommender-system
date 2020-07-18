import json
from bs4 import BeautifulSoup
import csv

with open('product_info_LA2.json', 'r', encoding="utf-8") as json_file:
    product_list = json.loads(json_file.read())

with open('product_info_LA2_cleansed.csv', 'w', encoding='utf-8', newline='') as csv_file:
    # 定義csv檔欄位
    fieldnames = ['keyword', 'name', 'brand', 'url', 'pic', 'price', 'category', 'star_ratings',
                  'at_a_glance', 'highlights', 'specifications', 'description', 'reviews']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()

# 清洗資料
count = 0  # 查看完成筆數用
for product in product_list:
    # 關鍵字要去掉trade mark符號否則寫入csv檔會出錯
    product['keyword'] = product['keyword'].replace('™', '')

    # 用BS處理HTML編碼，修改產品名稱內的亂碼，並去除換行符號以及trade mark符號
    product['name'] = BeautifulSoup(product['name'], 'lxml').text.replace('™', '')
    product['name'] = product['name'].replace("&amp;", "&").replace('\n', '').strip(f"- {product['brand']}").strip(' ')

    # 價格修改，先去除$符號和千分位逗號方便清洗
    product['price'] = product['price'].replace('$', '').replace(',', '')
    try:
        product['price'] = round(float(product['price']), 2)
    except ValueError:
        if '-' in product['price']:
            # 取出區間的最大與最小值，算平均價格
            low_p = float(product['price'].partition('-')[0])
            high_p = float(product['price'].partition('-')[2])
            product['price'] = round((low_p + high_p)/2, 2)
        else:
            continue

    # 把評分改為tuple
    product['star_ratings'] = tuple(product['star_ratings'])

    # description一樣要去掉trade mark跟換行
    redundant1 = 'PACKAGING MAY VARY BY LOCATION'
    product['description'] = product['description'].replace('™', '').replace('\n', '').replace('*', '')
    product['description'] = product['description'].replace('|', '').replace('\\', '').replace('½', 'half')
    product['description'] = product['description'].replace(redundant1, '').strip('-')

    # 刪除highlights內不必要的符號或句子
    if type(product['highlights']) == list:
        for i in range(len(product['highlights'])):
            useless01 = '(see nutrition information for Saturated Fat, and Sodium content)'
            useless02 = '(See nutrition for fat and saturated fat content.)'
            useless03 = '(Not a low calorie food. See nutrition information for calorie and sugar content.)'

            line = BeautifulSoup(product['highlights'][i], 'lxml').text
            line = line.replace('*', '').replace('●', '').replace('∙', '').replace('\n', '').replace('|', '')
            line = line.replace(useless01, '').replace(useless02, '').replace(useless03, '')
            product['highlights'][i] = line

    # 淨重項目改存為tuple，第一個元素為浮點數，第二個元素為小寫單位；去除每行開頭的空白
    if type(product['specifications']) == dict:
        for key, value in product['specifications'].items():
            product['specifications'][key] = value.strip(' ')
            if key == 'Net weight':
                value = value.strip(' ')
                product['specifications'][key] = (float(value.partition(' ')[0]), value.partition(' ')[2].lower())

    # reviews刪除不必要符號，w/或w/o改為with或without，❤改為love
    if type(product['reviews']) == list:
        lines =[]
        for line in product['reviews']:
            line = line.replace('*', '').replace('❤', '').replace('❁', '').replace('\n', '').replace('🤔', '')
            line = line.replace("[This review was collected as part of a promotion.]", '')
            line = line.replace('w/', 'with').replace('w/o', 'without').replace('w/out', 'without')
            lines.append(line)
        product['reviews'] = lines

    # 重新寫成新的文字檔csv
    with open('product_info_LA2_cleansed.csv', 'a', encoding='utf-8', newline='') as csv_file:
        # 把字典轉為csv格式寫入
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writerow(product)

    count += 1
    print(f"{count} finished.")
