#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys,re

f = open(sys.argv[1])

lines = f.readlines()
element_list = []
for line in lines:
    if not re.findall(r"\+ \dD|\+ -\dD|\+ \dP|\+ -\dP",line) == []:
        tmp_list = []
        tmp_list = line.split("<")
        for element in tmp_list:
            
            if re.findall(r"\+ \dD|\+ -\dD|\+ \dP|\+ -\dP",element) == []:
                if re.findall(r"格解析結果|正規化代表表記|用言代表表記|区切|格関係",element) == []:
                    if not element in element_list:
                        element_list.append(element)

element_list.append("格解析結果")
element_list.append("正規化代表表記")
element_list.append("用言代表表記")
element_list.append("区切")
element_list.append("格関係")


print element_list
for each in element_list:
    print each
