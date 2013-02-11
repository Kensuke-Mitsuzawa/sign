#! /usr/bin/python
# -*- coding:utf-8 -*-

def modi(out_list):
    """
    修飾情報のリストを構築する
    """

    dep_info_list = []
    
    for one_dim in out_list:
        for_two_dim_list = []
        for two_dim in one_dim:
            for_three_dim_list = []
            #ここで２次元目の要素の追加を開始
            #もし,two_dimが３次元目のリストなら,attributeを持たないので,isinstanceでtru or falseの判断を行う
            #もし、リストでなければ（インスタンスであれば）
            if not isinstance(two_dim,list):
                #修飾語の時だけ。と条件にしたいので
                if two_dim.modify_check == "yes":
                    for_two_dim_list.append(two_dim.k_dep)
                    
                if not two_dim.modify_check == "yes":
                    for_two_dim_list.append("")
        
            #もし、リストなら
            if isinstance(two_dim,list):
                if not len(two_dim) == 0:
                    for three_dim in two_dim:
                       
                        for_three_dim_list.append(three_dim.k_dep)
                    
                    for_two_dim_list.append(for_three_dim_list)
            
        dep_info_list.append(for_two_dim_list)

    print "dependency information:",dep_info_list
    out = modi_list(out_list)
    return out

def modi_list(out_list):
    """
    修飾語と修飾語がかかる格をひとつのリストに格納する関数
    入力時には３次元配列になっていて、出力時には４次元配列になる
    [[単ノード形態素, , ,[[並列の修飾形態素, ],[並列の被修飾格, ]]]]
    一次元目：必ず配列（もし構文、なので構文の時に２つに分離）
    二次元目：単ノードであればインスタンス。修飾と被修飾関係があれば配列を持つ
    三次元目：修飾と被修飾の関係にある語のインスタンス。さらに並列構造があれば配列を持つ　
    四次元目：並列構造にある語のインスタンス。


    for文の中で次の４通りに分岐するようになっている
    １　修飾語が単ノード
    ２　修飾語が並列（配列構造）
    ３　格が単ノード
    ４　格は並列（配列構造）
    """
    exist_modi = "no"
    para_case = "no"
    out = []
    case_set_list = []

    for one_dim in out_list:
        for_two_dim_list = []

        for two_dim in one_dim:

            #修飾語も格も並列構造を含まない場合
            if not isinstance(two_dim,list):
                """
                修飾語　か　格が並列していない場合
                
                修飾語の場合：
                case_set_listに修飾語のインスタンスを追加
                修飾語マーカーをオンにする

                格の場合：
                下の記述を参照

                修飾語でも格でもない場合：
                二次元目にリストにインスタンスを追加

                """
                #two_dimが修飾語だった場合の処理
                if two_dim.modify_check == "yes" and two_dim.predicate_check == "yes" and not two_dim.case_check == "yes":
                    case_set_list.append(two_dim)
                    exist_modi = "yes"
                    continue

                if two_dim.case_check == "yes" and exist_modi == "yes" and not para_case == "yes":
                    """
                    two_dimが格で、かつ修飾語チェックがオンになっていた時
                    case_set_listを閉じて、for_two_dim_listに追加
                    case_set_listを初期化
                    exist_modiマーカーを初期化
                    """
                    case_set_list.append(two_dim)
                    for_two_dim_list.append(case_set_list)
                    case_set_list = []
                    exist_modi = "no"
                    continue


                else:
                    for_two_dim_list.append(two_dim)
                    continue
                    
            if isinstance(two_dim,list):
                """
                修飾語　か　かかり先の語が並列構造を持つ場合
                三次元目のリストを展開して得たインスタンスをfor_para_listに格納する
                
                並列しているのが修飾語の場合：
                修飾語があるというマーカーをオンにする
                修飾語　と　被修飾語の関係リストに並列修飾語を追加する
                ひとつうえのfor文に戻る

                並列しているのが格の場合：
                （すでに修飾語がcase_set_listに格納されている状態）
                case_set_listを閉じて、for_two_dim_listに追加
                修飾語があるというマーカーを初期化する
                """
                for_para_list = []
                
                for three_dim in two_dim:
                    """
                    三次元目の展開を行う
                    並列をしている語が修飾語だった場合 exist_modiマーカーをyesにする
                    並列をしている語が格だった場合、para_caseマーカーをyesにする

                    どちらの場合でもfor_para_listにインスタンスを追加する
                    （並列をしているのは、修飾語か格のどちらかに限る。という前提があるから）
                    """
                    #three_dimが修飾語だった場合（修飾語が並列だった場合）
                    if three_dim.modify_check == "yes" and three_dim.predicate_check == "yes":
                        exist_modi = "yes" 
                    #three_dimが格だった場合（かかり先の格が並列だった場合）
                    if three_dim.case_check == "yes" and exist_modi == "yes":
                        para_case = "yes"
                    #どちらの場合にせよ、並列構造リストにノードを追加
                    for_para_list.append(three_dim)

                #並列構造リストを修飾語句リストに格納
                if exist_modi == "yes" and not para_case == "yes":
                    case_set_list.append(for_para_list)
                    
                if para_case == "yes":
                    """
                    係り先の格が並列だった時
                    case_set_listを閉じて、for_two_dim_listに追加
                    case_set_listを初期化
                    exist_modiマーカーを初期化
                    """
                    case_set_list.append(for_para_list)
                    for_two_dim_list.append(case_set_list)
                    for_para_list = []
                    case_set_list = []
                    para_case = "no"


        out.append(for_two_dim_list)




    return out   
        

    
