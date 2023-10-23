import json, os, sqlite3
anus = sqlite3.connect("newfag.db") 
finger = anus.cursor()

finger.execute("select * from posts where is_op_studios=1;")
lewd_posts = []

f = open("./lewd-total-compendium.txt", "r")
base = f.read()
f.close()
base = base.replace("\n", "")
base = base.replace(" ", "")

def fug():
    nig = finger.fetchall()
    for i in nig:
        n = i[7]
        is_op = i[14]
        obod = i[12]
        bod = i[12].replace("&quot;", "\"").replace("&apos;", "'").replace("<br>", "").replace(" ", "")
        if n=="44638": 
            print(len(obod), bod)
            input()
        if len(obod) < 50 and "pastebin.com" in bod:
            lewd_posts.append(n)
            continue
        cunny = int(len(bod)/2)
        if cunny+100 <= len(bod) and (bod[cunny:cunny+100] in base):
            lewd_posts.append(n)
fug()
f = open("./lewd_hints.json", "w")
f.write(json.dumps(lewd_posts))
f.close()