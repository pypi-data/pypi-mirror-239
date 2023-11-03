#!/usr/bin/env python3


import os,sys 

LIB_NAME = 'isqdeployer' 


DIR =  os.path.realpath(os.path.dirname(__file__))
DOC = os.path.join(DIR,'docs') 
SOURCE = os.path.join(DOC,'source')

def delete_rst_butnot_index():
    print(os.listdir(SOURCE))
    files = [f for f in os.listdir(SOURCE) if f[-4:] =='.rst' and f != 'index.rst'] 
    for file in files:
        fpath = os.path.join(SOURCE,file) 
        os.remove(fpath)


def compile():
    os.chdir(DOC)
    cmd1 = f'''sphinx-apidoc -o ./source ../{LIB_NAME}/'''
    os.system(cmd1)
    os.system("make clean;make html")    




delete_rst_butnot_index()
compile()
compile()

print("done!")
