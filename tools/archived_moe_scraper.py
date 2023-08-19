import sqlite3, requests, json, os, sys, pathlib, re

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
    cached = pathlib.Path("./cache/"+board+str(id)).exists()
    if cached:
        f = open("./cache/"+board+str(id))
        res = json.loads(f.read())
        f.close()
        return res
    f = open("./cache/"+board+str(id), "w")
    res = requests.get(uri+base+f"thread/?board={board}&num={id}", headers=headers).json()
    f.write(json.dumps(res, indent=2))
    f.close()
    return res

create_posts = """create table posts(
subject TEXT,
picrel TEXT,
name TEXT,
trip TEXT,
tim INTEGER,
post_number INTEGER,
op_no INTEGER,
prev_op INTEGER,
next_op INTEGER,
original_board TEXT,
bod TEXT,
usr_id TEXT,
is_op INTEGER,
reply_count INTEGER,
is_op_studios INTEGER,
prev_op_studios INTEGER,
next_op_studios INTEGER,
is_story INTEGER,
prev_story INTEGER,
next_story INTEGER,
is_lewd INTEGER,
prev_lewd INTEGER,
next_lewd INTEGER,
is_ghost INTEGER
);"""

create_episodes = """create table episodes(
number INTEGER,
title TEXT
);"""

create_episode_assignments = """create table episode_assignments(
number INTEGER,
thread INTEGER
);"""

try: os.remove("newfag.db")
except FileNotFoundError: pass
anus = sqlite3.connect("newfag.db") 
finger = anus.cursor()

notnull = lambda a: a if not(a == "null") else False

next_op_studios_hints = json.loads(open("neo_next_op_studios_hints.json").read())
prev_op_studios_hints = {}
for k in next_op_studios_hints.keys():
    prev_op_studios_hints[str(next_op_studios_hints[k])] = str(k)
story_hints = json.loads(open("neo_story_hints.json").read())
lewd_hints = json.loads(open("lewd_hints.json").read())
story_hints.extend(lewd_hints) # all lewd posts are story posts, including pastebin ones.
story_hints = sorted(story_hints)
op_trips = ["!!q2GxCwU0EVE", "!cxIwUVBDkg", "!!gJwhmPB7G+T", "!!qBIEOkk6OUO"]

f = open("thread_hints.json")
all_threads = json.loads(f.read())
f.close()

bare_threads = [int(i[1]) for i in all_threads]

def commit_post_to_db(subject, picrel, name, trip, tim, post_number, op_no, prev_op, next_op, original_board, bod, usr_id, is_op, reply_count, is_op_studios,
prev_op_studios, next_op_studios, is_story, prev_story, next_story, is_lewd, prev_lewd, next_lewd, is_ghost):
    j = locals().copy()
    k = lambda a: a.replace('"', '&quot;').replace('\'', '&apos;').replace("\n", "<br>")
    z = lambda a: f'"{k(str(a))}"' if type(a) == type("") else str(a)
    finger.execute(("insert into posts values(" + ",".join([z(j[i]) for i in commit_post_to_db.__code__.co_varnames]) + ");"))

