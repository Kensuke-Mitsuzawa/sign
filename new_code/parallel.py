#! /usr/bin/python
# -*- coding:utf-8 -*-

def check_clause(out_list):
    """
    out_listをいったん調査してみて、節機能があるか調べる
    節機能があれば、Trueを返す
    なければFalseを返す
    """
    clause_func = ""
    
    for one_dim_i in range(len(out_list)):
        for two_dim_i in range(len(out_list[one_dim_i])):
            """
            もしあした雨が降ったら、あしたの遠足は延期です。
            の例文の時にはpara_checkは入らない。その代わりにclause_funcの項目が何かしろの機能が表示される。
            なので、これをマーカーにする。
            """
            try:
                if not(out_list[one_dim_i][two_dim_i]).clause_func == "":
                    clause_func =  (out_list[one_dim_i][two_dim_i]).clause_func
            except AttributeError:
                continue

    if not clause_func == "":
        return "T"

    else:
        return "F"

def clause_func(out_list):
    """
    check_clauseで節機能が検知された場合のみに実行される。
    Input:out_list
    Output:節機能にあったNMSをつけたout_list
    """
    for one_dim_i in range(len(out_list)):
        for two_dim_i in range(len(out_list[one_dim_i])):
            """
            もしあした雨が降ったら、あしたの遠足は延期です。
            の例文の時にはpara_checkは入らない。その代わりにclause_funcの項目が何かしろの機能が表示される。
            なので、これをマーカーにする。
            """
            clause_func = ""

            try:
                clause_func =  (out_list[one_dim_i][two_dim_i]).clause_func
            except AttributeError:
                continue
            #------------------------------------------------------
            #節機能が見つかったインスタンスのみif以下の処理    
            if not clause_func == "":
                """
                以下、NMSをルールで記述する

                """
                print clause_func 

                if clause_func == "条件":
                    #記号を忘れたので、とりあえず条件とか書いておく
                    out_list[one_dim_i][two_dim_i].nms == "条件"

                if clause_func == "理由":
                    out_list[one_dim_i][two_dim_i].nms == "理由"

            #節機能が見つかったときの処理はここまで
            #------------------------------------------------------
            


def c_heiretsu(out_list):
    """
    次やるべきこと:二次元目にリストがある場合の記述

    """
    c_para_flag = "no"
    c_para_check = "no"
    out = []
    c_para_list = []
    tmp_para_list = []
    
    const = 0

    check_result = check_clause(out_list)

    print check_result
    if check_result == "T":
        clause_func(out_list)

    if check_result == "F":
        pass
    
                



def __c_heiretsu__():
    """
    ルールを書いた意味がよくわからなくなったので、別の関数として保存しておく
    処理を書いてたときに頭にウジでもわいていたのではないだろうか（本人談）

    """
        
    if not isinstance(one_dim[-1],list):
        """
        二次元目にインスタンスがある場合　かつ
        二次元目の最後はリストでない場合（つまりインスタンスの場合）
        
        
        最後のインスタンスを確認して、並列　かつ　並列基本句数０のとき（この時、節の並列と思われる）のときに限り、リストを展開
        次の節のために、c_para_checkをyesにする
        また、関数の返り値の制御のためにc_para_flagもyesにする
        
        次の節はc_para_checkがイエスの時に限り、節並列リストに加える操作をする
        """
        if (one_dim[-1]).para_check == "yes" and (one_dim[-1]).p_p_num == "":
            """
            節接続のNMSを入れるのなら、この-1のインスタンスを見て判断
            """
            
            for two_dim in one_dim:
                tmp_para_list.append(two_dim)
                c_para_check = "yes"
                c_para_list.append(tmp_para_list)
                tmp_para_list = []
                c_para_flag = "yes"
                continue
                
            if c_para_check == "yes":
                    
                for two_dim in one_dim:
                    tmp_para_list.append(two_dim)
                c_para_list.append(tmp_para_list)
                tmp_para_list = []
                out.append(c_para_list)
                c_para_list = []
                c_para_check = "no"

                #ほんとはここにcontinueがあったけど、整理中に消してしまいました
    if isinstance(one_dim[-1],list):
        """
        二次元目の最後がインスタンスでない場合
        ex.述語が並列になっている（並列リスト）
        
        基本的にやっていることは二次元の時と同じ
        """
        for two_dim in one_dim:
            if isinstance(two_dim,list):
                if (two_dim[-1]).para_check == "yes" and (two_dim[-1]).p_p_num == "":
                    """
                    節接続のNMSを入れるのなら、この-1のインスタンスを見て判断
                    """
                    for three_dim in two_dim:
                        tmp_para_list.append(three_dim)
                    c_para_check == "yes"
                    c_para_list.append(tmp_para_list)
                    tmp_para_list = []
                    c_para_flag = "yes"
                continue
                



    if c_para_flag == "yes":
        print "result of clause parallel",out
        return out

    if c_para_flag == "no":
        print "same as input(no clause parallel)",out_list
        return out_list

       

