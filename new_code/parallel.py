#! /usr/bin/python
# -*- coding:utf-8 -*-





def heiretsu(out_list):
    """
    並列語句の処理をするモジュール。
    節単位の並列はここでは扱わない。

    並列を起こしている最後の句ではcheckがyesにならない（KNPの仕様かと思う）
    なので、直前までのcheckがyesであれば、次の句も並列と見なして並列リストに追加する

    節単位の並列はattributeのpara_cehckが'yes'であっても、並列基本句数が表示されない（並列していのが節だから）
    これを利用して、節の並列なのか？それとも句の並列なのか？の判断を行う

    """

    #ヒューリスティックな方法だけど、これでなんとかなる
    para_list = []
    prev_para = "no"
    para_check = "no"
    for one_dim in out_list:
        one_dim_list = []
        for two_dim in one_dim:
            
            if two_dim.para_check == "yes" and not two_dim.p_p_num == "":
                """
                節構造の並列の処理を避けるため,not p_p_num == ""を記述
                """
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
            
            if two_dim.para_check == "yes" and prev_para == "no":
                """
                節構造の並列用に記述
                節の並列ではcheckはyesになるが、prev_paraはno
                """
                one_dim_list.append(two_dim)
                continue
 
        para_list.append(one_dim_list)
    
    #並列がない場合、二次元リストになって困るので、便宜上リストのindex0に空リストの挿入
    if para_check == "no":
        para_list[0].append([])

    print "parallel kihon phrase is",para_list

    return para_list
