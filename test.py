#!/usr/bin/env python3
from os import system
from sys import argv
from secrets import token_hex
from json import loads, dumps

flags = []
if len(argv) <= 1:
    flags.extend(["pm", "m", "r", "t"])
else:
    flags.extend(argv[1:])

if "pm" in flags:
    system("premake5 gmake2")
if "m" in flags:
    #system("rm -r obj/*")
    system("rm ./bin/Debug/FQarch")
    system("make config=debug")
if "r" in flags:
    print("running~~~")
    system("./bin/Debug/FQarch")
if "d" in flags:
    system("gdb ./bin/Debug/FQarch")
if "pr" in flags:
    system("valgrind --tool=callgrind bin/Debug/FQarch ./sample/")
    system("kcachegrind ./callgrind*")