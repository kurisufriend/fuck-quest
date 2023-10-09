import os, subprocess
from PIL import Image

#homofix
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


wanting = os.listdir("./media")
dicked = os.listdir("./media/thumbs")
missing = []
good = 0
for m in wanting:
    if m in dicked or m.endswith(".webm") and m+".png" in dicked:
        good += 1
    else:
        missing.append(m)
print(missing)
print(good/len(wanting));input()

vivian = os.listdir("./media")
amber = vivian.copy()
amber.extend(os.listdir("./media/promoted"))

for fn in amber:
    if fn == "thumbs" or fn == "to_be_upgraded" or fn == "promoted" or fn == ".gitignore": continue
    frompath = f"./media/{'promoted/' if fn not in vivian else ''}"+fn
    if fn.endswith(".webm"):
        subprocess.call(['ffmpeg', '-i', frompath, '-ss', '00:00:00.000', '-vframes', '1', "./media/thumbs/"+fn+".png"])
        continue
    if os.path.exists("./media/thumbs/"+fn): continue
    print(fn)
    i = Image.open(frompath)
    i.thumbnail([125, 125])
    i.save("./media/thumbs/"+fn)