def heiretsu(out_list):

    print "並列処理前のout_list:",out_list

    para_index_list = []

    #------------------------------------------------------
    #並列係り先リストの作成ここから（別の関数に移してもいい）
    for one_dim in out_list:
        """
        並列の係り先番号を保存するリストを作成する
        並列があれば、その係り先番号を保存
        並列がなければ、０を代入しておく。
        このリストはout_listと同じ形式にしたいので二次元リスト

        para_index_listがこのリスト
        """
        for_one_dim_list = []
        #------------------------------------------------------

        for two_dim in one_dim:
            if two_dim.para_check == "yes" and not two_dim.p_p_num == "":
                for_one_dim_list.append(two_dim.k_dep)

            else:
                for_one_dim_list.append(0)

        para_index_list.append(for_one_dim_list)
    #並列係り先リストの構築ここまで
    #------------------------------------------------------
    print "並列句係り先番号リスト:",para_index_list

    #------------------------------------------------------
    #元のインデックス番号を要素とするリストの作成ここから（別の関数に移していい）
    orig_index_list = []
    for one_dim in out_list:
        """
        orig_index_listの作成
        out_listの要素を移動すると、index番号が変化してしまうので、元のindex番号を保存しておかなくてはいけない
        このために元のindex番号をorig_index_listに保存しておく
        このリストはout_listと同じ形式にしたいので二次元リスト

        """

        for_one_dim_list = []
        for two_dim in one_dim:
            for_one_dim_list.append(two_dim.k_position)
        orig_index_list.append(for_one_dim_list)

    #インデックス番号を要素とするリストの作成ここまで
    #------------------------------------------------------
    print "オリジナルのindexリスト:",orig_index_list

    

    max_para = 0
    initial_para_check = "yes"

    #------------------------------------------------------
    #ここから本処理開始
    for one_dim in para_index_list:
        """
        並列構造のリストを作成する:para_list
        手順:
        まず、para_index_listをチェックする（二次元目まで展開）,０以外の要素があればif文で分岐
        para_index_listで見つかった０以外の要素は,並列の係り先のindex番号.このindex番号をorig_index_listから検索する.検索によって今,何番目にこのindexがあるのか？がわかる。

        """
        #------------------------------------------------------
        #二次元目の展開開始
        for two_dim in one_dim:
            if not two_dim == 0:
                """
                index_in_para_index_list:para_index_list中でのnot0の要素のindex番号
                orig_index:orig_index_listでのnot0の要素のindex番号
                
                構築した並列リストはKNPが指示した並列句数に達するまで置換をしない。
                この処理のために,三種類のタイプに場合わけをする
                initial_para_checkがyesの場合（並列の始まりの句）:

                並列リストを初期化
                initial_para_checkをnoにしておく
                最大並列句数を設定する
                並列句数カウンタを設定する（数の都合上２からスタート）
                並列リストに句を追加する
                並列句数カウンタを＋１
                
                並列句数が最大並列句数に達してない　かつ　initial_para_checkがnoの場合（並列の中間の句　もしくは　並列の最終句）:
                並列リストに句を追加
                並列句数カウンタを＋１

                並列句数カウンタが最大並列句数と同数になった（並列が終わったあと）:
                元のリストをinitial_para_i情報を使って、並列リストに置換
                並列リストに含まれる要素を、元のリストから削除
                initial_para_checkをyesに戻す
                """
                index_num = two_dim

                #------------------------------------------------------
                #initial_para_checkがyesのときここから
                if initial_para_check == "yes":
                    """
                    行う操作
                    １並列リストの構築
                    """

                    #並列数基本句数を考慮に入れる
                    for one_dim_out in out_list:
                        max_para = int(one_dim_out[one_dim.index(two_dim)].p_p_num)

                        
                    print max_para
                    para_count = 2
                    #最初の並列句のindex番号を保存しておく。（置換するときに必要）
                    initial_para_i = one_dim.index(two_dim)
                    
                    para_list = []
                    para_list_for_orig = []
                    

                    initial_para_check = "no"

                    index_in_para_index_list = one_dim.index(index_num)
                    
                    for orig_two_dim in orig_index_list:

                        orig_index = orig_two_dim.index(index_num)
                        para_list_for_orig.append(orig_two_dim[index_in_para_index_list])
                        para_list_for_orig.append(orig_two_dim[orig_index])

                        print "現在の並列リスト:",para_list_for_orig

                    for out_list_two_dim in out_list:

                        para_list.append(out_list_two_dim[index_in_para_index_list])
                        para_list.append(out_list_two_dim[orig_index])
                        
                        print "現在の並列リスト:",para_list                        

                    para_count = para_count + 1
                    #最後は意図的にcontinueを記述していない
                #initial_para_checkがyesのときここまで
                #------------------------------------------------------

                #------------------------------------------------------
                #まだ、最大並列句数に達していないとき（並列句の中間のとき）ここから
                if para_count < max_para and initial_para_check == "no":
                    """
                    行う操作
                    １並列リストの構築
                    """

                    index_in_para_index_list = one_dim.index(index_num)
                    
                    for orig_two_dim in orig_index_list:

                        orig_index = orig_two_dim.index(index_num)
                        para_list_for_orig.append(orig_two_dim[orig_index])

                        print "現在の並列リスト:",para_list_for_orig

                    for out_list_two_dim in out_list:
                        para_list.append(out_list_two_dim[orig_index])
                        
                        print "現在の並列リスト:",para_list  
                    

                    para_count = para_count + 1
                    print para_count
                    #このcontinueは必要
                    continue
                #最大並列句に達していないときここまで
                #------------------------------------------------------


                #------------------------------------------------------
                #終了条件ここから
                if para_count >= max_para:
                    """
                    行う操作
                    ２並列リストをオリジナルのリストに追加（実際は置換操作）
                    ３だぶってる番号をオリジナルリストから削除
                    NMSを挿入するならここで入れるのが妥当
                    """

                    initial_para_check = "yes"
                    
                    for orig_two_dim in orig_index_list:
                        orig_two_dim[initial_para_i] = para_list_for_orig
                        for delete_number in para_list_for_orig:
                            if delete_number in orig_two_dim:
                                orig_two_dim.remove(delete_number)

                    print "並列処理すべて完了後の並列リスト:",orig_index_list

                    #------------------------------------------------------
                    #NMSタグの記述を行う
                    #ただし、最後の句だけはNを入れない
                    for one_para_ins in para_list:
                        one_para_ins.nms == "N"
                    para_list[-1].nms == ""
                     #------------------------------------------------------


                    for out_list_two_dim in out_list:
                        out_list_two_dim[initial_para_i] = para_list

                        for delete_instance in para_list:
                            if delete_instance in out_list_two_dim:
                                out_list_two_dim.remove(delete_instance)

                #終了条件ここまで
                #------------------------------------------------------
                    print "並列処理すべて完了後の並列リスト:",out_list

        #二次元目の展開ここまで
        #------------------------------------------------------
    #三次元目の展開ここまで
    #------------------------------------------------------

    return out_list,orig_index_list

def _heiretsu_(out_list):
    """
    旧バージョンの関数
    致命的な欠陥を見つかったので使用中止
    ex.「私はきれなグアムと素敵なハワイに行った。」
    が以下のようになってしまう
    [私　きれい[グアム　素敵]ハワイ　行った]

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
                
                """
                並列の間にはうなずきのNを挿入
                """
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
