import json, os, sqlite3
anus = sqlite3.connect("newfag.db") 
finger = anus.cursor()

finger.execute("select * from posts where is_op_studios=1;")
story_posts = []

f = open("./fq-story-complete.txt", "r")
base = f.read()
f.close()
base = base.replace("\n", "")
base = base.replace(" ", "")

def fug():
    nig = finger.fetchall()
    for i in nig:
        n = i[5]
        is_op = i[10]
        bod = i[8].replace("&quot;", "\"").replace("&apos;", "'").replace("<br>", "").replace(" ", "")

        if is_op == "1":
            story_posts.append(n)
            continue
        cunny = int(len(bod)/2)
        if cunny+100 <= len(bod) and (bod[cunny:cunny+100] in base):
            story_posts.append(n)
fug()
print(story_posts)
f = open("./story_hints.json", "w")
f.write(json.dumps(story_posts))
f.close()