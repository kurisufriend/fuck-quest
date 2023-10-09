# king me
import requests, os, json, datetime, threading


f = open("proxies.txt", "r")
proxies = f.read()
f.close()
proxies = [i.split(":") for i in proxies.split("\n") if i]
proxies = [f"socks5h://{i[2]}:{i[3]}@{i[0]}:{i[1]}" for i in proxies if i]
proxy_iter = 20

breads = os.listdir("./cache/")



remlnks = {}

for bread in breads:
    if bread == ".gitignore": continue
    f = open("./cache/"+bread)
    jbread = json.loads(f.read())
    f.close()
    num = bread.replace("a", "").replace("tg", "").replace("qst", "")
    board = {"a": "a", "q": "qst", "t": "tg"}[bread[0]]
    jbread = jbread[num]
    jbread["posts"][num] = jbread["op"]
    jbread = jbread["posts"]
    year = datetime.date.fromtimestamp(jbread[num]["timestamp"]).year
    for poastk in jbread.keys():
        poast = jbread[poastk]
        if poast.get("media") == None: continue
        if bread[0] != "a":
            continue

        if poast["media"].get("remote_media_link"):
            remlnks[board+poast["media"]["media_orig"]] = poast["media"]["remote_media_link"]

s_o_ytc_kayos_the_real_ones = os.listdir("./media/promoted")
print(len(remlnks));input()

def attempt_set_promotion(remlnks, big):
    global proxy_iter
    for idx, remlnk in enumerate(remlnks):
        if remlnk in s_o_ytc_kayos_the_real_ones: continue
        print(idx, len(remlnks))
        proxy_iter += 1
        proxy = proxies[proxy_iter % len(proxies)]
        print(proxy)
        req_prox = {
            "https": proxy,
            "http": proxy
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            # 'If-Modified-Since': 'Mon, 10 Mar 2014 09:18:06 GMT',
            # 'If-None-Match': '"531d834e-7d2"',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        while True:
            try:
                r = requests.get(big[remlnk], headers=headers, proxies=req_prox)
            except requests.exceptions.ConnectionError as e:
                print(e)
                continue
            break
        if r.status_code != 200:
            print("FUCK?ING FAULKED WHAT THE FUCK~~~@@@~!!")
            continue
        link = str(r.content)
        link = link[link.find("url=")+4:].split("\"")[0]
        for i in range(3):
            try: 
                proxy_iter += 1
                proxy = proxies[proxy_iter % len(proxies)]
                print(proxy)
                req_prox = {
                    "https": proxy,
                    "http": proxy
                }
                r = requests.get(link, headers=headers, proxies=req_prox)
            except requests.exceptions.ConnectionError as e:
                print(e)
                continue
            break

        if r.status_code == 200:
            f = open("media/promoted/"+remlnk, "wb")
            f.write(r.content)
            f.close()
        else:
            print(r.status_code)

        print(remlnk) 

subsets = [list(remlnks.keys())[x:x+50] for x in range(0, len(remlnks.keys()), 50)]
for subset in subsets:
    threading.Thread(target=attempt_set_promotion, args=(subset,remlnks)).start()