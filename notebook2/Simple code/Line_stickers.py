
import os

from bs4 import BeautifulSoup

#import lxml
import requests


url = 'https://store.line.me/stickershop/product/6310/zh-Hant'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

line_stickers = []

# 取得每個貼圖連結
for tag in soup.find_all('span', 'mdCMN09Image'):
    style = tag['style']
    l_parentheses = style.rfind('(') + 1
    r_parentheses = style.rfind(')')
    path = style[l_parentheses:r_parentheses]
    line_stickers.append(path)
    print(path)
    
# 取得標題並建立該標題的資料夾
title = soup.title.text.split(':')[0].strip()
if not os.path.exists(title):
    os.mkdir(title)
    
# 下載貼圖
for url in line_stickers:
    local_filename = url.split('/')[-1]
    response = requests.get(url, stream=True)
    with open(os.path.join(title, local_filename), 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print('{} Downloaded!'.format(local_filename))
print('Completed!')