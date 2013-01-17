#! /usr/bin/python
# -*- coding:utf-8 -*-


def sentence_rule(set_dic,struc_dic):

    morp = {}
    
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
        print morp["main"],morp["Ga"],morp["Predict"],per

    if not struc_dic["passive"] == []:
        print morp["main"], morp["Ni"],morp["Predict"],per

    if not struc_dic["force"] == []:
        print morp["main"], morp["Ni"], per,morp["Wo"], morp["Predict"],"+顎あげ ","わかる(+うなずき) ",morp["Wo"], morp["Predict"]

    if not struc_dic["if"] == []:
        morp["main"],morp["Ni"],morp["Predict"]


     #--------------------------------------
