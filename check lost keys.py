import json
import pandas as pd

# 匯入Amy程式完成後的檔案，要事先檢查內容格式，確認是完整的list
with open('product_info_LA2.json', 'r', encoding='utf-8') as results:
    results_list = json.loads(results.read())
product_keyset = set()  # 整理出有抓出東西的keywords集合
for product in results_list:
    product_keyset.add(product['keyword'])

# 直接匯入原本的區域keywords檔，另外寫成一個集合
keywords = pd.read_csv('keywords_LA2.csv')
key_set = set(keywords['product_name'])

# 兩個集合相比對，抓出沒有結果的keywords
loss_set = key_set - product_keyset
loss_list = list(loss_set)
print(len(loss_list))
