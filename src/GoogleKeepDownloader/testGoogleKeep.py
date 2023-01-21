import requests
from io import BytesIO
from PIL import Image
import time
import pandas as pd
import matplotlib.pyplot as plt
#
#
url = "https://keep.googleapis.com"
res = requests.get(url)
# request.get 요청
#
links = []
for j, line in enumerate(res.content.decode().split(',')):
    print(line)
    # if line.find('https://lh3.google')!=-1:
    #     links.append(line)

print(links)
print(len(links))
print(res.content[:100])
# res2 = requests.get(links[299][2:-1])
# print(res2.content)
#
# img = Image.open(BytesIO(res2.content))
# plt.imshow(img)
#

