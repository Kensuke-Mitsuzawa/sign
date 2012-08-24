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
dd ={}

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

        #辞書のキーを作る。ブロック番号+ブロック内番号にしたい(ex.01,02,11,12..)
        #ので、一度、文字型で２つの情報をくっつけてから整数型に変換する
        #01,02の0が消えてしまうが妥協する。
        key = str(tag_info_list[1]) + str(no_in_block)
        key = int(key)
        

        print "key no. is",key
        print "-------------------------"

       #実は下の命令でも d[key] = info_listでも同じ結果になる。一応残しておく
       # for tmp in info_list:
       #     d.setdefault(key,[]).append(tmp)

        d[key] = info_list
        
    else :
        pass
       
#ここより以下は関数にしてもいいんだろうが、めんどくさいのでパス



#リストの復元

dic_list = d.values()

# info_list_は二次元配列で定義する。なので[][]の１つめの[]が、何番目形態素か？２つめの[]が、その形態素の中身
info_list_ = []
for tmp in range(len(dic_list)):
    info_list_.append(dic_list[tmp])
    

#ここからルールを書いていく。
# ルールガイド
# リストの順番は [0]は*,[1]は形態素区切り番号,[2]は係り受け情報,[3]は不明,[4]は不明,[5]はかかり元*か被かかり-か,[6]はかかり文番号,[7]いつも"D",[8]は空き"|",[9]は語,[10]は品詞,[11]は品詞（詳しく）,[12]は機能,[13]は機能(詳しく),[14]は何型動詞か,[15]は動詞が何形か,[16]は語の原形,[17]は仮名,[18]は活用の仮名表示とスペースのあとに不明なタグ（[18]は使わない方がいい)

#<名前>と申します。　
if info_list_[0][10] == u"名詞" and info_list_[0][11] ==u"固有名詞" and info_list_[0][12] == u"人名" and info_list_[0][13] == u"姓":
    
    if info_list_[1][10] == u"助詞" and info_list_[1][11] == u"格助詞" and info_list_[1][12] == u"引用":

        if info_list_[2][10] == u"動詞" and info_list_[2][11] == u"自立":

            print u"{<t> pt(1) 名前} %s。" % info_list_[0][9]

#あなたのお名前はなんとおっしゃいますか？
# ここらへん、dep情報も活用したいのだが、リストの自動作成がまだできてないので、実現してない.
# ホントなら、〜にかかってたらというif文もつくりたいのだが
if info_list_[0][10] == u"名詞" and info_list_[0][11] == u"代名詞" and info_list_[0][12] == u"一般":

    if info_list_[1][10] == u"助詞" and info_list_[1][11] == u"連体詞":

        if info_list_[2][10] == u"接頭辞" and info_list_[2][11] == u"名詞接続":

            if info_list_[3][10] == u"名詞" and info_list_[3][11] == u"一般":

                if info_list_[4][10] == u"助詞" and info_list_[4][11] == u"係助詞":

                    if info_list_[5][10] == u"副詞" :

                        if info_list_[6][10] == u"動詞" and info_list_[6][11] == u"自立":

                            if info_list_[7][10] == u"助動詞":

                                if info_list_[9][10] == u"記号,一般":

                                    print "{<t> pt(2) 名前}{<whq> 何?}"


#あなたの手話の先生はだれですか？

if info_list_[0][10] == u"名詞" and info_list_[0][11] == u"代名詞" and info_list_[0][12] == u"一般":

    if info_list_[1][9] == u"の":

        if info_list_[2][9] == u"手話":

            if info_list_[3][9] == u"の":

                if info_list_[4][9] == u"先生":

                    if info_list_[5][9] == u"は":

                        if info_list_[6][9] == u"だれ":

                            if info_list_[7][9] == u"です":

                                if info_list_[8][9] == u"か":

                                    print "{<t> %s 手話　先生}{<whq> 誰　pt(3)?}" % info_list_[0][9]

                                
    
    
#あなたは佐藤さんですか？

if info_list_[0][9] == u"あなた" and info_list_[0][10] == u"名詞" and info_list_[0][11] == u"固有名詞" and info_list_[0][12] == u"一般":

    if info_list_[1][9] == u"は":

        if info_list_[2][10] == u"名詞" and info_list_[2][11] == u"固有名詞" and info_list_[2][12] == u"人名" and info_list_[2][13] == u"姓":

            if info_list_[3][9] == u"さん":

                if info_list_[4][9] == u"です":

                    if info_list_[5][9] == u"か":

                        print "{<t> pt(2)} %s  pt(2)?" % info_list_[2][9]

