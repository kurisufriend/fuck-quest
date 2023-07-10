import json, os, sqlite3
anus = sqlite3.connect("newfag.db") 
finger = anus.cursor()

finger.execute("select post_number from posts where is_op_studios=1;")
al = finger.fetchall()

d = {}

i = 0
while i < len(al):
    n = al[i][0]
    print(n)
    if i+1 < len(al):
        d[int(n)] = int(al[i+1][0])
    i += 1
f = open("neo_next_op_studios_hints.json", "w")
f.write(json.dumps(d))
f.close()