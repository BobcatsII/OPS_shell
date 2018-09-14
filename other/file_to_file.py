#!/usr/bin/python
#coding:utf8
import os
import sys

filedir = "/home/ss/pre_5.3.30/"
mydir = sys.argv[1]

num = 0
os.chdir(filedir + mydir)
conf_lst = os.listdir(filedir + mydir)
for i in conf_lst:
    num += 1
    with open(i, 'r') as f:
        f_content = f.readlines()
        for j in f_content:
            if j == '\n':
                continue
            else:
                new_f = open("application_pre.properties", "a")
                new_f.writelines(j)
        new_f.write("\n\n\n")
        new_f.close()
        os.remove(i)
        if num == len(conf_lst):
            break
