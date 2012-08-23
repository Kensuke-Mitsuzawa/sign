#! /usr/bin/python
# -*- coding: utf-8 -*-
#coding: UTF-8

import sys
import codecs
import re

class word_info:

    def __init__(self,word,pos,pos_m,func,func_m,kana):
        self.word = word
        self.pos = pos
        self.pos_m = m
        self.func = func
        self.func_m = func_m
        self.kana = kana

class depen_part(word_info):

    def __init__(self,dep,word_num,*av):
        word_info.__init__(self,*av)
        self.dep = dep
        self.word_num = word_num
        




element=[]
cabocha_file = codecs.open('test.txt','r','utf-8')
#cf = cabocha_file.decode('utf-8')
cf = cabocha_file.readlines()
# EOSのタグを消去するための処理
cf.pop()

for line in cf:
    print line

    if len(line) == 22:
        #char_listをリセットする
        char_list = []
        
        #ブロック内番号をリセットする
        no_in_block = 0
        #情報をリスト化。空白区切りを行う
        tag_info_list = line.split(" ")
        #番号Dはインデックス[2]に入っている
        dep_tag = tag_info_list[2]

        #-*Dか*Dをリストに追加していく
        for char in dep_tag:
            char_list.append(char)
            
            
        #もし−記号なら、−記号を追する
        if char_list[0] == "-":
            tag_info_list.append(u"-")
            tag_info_list.append(int(char_list[1]))
            tag_info_list.append(u"D")

            continue
                
        if re.compile("[1-9]").search(char_list[0]):
            tag_info_list.append(u"*")
            tag_info_list.append(int(char_list[0]))
            tag_info_list.append(u"D")

            continue
            
            #これで末尾に*,番号,D]か-,番号,D]のどちらかのリストができあがっているはず


    if len(line) > 23:

            # ","で区切ってリストに追加する

            word_info_list = line.split(",")
        

            #リスト末尾にブロック内番号を追加
            word_info_list.append(no_in_block)
            

            #ホントはもっと後でする処理だけど、書き忘れ防止に。
            no_in_block += 1
            
            #２つの情報リストを結合する
            info_list = tag_info_list + word_info_list

            key = str(tag_info_list[1]) + str(no_in_block)
            # ここでエラーが出るようならぜんぶstrにしてしまっていいだろう

            d = {}

            for tmp in info_list:
                d.setdefault(key,[]).append(tmp)

            print d

    else :
        pass





    

#for line in cf:
    
#input_sentence = sys.stdin.readline()
#input_sentence = input_sentence.decode('utf-8')


