#! /usr/bin/python
# -*- coding:utf-8 -*-


#入力文が複数節なのか？単節なのか？を判断する。返すのは二値。yes or no
def clause_check(out_list):
    #どうも節には主節、連用節、連体節があるくさいが、とりあえずは、主節 or notで判断してもいいだろう
    main_c = ""
    sub_c = ""
    #返り値
    multi_c = ""
    
    for one_p in out_list:
        
        if one_p.c_clause_type == "主節":
            main_c = "yes"

        #ちょっと条件が特殊。連用節か連体節　かつ　not　修飾語　を満たす時、sub節と見なす。
        if (one_p.c_clause_type == "連用節"  or one_p.c_clause_type == "連用節") and not one_p.modify_check == "yes":
            sub_c = "yes"

    if main_c == "yes" and sub_c == "yes":
        multi_c = "yes"

    if main_c == "yes" and not sub_c == "yes":
        multi_c = "no"
        

    return multi_c


#複数の節があるときに、まとめあげる関数
def make_clause_set(input_list):
    
    #一時的なリスト
    tmp_list = []
    
    #文全体のリスト
    sentence_list = []

    for one_node in input_list:
    
        if one_node.c_clause_type == "連用節" and not one_node.modify_check == "yes":
           
            tmp_list.append(one_node)
            sentence_list.append(tmp_list)
            #一時リストを再初期化
            tmp_list = []
            continue     

        if one_node.c_clause_type == "連体節" and not one_node.modify_check == "yes":
    
            tmp_list.append(one_node)
            sentence_list.append(tmp_list)
            #一時リストを再初期化
            tmp_list = []
            continue
            
        if one_node.c_clause_type == "主節":
            tmp_list.append(one_node)
            sentence_list.append(tmp_list)
            #一時リストを再初期化
            tmp_list = []
            continue

        else:
            tmp_list.append(one_node)
            continue


    return sentence_list
