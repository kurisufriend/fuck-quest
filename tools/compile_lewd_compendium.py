from os import listdir

acc = ""
for fn in [i for i in listdir("./lewd") if i.endswith(".txt")]:
    f = open("./lewd/"+fn)
    acc += f.read()
    f.close()
f = open("./lewd-total-compendium.txt", "w")
f.write(acc)
f.close()