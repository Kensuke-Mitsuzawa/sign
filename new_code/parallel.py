#! /usr/bin/python
# -*- coding:utf-8 -*-



def heiretsu(out_list):
    """
    並列語句の処理をするモジュール。
    節単位の並列はここでは扱わない。
    """

    #ヒューリスティックな方法だけど、これでなんとかなる
    para_list = []
    prev_para = "no"
    para_check = "no"
    for one_dim in out_list:
        one_dim_list = []
        for two_dim in one_dim:
            
            if two_dim.para_check == "yes":
                new_para_list = []
                new_para_list.append(two_dim)
                prev_para = "yes"
                para_check  = "yes"
                continue
                
            if two_dim.para_check == "" and prev_para == "yes":
                new_para_list.append(two_dim)
                one_dim_list.append(new_para_list)
                prev_para = "no"
                continue
                
            if two_dim.para_check == "" and prev_para == "no":
                one_dim_list.append(two_dim)
                continue

        para_list.append(one_dim_list)
    
    #並列がない場合、二次元リストになって困るので、便宜上リストのindex0に空リストの挿入
    if para_check == "no":
        para_list[0].append([])

    print "parallel kihon phrase is",para_list

    return para_list
