from mylib import helper as h
import random
import mlflow
import sklearn as sk
from random import randint
from urllib.parse import quote as qt
import urllib.parse as ps

# ensure PYTHONPATH is set to the myplugins path
def test():
    if True:
        return 5
    return 5

def test2():
    if True:
        return 1
    return 5

def test3():
    random.randint(1, 10)
    randint(2,4)
    ps.quote('testing321')
    # random.random()
    if random.random() > 0.5:
        return 2
    return 2

def test4(v):
    return v

a = "Hello, world!"
# print("Hello, world!")
c = "Hello," + " world!"

h.dosomething(11 + 5)
# this is not scanned, cos not defined here
# we want to try 
# not using funcdef, but some func visit/call
# but this might be runtime not static
# nodes: https://astroid.readthedocs.io/en/latest/api/astroid.nodes.html

# 1. can we track function call of imported module?
# 2. can we get the original module name if aliased?

z = 99

# pylint: disable=hello-world
d = "Hello, world!"
e = d

local_path1 = "./home/something"
local_path2 = "./cdsw/something"
local_path3 = "cdsw/"
local_path4 = "home/"
local_path5 = "/cdsw"
local_path6 = "/home"
# test4('/home/something')
qt('testing')
# false positives
cdsw_safe = "nothing"

