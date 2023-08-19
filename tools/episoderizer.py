import json, os, sqlite3
anus = sqlite3.connect("newfag.db") 
finger = anus.cursor()

finger.execute("select * from posts where is_op=1;")
nig = finger.fetchall()
seasons = {1: ("Season One: Fuck Quest Classic", "FUCK QUEST Fan OVA", []),
    2: ("Season Two", "FUCK QUEST Season Finale: &quot;THE dARKBLOOM@STER&quot;", []),
    3: ("Season Three", "FUCK QUEST 3, Episode 12: &quot;Rose-sama: Love is War&quot;", []),
    4: ("Season Four", "FUCK QUEST OVA, PART 2: &quot;No Fuck No Life&quot;", []),
    5: ("Wesley's Bizarre Adventure", "Wesley&apos;s Bizarre Adventure, Episode 9: &quot;Yuri Camp&quot;", [])
}
pin = 1
for n in nig:
    tit = n[0]
    n = n[5]
    seasons[pin][2].append(n)    
    if tit in [jjj[1] for jjj in seasons.values()]: pin += 1
print(seasons)
f = open("episode_hints.json", "w")
f.write(json.dumps(seasons, indent=4))
f.close()