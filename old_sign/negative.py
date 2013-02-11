#! /usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------------------
# module to detect negative information of KNP result. To detect negative information, regular expression is used
# 
#------------------------------------------------------------------------------------------------------------



import re

def find_negation(clause_list,clause_num,clause):
    #否定形 or not 否定じゃなければ１を返す
    negative_value = 0
    
    #カウンターの設置
    counter = 0
    
    #ここで新しい節を読みおなし
    for value in clause:

        if counter == 0:
            start_pos = 1
            end_pos = value

        else:
            start_pos = end_pos + 1
            end_pos = end_pos + value

        counter += 1

        #情報の抽出を正規表現でしていく
        for i in range(start_pos,end_pos + 1):
            sentence = clause_list[i]
            
            #+以降が単語に関する情報の（はず）なので、ここから情報を抽出する
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<否定表現>",sentence) == []:
                    #否定なら１を返す
                    negative_value = 1


    return negative_value



def negation(clause_list,clause_num,clause):
    #否定文に関する処理を行う
    print "--------------------------"
    print "About negative information\n"

    #どの否定形か？を管理する変数
    negative = ""
    
    #カウンターの設置
    counter = 0
    
    #ここで新しい節を読みおなし
    for value in clause:

        if counter == 0:
            start_pos = 1
            end_pos = value

        else:
            start_pos = end_pos + 1
            end_pos = end_pos + value

        counter += 1

        #情報の抽出を正規表現でしていく
        for i in range(start_pos,end_pos + 1):
            sentence = clause_list[i]
            
            #+以降が単語に関する情報の（はず）なので、ここから情報を抽出する
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<否定表現>",sentence) == []:
                    choice = raw_input("1 意思の否定 2 所有・存在の否定 3 完了の否定 4 不可能の意味 5 経験の否定 6 必要性の否定\n")
                    choice = int(choice)
                    if choice == 1:
                        negative = "willness"
                    if choice == 2:
                        negative = "posess"
                    if choice == 3:
                        negative = "perfect"
                    if choice == 4:
                        negative = "impossible"
                    if choice == 5:
                        negative = "experience"
                    if choice == 6:
                        negative = "need"

            #否定表現がなかった時。つまり否定文じゃなかった時
            #else:
            #    negative = ""

    #-------------------------------
    #単なる表示の都合上
    if not negative == "":
        print negative,"is selected"
    #-------------------------------
                   
    return negative

