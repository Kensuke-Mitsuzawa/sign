#! /usr/bin/python
# -*- coding: utf-8 -*-
#coding: UTF-8

import sys
import codecs
import re

# 結局、使ってないけど一応残しておく
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

# dは分解した要素を保存しておくための辞書
d ={}

for line in cf:
    print "-------------------------"

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
            #処理にまったく関係ないが見やすくするために|をいれる。
            tag_info_list.append(u"|")
            tag_info_list.append(u" ")
            continue
                
        if re.compile("[1-9]").search(char_list[0]):
            tag_info_list.append(u"*")
            tag_info_list.append(int(char_list[0]))
            tag_info_list.append(u"D")
            tag_info_list.append(u"|")
            tag_info_list.append(u" ")
            continue
            
            #これで末尾に*,番号,D]か-,番号,D]のどちらかのリストができあがっているはず


    if len(line) > 23:
        print line
        # ","で区切ってリストに追加する
        word_info_list = line.split(",")

        #語情報の先頭は空白でつながったままなので、分解して「語」をtag_info_listの最後に、「品詞」をword_info_listの先頭に入れる。
        #だいぶ後だしじゃんけん的な処理なので、コードを書き換える時は要注意
        tmp = word_info_list[0]
        tmp_splitted = tmp.split(" ")
        tag_info_list[-1] = tmp_splitted[0]
        word_info_list[0] = tmp_splitted[-1]
        
        #リスト末尾にブロック内番号を追加
        word_info_list.append(no_in_block)

        #ホントはもっと後でする処理だけど、書き忘れ防止に。
        no_in_block += 1
            
        #２つの情報リストを結合する
        info_list = tag_info_list + word_info_list

        print info_list[9],info_list[10]
        

        key = str(tag_info_list[1]) + str(no_in_block)
        # ここでエラーが出るようならぜんぶstrにしてしまっていいだろう

        print key
        print "-------------------------"

       #実は下の命令でも d[key] = info_listでも同じ結果になる。一応残しておく
       #ここで並びがおかしくなるエラーが起きている可能性がある。
       # for tmp in info_list:
       #     d.setdefault(key,[]).append(tmp)

        d[key] = info_list
        print d

    else :
        pass

#ここより以下は関数にしてもいいんだろうが、めんどくさいのでパス



#リストの復元

dic_list = d.values()
#for tmp in range(len(dic_list)):
#    print "info_list_" + str(tmp)
    

#ここからルールを書いていく。
info_list_1 = dic_list[0]
info_list_2 = dic_list[1]
info_list_3 = dic_list[2]
info_list_4 = dic_list[3]
info_list_5 = dic_list[4]

print info_list_1[9],info_list_1[10]
print info_list_2[9],info_list_2[10]
print info_list_3[9],info_list_3[10]
print info_list_4[9],info_list_4[10]
print info_list_5[9],info_list_5[10]




if info_list_1[10] == u"名詞": #and info_list_1[11] ==u"固有名詞" and info_list_1[12] == u"人名" and info_list_1[13] == u"姓":
    print "ok"
    if info_list_2[10] == u"助詞" and info_list_2[11] == u"格助詞" and info_list2[12] == u"引用":

        if info_list_3[10] == u"動詞" and info_list_3[11] == u"自立":

            print "OK"

    
    
    


