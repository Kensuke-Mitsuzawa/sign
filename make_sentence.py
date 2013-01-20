#! /usr/bin/python
# -*- coding:utf-8 -*-

#------------------------------------------------------------------------------------------------------------
#module to generate output(only sequence of morpheme)
#------------------------------------------------------------------------------------------------------------

#平叙文のときは入力と同じ並び順に出力したいので、以下の処理
def sentence_for_normal(set_dic):
    index_list = []
    sequence_list = []

    for one_key_in_dic in set_dic:
        tmp_list = set_dic[one_key_in_dic]
        order = (tmp_list[0]).order
        index_list.append(order)

    index_list.sort()

    for index in index_list:
        for one_key_in_dic in set_dic:
            
            tmp_list = set_dic[one_key_in_dic]
            if index == tmp_list[0].order:
                sequence_list.append(tmp_list)


    return sequence_list
    


def sentence_rule(set_dic,struc_dic):

    morp = {}
    
    # 平叙文のときは入力と同じ並びにしたいので
    if struc_dic['nor'] == 'OK':
        morp_list = []
        sequence_list = sentence_for_normal(set_dic)
        for list_2d in sequence_list:
            for instance in list_2d:
                morp_list.append(instance.morpheme)
        
    #形態素だけを表示するため、格の名前がkey、形態素並び（リスト）がvalueの辞書を作る
    if not struc_dic['nor'] == 'OK':
        for one in set_dic:
            instance = set_dic[one]
            morp_list = []
            for one_instance in instance:
                morp_list.append(one_instance.morpheme)
                morp_list.append(" ")
                morp_seq = "".join(morp_list)
            
            morp.setdefault(one,morp_seq)
    
    #set_dicの中にメインがあればをなんとかして記述
    if "main" in set_dic:
        #この記述は主格に修飾語がくっついている場合は問題になる
        person_number = (set_dic["main"])[0].person
        per = "pt(" + str(person_number) + ")"

    #--------------------------------------
    #ここから手話の単語並び文に関する記述
    print "Sign language word Sequence is"

    if not struc_dic["nor"] == []:
        format = " ".join(morp_list)
        format = format +" " +per
        print format

    if not struc_dic["passive"] == []:
        print morp["main"], morp["Ni"],morp["Predict"],per

    if not struc_dic["force"] == []:
        print morp["main"], morp["Ni"], per,morp["Wo"], morp["Predict"],"+顎あげ ","わかる(+うなずき) ",morp["Wo"], morp["Predict"]

    if not struc_dic["if"] == []:
        morp["main"],morp["Ni"],morp["Predict"]

     #--------------------------------------
