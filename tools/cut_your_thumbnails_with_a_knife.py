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

for fn in os.listdir("./media"):
    if fn == "thumbs" or fn == "to_be_upgraded" or fn == ".gitignore": continue
    if fn.endswith(".webm"):
        subprocess.call(['ffmpeg', '-i', "./media/"+fn, '-ss', '00:00:00.000', '-vframes', '1', "./media/thumbs/"+fn+".png"])
        continue
    if os.path.exists("./media/thumbs/"+fn): continue
    print(fn)
    i = Image.open("./media/"+fn)
    i.thumbnail([125, 125])
    i.save("./media/thumbs/"+fn)