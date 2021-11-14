import time
import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict

domain_data = json.load(open('./dataset/domain.json', mode='r', encoding="utf-8"))
domain_seconds = []
for domain in domain_data.keys():
    domain_seconds.append('.'.join(domain.split('.')[1:]))
# domain_seconds = domain_seconds[:10]
print(domain_seconds)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
           "Accept": "*/*"}
domain_data = ["tmall.com", "Qq.com"]
urls = ["https://top.chinaz.com/Html/site_" + domain_second + ".html" for domain_second in domain_seconds]
domain_dict_all = defaultdict(lambda: 0)
count = 0
for url in urls:
    session = requests.Session()
    response = session.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    domain_name_all = []
    domain_value_all = []
    # 备案信息
    ICP = soup.findAll("li", {"class": "TMain06List-Left fl"})[0].findAll("p")
    for content in ICP[1:]:
        content = [element.string.encode("utf-8").decode() for element in content.contents]
        for i in content:
            name, value = i.split("：")
            domain_name_all += [name]
            domain_value_all += [value]

    # 服务器信息
    SERVER = soup.findAll("li", {"class": "TMain06List-Cent fl"})[0].findAll("p")
    for content in SERVER[1:]:
        content = [element.string.encode("utf-8").decode() for element in content.contents]
        for i in content:
            name, value = i.split("：")
            domain_name_all += [name]
            domain_value_all += [value]

    # 域名信息
    Domain = soup.findAll("li", {"class": "TMain06List-right fl"})[0].findAll("p")
    for content in Domain[1:]:
        content = [element.string.encode("utf-8").decode() for element in content.contents]
        for i in content:
            name, value = i.split("：")
            domain_name_all += [name]
            domain_value_all += [value]
    domain_dict = dict(zip(domain_name_all, domain_value_all))
    domain_dict_all[".".join(url.split("/")[-1].split("_")[-1].split(".")[:-1])] = domain_dict
    if count in list(range(100, len(domain_seconds)-1, 100)):
        time.sleep(3600)
    count += 1

file = './dataset/domain_message_zhanzhang.json'
with open(file, mode='w', encoding='utf-8') as f:
    json.dump(domain_dict_all, f, ensure_ascii=False)






























