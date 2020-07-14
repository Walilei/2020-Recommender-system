import json
from bs4 import BeautifulSoup

with open('product_info_LA2.json', 'r', encoding="utf-8") as file:
    product_list = json.loads(file.read())

# 清洗資料
count = 0  # 查看完成筆數用
for product in product_list:
    # 用BS處理HTML編碼，修改產品名稱內的亂碼，並去除換行符號
    product['name'] = BeautifulSoup(product['name'], 'lxml').text
    product['name'] = product['name'].replace("&amp;", "&").replace('\n', '')

    # 價格修改，先去除$符號和千分位逗號方便清洗
    product['price'] = product['price'].replace('$', '').replace(',', '')
    try:
        product['price'] = float(product['price'])
    except ValueError:
        if '-' in product['price']:
            # 取出區間的最大與最小值，算平均價格
            low_p = float(product['price'].partition('-')[0])
            high_p = float(product['price'].partition('-')[2])
            product['price'] = (low_p + high_p)/2
        else:
            print(f"{product['name']} has no price.")

    # 把評分改為tuple
    product['star_ratings'] = tuple(product['star_ratings'])

    # 刪除highlights內不必要的符號或句子
    if type(product['highlights']) == list:
        for i in range(len(product['highlights'])):
            useless01 = '(see nutrition information for Saturated Fat, and Sodium content)'
            useless02 = '(See nutrition for fat and saturated fat content.)'
            useless03 = '(Not a low calorie food. See nutrition information for calorie and sugar content.)'

            line = BeautifulSoup(product['highlights'][i], 'lxml').text
            line = line.replace('*', '').replace('●', '').replace('∙', '').replace(r'\n', '').replace('|', '')
            line = line.replace(useless01, '').replace(useless02, '').replace(useless03, '')
            product['highlights'][i] = line

    # 淨重項目改存為tuple，第一個元素為浮點數，第二個元素為小寫單位；去除每行開頭的空白
    if type(product['specifications']) == dict:
        for key, value in product['specifications'].items():
            product['specifications'][key] = value.strip(' ')
            if key == 'Net weight':
                value = value.strip(' ')
                product['specifications'][key] = (float(value.partition(' ')[0]), value.partition(' ')[2].lower())

    # 重新寫成新的文字檔
    with open('product_info_LA2_cleansed', 'a', encoding='utf-8') as file_1:
        json.dump(product, file_1, indent=4, ensure_ascii=False)
        file_1.write(',')

    count += 1
    print(f"{count} finished.")