bigbook = {}
def commit_from_data(jsonbase, us_num, og_us_num, op_n, og_op_n, real_to_fake_tranny_dictionary, replies = -1):
    is_op_studios = (notnull(jsonbase["trip"]) in op_trips) and not((notnull(jsonbase["trip"]) == "!cxIwUVBDkg") and int(us_num) >= 15197)
        
    basexxx = notnull(jsonbase["comment"]) or "DICKS EVERYWHERE"
    if board == "qst" and is_op_studios:
        # fix OP italics, which were malformed for reasons not known to man
        ctr = 0
        while ctr < len(basexxx):
            if basexxx[ctr] == "m" and (ctr+4 < len(basexxx)) and basexxx[ctr:ctr+4] == "mu-i":
                basexxx = basexxx.replace("mu-i", "op-italics").replace("[/spoiler]", "</span>")
            ctr += 1

    # who are you meme arrow ing
    linez = [("<gt>"+l+"</gt>" if l.startswith(">") else l) for l in basexxx.split("\n")]
    basexxx = "\n".join(linez)

    # replace backlink deadnames with new ones that are heckin cute and valid
    ctr = 0
    while ctr < len(basexxx):
        if basexxx[ctr] == ">" and basexxx[ctr:ctr+2] == ">>" and not(basexxx[ctr:ctr+3] == ">>>"):
            ctr2 = ctr+2
            while ctr2 < len(basexxx) and (ord(basexxx[ctr2]) >= 48 and ord(basexxx[ctr2]) <= 57 ): ctr2 += 1
            target = basexxx[ctr:ctr2]
            if len(target) > 2 and real_to_fake_tranny_dictionary.get(target[2:]):
                rep = real_to_fake_tranny_dictionary[target[2:]]
                basexxx = basexxx.replace(target, f'<a href=[realquoterep]#{rep}[realquoterep]>'+">>"+rep+"</a>")
                #basexxx = basexxx[:ctr] + real_to_fake_tranny_dictionary[target[2:]] + basexxx[ctr2:]
                #print("okay NIGGER replacing", target[2:], "with", real_to_fake_tranny_dictionary[target[2:]])
                #print(target)
        ctr += 1

    # (;_;) <--- me (lazy bastard) (spoilers in raw CSS is easier anyway)
    basexxx = basexxx.replace("[spoiler]", "<spoiler>").replace("[/spoiler]", "</spoiler>")

    commit_post_to_db(
        notnull(jsonbase["title"]) or "",                                #subject
        "", # b64 of the image TODO                                 #picrel
        notnull(jsonbase["name"]) or "Anonymous",                        #name
        notnull(jsonbase["trip"]) or "",                                 #trip
        int(notnull(jsonbase["timestamp"])) or 0,                        #tim
        int(us_num),                              #post_number
        int(op_n),                                                  #op_no
        bigbook[str(bare_threads[bare_threads.index(int(og_op_n))-1])] if bare_threads.index(int(og_op_n))-1 >= 0 else -1,                                                  #prev_op
        int(op_n)+int(thread_length),                                    #next_op
        board,                                                      #original_board
        basexxx,              #bod
        notnull(jsonbase["poster_hash"]) or "000000",                    #usr_id
        1 if (str(us_num) == str(op_n)) else 0,             #is_op
        thread_length,                                                #reply_count
        1 if (is_op_studios) else 0,      #is_op_studios# magic number check is to circumvent false OP positives due to a cracked tripcode
        int(prev_op_studios_hints.get(str(us_num)) or -1),                                     #prev_op_studios
        int(next_op_studios_hints.get(str(us_num)) or -1),                                     #next_op_studios
        1 if (int(us_num) in story_hints) else 0,        #is_story
        story_hints[story_hints.index(int(us_num))-1] if int(us_num) in story_hints and story_hints.index(int(us_num))-1 >= 0 else -1, # prev_story                                  #prev_story
        story_hints[story_hints.index(int(us_num))+1] if int(us_num) in story_hints and story_hints.index(int(us_num))+1 < len(story_hints) else -1, # next_story post                                  #next_story
        1 if (int(us_num) in lewd_hints) else 0,         #is_lewd
        lewd_hints[lewd_hints.index(int(us_num))-1] if int(us_num) in lewd_hints and lewd_hints.index(int(us_num))-1 >= 0 else -1, # prev lewd post                                    #prev_lewd
        lewd_hints[lewd_hints.index(int(us_num))+1] if int(us_num) in lewd_hints and lewd_hints.index(int(us_num))+1 < len(lewd_hints) else -1, # next lewd post                                    #next_lewd
        0 if (jsonbase["subnum"] == "0") else 1                                     #is_ghost
    )

finger.execute(create_posts)
finger.execute(create_episodes)
finger.execute(create_episode_assignments)
anus.commit()

fake_n = 0

for ttt in all_threads:
    rtftd = {}
    board = ttt[0]
    op_n = int(ttt[1])
    fake_op_n = fake_n
    print("\ndoing thread", op_n)

    thread = get_thread(board, op_n)
    op = thread[str(op_n)]["op"]
    posts = thread[str(op_n)]["posts"]
    thread_length = len(posts)

    bigbook[str(op_n)] = str(fake_n)
    rtftd[str(op_n)] = str(fake_n)
    commit_from_data(op, fake_n, op_n, fake_op_n, op_n, rtftd, replies=thread_length)
    fake_n += 1

    ctr = 0
    for n in posts.keys():
        ctr += 1
        print("\b"*50, ctr, "out of", thread_length, end="")
        cur = posts[n]
        rtftd[str(n)] = str(fake_n)
        commit_from_data(cur, fake_n, n, fake_op_n, op_n, rtftd)
        fake_n += 1

print("\nloading episode data...")
episode_hints = open("episode_hints.json", "r")
edata = json.loads(episode_hints.read())
episode_hints.close()
for e in edata.keys():
    d = edata[e]
    finger.execute("insert into episodes values("+e+",\""+d[0]+"\");")
    for ep in d[2]:
        finger.execute("insert into episode_assignments values("+e+","+str(ep)+");")

anus.commit()