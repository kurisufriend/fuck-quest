# strategy for scraping down imgs:
#   - for /a/ block, take thumbs from archived.moe be polite while scraping.
#       - then, upgrade these thumbs to fullsize through reverse searching, hash checking, etc.
#       - look for the screenshot/manual archives one anon had for help in manual upgrades
#   - for /tg/ and /qst/ try for full from suptg politely
#       - then try archived
import requests, json, os, datetime, time, sys

manifest = {}

breads = os.listdir("./cache/")

# construct image manifest
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
        res = []
        res_thumbs = []
        if bread[0] == "a":
            pass
        else:
            suptg_url = f"https://suptg.thisisnotatrueending.com/{board if board == 'qst' else ''}archive/{year}/{num}/{'thumbs' if board == 'qst' else 'images'}/{poast['media']['media_orig']}"
            res.append(suptg_url)

        if poast["media"].get("media_link"):
            res.append(poast["media"]["media_link"])
        if poast["media"].get("thumb_link"):
            res_thumbs.append(poast["media"]["thumb_link"])

        manifest[board+poast['media']['media_orig']] = {}
        manifest[board+poast['media']['media_orig']]["filename"] = poast["media"]["media_filename"]
        manifest[board+poast['media']['media_orig']]["spoiler"] = poast["media"]["spoiler"]
        manifest[board+poast['media']['media_orig']]["sources"] = res
        manifest[board+poast['media']['media_orig']]["thumbs"] = res_thumbs


#check against manifest
med = os.listdir("media/")
low_self_esteem = med.copy()
low_self_esteem.extend(os.listdir("media/thumbs"))
good = 0
goodl = 0
missing = []
for mk in manifest.keys():
    if mk in med:
        good += 1
    if mk in low_self_esteem:
        goodl += 1
    else:
        missing.append(manifest[mk])
print(json.dumps(missing, indent=2))
print("total missing", len(missing))
print("missing .webm", len([i for i in missing if i["filename"].endswith(".webm")]))
print(f"{goodl/len(manifest)*100}% low self esteem coverage");
print(f"{good/len(manifest)*100}% coverage");input()

print(json.dumps(manifest, indent=2))

f = open("proxies.txt", "r")
proxies = f.read()
f.close()
proxies = [i.split(":") for i in proxies.split("\n") if i]
proxies = [f"socks5h://{i[2]}:{i[3]}@{i[0]}:{i[1]}" for i in proxies if i]
proxy_iter = 20

# fetch imgs
for imagek in manifest.keys():
    image = manifest[imagek]

    status = 0
    tries = 0
    while status != 200 and tries <= 1:

        
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
        isthumb = image["sources"] == []
        endpoint = image["thumbs"][0] if isthumb else image["sources"][(proxy_iter % 2) % len(image["sources"])]

        if os.path.exists("media/"+("to_be_upgraded/" if isthumb else "")+imagek):
            print(imagek, "found, go around...")
            break

        time.sleep(.01)
        print(endpoint)
        try: r = requests.get(endpoint, headers=headers, proxies=req_prox)
        except requests.exceptions.ConnectionError as e:
            print("conn err")
            status = -1337
            continue
        status = r.status_code
        if r.content == bytes():
            status = 404
        print(r.status_code)

        if status == 200:
            f = open("media/"+("to_be_upgraded/" if isthumb else "")+imagek, "wb")
            f.write(r.content)
            f.close()
        tries += 1
