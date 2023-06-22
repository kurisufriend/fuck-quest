import sqlite3, requests, json, os, sys

uri = "https://archived.moe"
base = "/_/api/chan/"

h = """GET /_/api/chan/post/?board=qst&num=2494905 HTTP/3
Host: archived.moe
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Alt-Used: archived.moe
Connection: keep-alive
Cookie: foolframe_7Ww_theme=foolz%2Ffoolfuuka-theme-yotsubatwo%2Fyotsuba-b; foolframe_7Ww_csrf_token=647b9889caa618.50967497
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
TE: trailers"""
headers = {}
for k,v in [i.split(": ") for i in h.split("\n")[1:]]: headers[k] = v

def get_thread(board, id):
    print(uri+base+f"thread/?board={board}&num={id}")
    return requests.get(uri+base+f"thread/?board={board}&num={id}", headers=headers).json()

create_posts = """create table posts(
subject TEXT,
picrel TEXT,
name TEXT,
trip TEXT,
tim INTEGER,
post_number INTEGER,
op_no INTEGER,
original_board TEXT,
bod TEXT,
usr_id TEXT,
is_op INTEGER,
is_op_studios INTEGER,
is_story INTEGER,
next_story INTEGER,
is_lewd INTEGER,
next_lewd INTEGER
);"""

create_images = """create table images
"""

try: os.remove("newfag.db")
except FileNotFoundError: pass
anus = sqlite3.connect("newfag.db") 
finger = anus.cursor()

def commit_post_to_db(subject, picrel, name, trip, tim, post_number, op_no, original_board, bod, usr_id, is_op, is_op_studios,
is_story, next_story, is_lewd, next_lewd):
    j = locals().copy()
    k = lambda a: a.replace('"', '&quot;').replace('\'', '&apos;').replace("\n", "<br>")
    z = lambda a: f'"{k(str(a))}"' if type(a) == type("") else str(a)
    finger.execute(("insert into posts values(" + ",".join([z(j[i]) for i in commit_post_to_db.__code__.co_varnames]) + ");"))

notnull = lambda a: a if not(a == "null") else False

story_post_ids = []
lewd_post_ids = []
op_trips = ["!!q2GxCwU0EVE", "!cxIwUVBDkg"]

finger.execute(create_posts)
anus.commit()

f = open("thread_hints.json")
all_threads = json.loads(f.read())
f.close()

for ttt in all_threads:
    board = ttt[0]
    op_n = int(ttt[1])
    print("doing thread", op_n)

    thread = get_thread(board, op_n)
    op = thread[str(op_n)]["op"]
    posts = thread[str(op_n)]["posts"]
    thread_length = len(posts)
    ctr = 0
    for n in posts.keys():
        ctr += 1
        print("\b"*10, ctr, "out of", thread_length)
        cur = posts[n]
        commit_post_to_db(
            notnull(cur["title"]) or "",                                #subject
            "", # filename of the image TODO                                 #picrel
            notnull(cur["name"]) or "Anonymous",                        #name
            notnull(cur["trip"]) or "",                                 #trip
            int(notnull(cur["timestamp"])) or 0,                        #tim
            int(notnull(cur["num"])) or 0,                              #post_number
            int(op_n),                                                  #op_no
            board,                                                      #original_board
            notnull(cur["comment"]) or "DICKS EVERYWHERE",              #bod
            notnull(cur["poster_hash"]) or "000000",                    #usr_id
            1 if (notnull(cur["num"]) == str(op_n)) else 0,             #is_op
            1 if (notnull(cur["trip"]) in op_trips) else 0,      #is_op_studios
            1 if (notnull(cur["num"]) in story_post_ids) else 0,        #is_story
            -1, # next_story post TODO                                  #next_story
            1 if (notnull(cur["num"]) in lewd_post_ids) else 0,         #is_lewd
            -1 # next lewd post TODO                                    #next_lewd
        )
    n = op_n
    commit_post_to_db(
        notnull(op["title"]) or "",                                #subject
        "", # filename of the image TODO                                 #picrel
        notnull(op["name"]) or "Anonymous",                        #name
        notnull(op["trip"]) or "",                                 #trip
        int(notnull(op["timestamp"])) or 0,                        #tim
        int(notnull(op["num"])) or 0,                              #post_number
        int(op_n),                                                  #op_no
        board,                                                      #original_board
        notnull(op["comment"]) or "DICKS EVERYWHERE",              #bod
        notnull(op["poster_hash"]) or "000000",                    #usr_id
        1 if (notnull(op["num"]) == str(op_n)) else 0,             #is_op
        1 if (notnull(op["trip"]) in op_trips) else 0,      #is_op_studios
        1 if (notnull(op["num"]) in story_post_ids) else 0,        #is_story
        -1, # next_story post TODO                                  #next_story
        1 if (notnull(op["num"]) in lewd_post_ids) else 0,         #is_lewd
        -1 # next lewd post TODO                                    #next_lewd
    )
anus.commit()