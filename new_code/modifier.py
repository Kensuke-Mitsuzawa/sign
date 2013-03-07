#! /usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Kensuke Mitsuzawa'
__version__ = "2013/3/6"
__copyright__ = ""
__license__ = "GPL v3"

def modi(out_list,orig_index_list,frag):
    """
    方針
    並列構造リストの構築と同じ方針
    やるべきことは３つ
    修飾発生箇所リストの構築
    インデックスリストの並び替え
    インスタンスリストの並び替え
    """

    if frag == 1:
        print u"修飾処理前のout_list:",out_list

    modi_index_list = []
    for_one_dim_list = []

    clause_count = 0
    multi_clause = u"no"


    for one_dim in out_list:
        """
        係り先リストの構築
        もし、修飾語（とぼくが考える）の条件に引っかかったら、その語が係る先のインデックス番号をリストに追加する(for_one_dim_listに追加)
        """

        clause_count = clause_count + 1

        #------------------------------------------------------
        #二次元目の展開
        for two_dim in one_dim:
            """
            展開したリストが二次元配列（並列なし）か三次元配列（並列あり）かにより処理を分ける
            """

            #------------------------------------------------------
            #並列構造なしの時
            if not isinstance(two_dim,list):
                """
                三次元配列（並列構造なし）の場合

                以下に修飾語となる時のルールを記述していく
                """
                if two_dim.pos == u"副詞" and two_dim.modify_check == u"yes":
                    """
                    副詞かつ修飾語の場合の記述
                    非常に古典的なやり方だが、これで「もし」が引っかかるのを回避
                    """

                    if not two_dim.input_morp == u"もし":
                        for_one_dim_list.append(two_dim.k_dep)
                        continue

                if two_dim.modify_check == u"yes" and two_dim.predicate_check == u"yes" and (two_dim.pos == u"形容詞" or two_dim.pos == u"副詞") and not two_dim.case_check == u"yes":
                    """
                    一般的（？）な修飾語の特徴に対する処理
                    一般的にはmodify_checkとpredicate_checkがオンになり、かつその時は品詞が「形容詞」か「動詞」で、また格チェックはオフになるので、上のifになる
                    """
                    for_one_dim_list.append(two_dim.k_dep)
                    continue

                else:
                    for_one_dim_list.append(0)
                    continue
                #並列構造なしの時はここまで
                #------------------------------------------------------


            #------------------------------------------------------
            #並列構造ありのとき
            if isinstance(two_dim,list):
                """
                三次元構造の時（並列構造が存在するとき）
                三次元目のインスタンスを格納するようのリストを用意
                三次元目のリストを展開
                """
                for_two_dim_list = []
                #------------------------------------------------------
                #三次元目の展開を開始
                for three_dim in two_dim:
                    """
                    以下に修飾語となる時のルールを記述していく
                    """
                    if three_dim.pos == u"副詞" and three_dim.modify_check == u"yes":
                        """
                        副詞の時の条件
                        述語にかかる副詞で、modify_checkがyesでpredicate_checkがnoの時があったので、追加
                        case_set_listを閉じる条件はしたに記述
                        ここで問題が起きてる、本来閉じたいノードがcaseがnoなので、閉じれなく、次の条件に合うノードで閉じてしまう現象が発生
                        [もし、あした雨がたくさんふったら、遠足は延期になる。]
                        """
                        if not three_dim.input_morp == u"もし":
                            for_two_dim_list.append(three_dim.k_dep)
                            continue


                    if three_dim.modify_check == u"yes" and three_dim.predicate_check == u"yes" and (three_dim.pos == u"形容詞" or three_dim.pos == u"副詞") and not three_dim.case_check == u"yes":
                        for_two_dim_list.append(three_dim.k_dep)
                        continue

                    else:
                        for_two_dim_list.append(0)
                        continue
                #三次元目の展開、ここまで
                #------------------------------------------------------

            for_one_dim_list.append(for_two_dim_list)
            #並列構造ありの時、ここまで
            #------------------------------------------------------

        modi_index_list.append(for_one_dim_list)
        for_one_dim_list = []
        #二次元目の展開終了
        #------------------------------------------------------

    #一次元目の展開終了（一番上のforの終了）
    #------------------------------------------------------

    #__xx__
    #print clause_count
    if clause_count > 1:
        """
        もし、節が２つの構造だったら、後で別の処理をさせたい。
        だからチェックを入れておく
        """
        multi_clause = u"yes"

    if multi_clause == u"no":
        out_list,orig_index_list = make_modi_set(out_list,orig_index_list,modi_index_list,frag)
    else:
        out_list,orig_index_list = multi_modi_set(out_list,orig_index_list,modi_index_list,frag)

    return out_list,orig_index_list

def multi_modi_set(out_list,orig_index_list,modi_index_list,frag):
    """
    ちょっと特殊な時に該当
    if文とか、（原因ー結果）文とか節が２つの構造になってしまう時はちょっと処理を変えないといけないので、この関数を呼び出す
    やっていることは基本的に一緒

    まだやっていないこと
    １　initial_modi_checkがnoの時の記述
    ２　節の中に並列が存在している場合（つまりさらにリストが内側に存在する場合）の記述
    """

    if frag == 1:
        print u"係り受け先リストは:",modi_index_list

    modi_set_list_orig = []
    modi_set_list = []
    initial_modi_check = u"yes"

    #------------------------------------------------------
    #一次元目の展開
    for one_dim_i in range(len(modi_index_list)):
        #------------------------------------------------------
        #二次元目の展開
        for two_dim_i in range(len(modi_index_list[one_dim_i])):
            if not modi_index_list[one_dim_i][two_dim_i] == 0:

                now_index = two_dim_i
                next_dep_number = modi_index_list[one_dim_i][two_dim_i+1]

                #------------------------------------------------------
                #initial_modi_checkがno,つまり連続修飾語の中間
                if initial_modi_check == u"no":
                    """
                    まだ面倒で中身を記述していない
                    """



                    continue
                #initial_modi_check=noのときはここまで
                #------------------------------------------------------


                #------------------------------------------------------
                #修飾語句の固まりの最初のとき
                if initial_modi_check == u"yes":

                    initial_modi_check = u"no"

                    initial_modi_i = two_dim_i

                    for orig_one_dim_i in range(len(orig_index_list)):
                        try:
                            orig_index = orig_index_list[orig_one_dim_i].index(modi_index_list[one_dim_i][two_dim_i])
                            modi_set_list_orig.append(orig_index_list[one_dim_i][two_dim_i])
                            modi_set_list_orig.append(orig_index_list[orig_one_dim_i][orig_index])

                            modi_set_list_orig.reverse()
                            #__xx__
                            #print modi_set_list_orig

                            modi_set_list.append(out_list[one_dim_i][two_dim_i])
                            modi_set_list.append(out_list[orig_one_dim_i][orig_index])

                            modi_set_list.reverse()
                            #__xx__
                            #print modi_set_list

                        except ValueError:
                            continue

                    #ここでは意図的にifのcontinueを記述しない
                #initial_modi_checkがyesのときはここまで
                #------------------------------------------------------

                #------------------------------------------------------
                #終了条件,次に係り受けをもっていない（つまり、修飾語句固まりの最終）
                if next_dep_number == 0:

                    initial_modi_check = u"yes"

                    orig_index_list[one_dim_i][initial_modi_i] = modi_set_list_orig
                    out_list[one_dim_i][initial_modi_i] = modi_set_list

                    for delete_num in modi_set_list_orig:
                        try:
                            orig_index_list[one_dim_i].remove(delete_num)
                        except ValueError:
                            continue

                    for delete_ins in modi_set_list:
                        try:
                            out_list[one_dim_i].remove(delete_ins)
                        except ValueError:
                            continue
                #終了条件の最後
                #------------------------------------------------------

        #二次元目の展開ここまで
        #------------------------------------------------------
    #一次元目展開ここまで
    #------------------------------------------------------

    return out_list,orig_index_list

def paralist_error(dep_in_paralist_error,dep_num_paralist_error,initial_modi_i,orig_index_list,out_list,modi_set_list_orig,modi_set_list,para_list_orig,para_list,dep_ins_paralist_error):
    """
    修飾語が単ノードで被修飾語が並列リストに格納されている場合の記述
    例: [私　素敵な [ハワイ　グアム]　行った]

    この時、initial_modi_checkはnoになっている.なぜなら,すでに修飾語がある前提だから
    """
    dep_in_paralist_error = u"no"

    #print "paralistエラーを起こしたときの係り先番号:",dep_num_paralist_error
    for orig_two_dim in orig_index_list:
        for orig_three_dim in orig_two_dim:
            if isinstance(orig_three_dim,list):
                try:
                    orig_index = orig_three_dim.index(dep_num_paralist_error)
                    para_list_orig.append(orig_three_dim[orig_index])

                except ValueError:
                    continue


    for out_two_dim in out_list:
        for out_three_dim in out_two_dim:
            if isinstance(out_three_dim,list):
                try:
                    out_index = out_three_dim.index(dep_ins_paralist_error)
                    para_list.append(out_three_dim[out_index])

                except ValueError:
                    continue

    modi_set_list_orig.append(para_list_orig)
    modi_set_list.append(para_list)
    modi_set_list_orig.reverse()
    modi_set_list.reverse()

    for orig_two_dim in orig_index_list:
        orig_two_dim[initial_modi_i] = modi_set_list_orig

        for para_list in modi_set_list_orig:
            for delete_num in para_list:
                if delete_num in orig_two_dim:
                    orig_two_dim.remove(delete_num)
                for orig_three_dim in orig_two_dim:
                    if isinstance(orig_three_dim,list) and not orig_three_dim == modi_set_list_orig:
                        try:
                            orig_three_dim.remove(delete_num)
                        except ValueError:
                            continue

    for out_two_dim in out_list:
        out_two_dim[initial_modi_i] = modi_set_list

        for para in modi_set_list:
            for delete_ins in para:
                if delete_ins in out_two_dim:
                    out_two_dim.remove(delete_ins)
                for out_three_dim in out_two_dim:
                    if isinstance(out_three_dim,list) and not out_three_dim == modi_set_list:
                        try:
                            out_three_dim.remove(delete_ins)
                        except ValueError:
                            continue

        for orig_two_dim in orig_index_list:
            try:
                orig_two_dim.remove([])
            except ValueError:
                pass

        for out_two_dim in out_list:
            try:
                out_two_dim.remove([])
            except ValueError:
                pass

    #print "処理の結果のmodi_setlist:",modi_set_list_orig
    #print "処理の結果のmodi_set:",modi_set_list
    #print "現在のorig_index_list:",orig_index_list
    #print "現在のout_list:",out_list


    return dep_in_paralist_error,modi_set_list_orig,orig_index_list,out_list



def make_modi_set(out_list,orig_index_list,modi_index_list,frag):
    if frag == 1:
        print u"修飾係り受け先リスト:",modi_index_list
        print u"現在のindexリスト:",orig_index_list
        print u"現在のインスタンスリスト:",out_list


    #------------------------------------------------------
    #一次元目の展開を開始
    for one_dim in modi_index_list:
        """
        修飾構造のリストを作成する:modi_set_list
        手順:
        まず、modi_index_listをチェックする（二次元目まで展開）
        ０以外の要素があればif文で分岐
        modi_index_listで見つかった０以外の要素は,並列の係り先のindex番号.このindex番号をorig_index_listから検索する.検索によって見つかった番号を返す.modi_index_list内で0以外の数字をもつmodi_index_listのindex番号と返された番号をmodi_set_listに追加

        二次元目を展開して見つからなかったら三次元目を展開して探す.（三次元目に係り先番号が存在するとき＝並列構造のとき）だから、特別な処理が必要

        １　上のmodi_set_listとは別のリストを新規作成（modi_set_in_para）
        ２　modi_set_in_paraへの追加がすべて完了したら、modi_set_in_paraを展開途中の三次元目にリストに入れる（appendでなく置換.置換する場所は元々の係り先句の番号）


        並列のときと同じくチェック方式を多用するのが有効かも　
        """
        initial_modi_check = u"yes"
        dep_in_paralist_error = u"no"
        first_check = u'no'

        #------------------------------------------------------
        #二次元目の展開を開始
        for two_dim in one_dim:
            """
            現状のコードだと、色んな問題が出てる
            例えば、係り先リストが[[0, 2, [0, 0], 4, 0]]でインデックスリストが[0, 1, [2, 4], 3, 5]の時、いまのコードだと.indexメソッドがエラーを出す。tryを使って回避したが、このときの処理を記述する必要がある
            """
            #------------------------------------------------------
            #並列構造なしのif
            if not isinstance(two_dim,list):
                if not two_dim == 0:
                    """
                    two_dimがインスタンス（つまり並列構造が存在しないとき）
                    """
                    #修飾語が連続する場合のために次の語が係り元かどうかチェックする。次が０なら、係りもとはない
                    now_index = one_dim.index(two_dim)
                    next_dep_number = one_dim[now_index+1]

                    if initial_modi_check == u"yes":
                        """
                        修飾語の最初の部分
                        """
                        modi_set_list = []
                        modi_set_list_orig = []

                        initial_modi_check = u"no"
                        #__xx__
                        first_check = u'yes'
                        index_in_modi_index_list = one_dim.index(two_dim)

                        initial_modi_i = one_dim.index(two_dim)
                        #orig_index_listから当該番号を検索
                        for orig_two_dim in orig_index_list:

                            try:
                                orig_index = orig_two_dim.index(two_dim)
                                modi_set_list_orig.append(orig_two_dim[index_in_modi_index_list])
                                modi_set_list_orig.append(orig_two_dim[orig_index])

                                modi_set_list_orig.reverse()

                                for out_list_two_dim in out_list:
                                    modi_set_list.append(out_list_two_dim[index_in_modi_index_list])
                                    modi_set_list.append(out_list_two_dim[orig_index])
                                    modi_set_list.reverse()

                                #__xx__
                                #print u"現在の修飾リスト:",modi_set_list_orig
                            except ValueError:
                                print u"係り先リストが[[0, 2, [0, 0], 4, 0]]でインデックスリストが[0, 1, [2, 4], 3, 5]のタイプのエラーが発生している"

                                #ここら辺の処理をまとめて関数に移してもいいような気がするんだが...
                                dep_in_paralist_error = "yes"
                                dep_num_paralist_error = two_dim

                                for out_two_dim in out_list:
                                    for out_three_dim in out_two_dim:

                                        try:
                                            if out_three_dim.k_position == dep_num_paralist_error:
                                                dep_ins_paralist_error = out_three_dim

                                        except AttributeError:
                                            if isinstance(out_three_dim,list):
                                                for out_four_dim in out_three_dim:
                                                    if out_four_dim.k_position == dep_num_paralist_error:
                                                        dep_ins_paralist_error = out_four_dim

                                para_list = []
                                para_list_orig = []
                                for orig_two_dim in orig_index_list:
                                    para_list_orig.append(orig_two_dim[index_in_modi_index_list])

                                for out_two_dim in out_list:
                                    para_list.append(out_two_dim[index_in_modi_index_list])

                                dep_in_paralist_error,modi_set_list_orig,orig_index_list,out_list = paralist_error(dep_in_paralist_error,dep_num_paralist_error,initial_modi_i,orig_index_list,out_list,modi_set_list_orig,modi_set_list,para_list_orig,para_list,dep_ins_paralist_error)


                    if initial_modi_check == u"no" and first_check == u'no':
                        """
                        次の語も係りを持っている場合
                        修飾語（←対象）　修飾語　格
                        のようなケース
                        """

                        index_in_modi_index_list = one_dim.index(two_dim)

                        if dep_in_paralist_error == u"no":
                            for orig_two_dim in orig_index_list:

                                try:
                                    orig_index = orig_two_dim.index(two_dim)
                                    modi_set_list_orig.append(orig_two_dim[orig_index])
                                    
                                    #__xx__
                                    #print u"現在の修飾リスト:",modi_set_list_orig

                                    for out_list_two_dim in out_list:
                                        modi_set_list.append(out_list[orig_index])

                                except ValueError:
                                    dep_in_paralist_error = u"yes"
                                    dep_num_paralist_error = two_dim

                                    para_list = []
                                    para_list_orig = []

                                    for out_two_dim in out_list:
                                        for out_three_dim in out_two_dim:
                                            if isinstance(out_three_dim,list):
                                                for out_four_dim in out_three_dim:
                                                    try:
                                                        if out_four_dim.k_position == dep_num_paralist_error:
                                                            dep_ins_paralist_error = out_four_dim

                                                    except AttributeError:
                                                        continue

                                    for orig_two_dim in orig_index_list:
                                        para_list_orig.append(orig_two_dim[index_in_modi_index_list])
                                    for out_two_list in out_list:
                                        para_list.append(out_two_dim[index_in_modi_index_list])

                                    dep_in_paralist_error,modi_set_list_orig,orig_index_list,out_list = paralist_error(dep_in_paralist_error,dep_num_paralist_error,initial_modi_i,orig_index_list,out_list,modi_set_list_orig,modi_set_list,para_list_orig,para_list,dep_ins_paralist_error)


                    if initial_modi_check == u"no" and int(next_dep_number) == 0 and dep_in_paralist_error == u"no":

                        """
                        修飾語連続の末尾の時に以下が実行される
                        next_dep_number（係り受け先リストで今の次の要素）が0なら、今の句が、修飾語連続の末尾と判断できる
                        """
                        initial_modi_check = u"yes"

                        for orig_two_dim in orig_index_list:
                            orig_two_dim[initial_modi_i] = modi_set_list_orig
                            for delete_number in modi_set_list_orig:
                                if delete_number in orig_two_dim:
                                    orig_two_dim.remove(delete_number)


                        for out_list_two_dim in out_list:
                            out_list_two_dim[initial_modi_i] = modi_set_list
                            for delete_ins in modi_set_list:
                                if delete_ins in out_list_two_dim:
                                    out_list_two_dim.remove(delete_ins)


            #並列構造なしのifここまで
            #------------------------------------------------------


            #------------------------------------------------------
            #並列構造が存在する場合
            if isinstance(two_dim,list):
                """
                やるべきことは以下のとおり

                係り先リストで、並列リストの展開
                展開したインデックス番号をorig_listから探す
                探し方には二通りある、なので、以下の２つの場合に処理を記述する
                １　並列リスト内にインデックス番号がある
                ２　並列リストの外（一個、上の次元のリストにある）

                １　並列リスト内で見つかったとき
                [係りもと　係り先]　だから、このままでいいのでは？
                例：　私は大きくて可愛いねこが好きだ

                ２　並列リスト外で見つかった場合
                [[係りもと　並列インスタンス]　その他　係り先]
                をこうする必要がある
                [[係りもと　並列インスタンス　係り先]　その他]
                """
                for three_dim in two_dim:
                    if not three_dim == 0:

                        if initial_modi_check == u"yes":
                            modi_set_list = []
                            modi_set_list_orig = []

                            initial_modi_check = u"no"

                            index_in_modi_index_list = two_dim.index(three_dim)

                            #これは一次元リスト中の二次元リストの位置を記録しておく
                            initial_modi_i = one_dim.index(two_dim)

                            for orig_two_dim in orig_index_list:
                                    #係り先番号を並列構造リストの中を検索
                                    for orig_three_dim in orig_two_dim:

                                        if isinstance(orig_three_dim,list):
                                            try:
                                                orig_index = orig_three_dim.index(three_dim)

                                                modi_set_list_orig.append(orig_three_dim[index_in_modi_index_list])
                                                modi_set_list_orig.append(orig_three_dim[orig_index])

                                            except ValueError:
                                                print u"three_dimの要素がリストにないってよ！"

                            for out_list_two_dim in out_list:
                                for out_three_dim in out_list_two_dim:

                                    if isinstance(out_three_dim,list):
                                        modi_set_list.append(out_three_dim[index_in_modi_index_list])
                                        modi_set_list.append(out_three_dim[orig_index])


                                    #ここから、係り先が三次元リストの外で見つかった場合について記述（めんどうで未記述 2/18）
                            continue


                        if initial_modi_check == u"no":
                            """
                            私は大きくて可愛いネコが好きだ。の例だと、[私 [大きい　可愛い]ネコ　好き]になる
                            大きい→可愛い　の修飾をチェックしてinitial_modi_checkがnoに変化する
                            なので、次に可愛い→ネコの対する処理が必要

                            今は[修飾語　修飾語]　格　に対する処理
                            もし、[修飾語　修飾語　修飾語]格　だったらどうすんのさ？まだ、考えてない
                            """
                            initial_modi_check = u"yes"

                            for orig_two_dim in orig_index_list:

                                try:
                                    orig_index = orig_two_dim.index(three_dim)

                                    modi_set_list_orig.append(orig_two_dim[orig_index])

                                except ValueError:
                                    print u"three_dimは見つからなかったってよ！"

                                orig_two_dim[initial_modi_i] = modi_set_list_orig
                                for delete_number in modi_set_list_orig:
                                    if delete_number in orig_two_dim:
                                        orig_two_dim.remove(delete_number)

                            for out_list_two_dim in out_list:
                                modi_set_list.append(out_list_two_dim[orig_index])

                                out_list_two_dim[initial_modi_i] = modi_set_list
                                for delete_ins in modi_set_list:
                                    if delete_ins in out_list_two_dim:
                                        out_list_two_dim.remove(delete_ins)





            #並列構造ありのifここまで
            #------------------------------------------------------

        #二次元目の展開終了
        #------------------------------------------------------
    #最初のforはここまで
    #------------------------------------------------------
    if frag == 1:
        print u"修飾処理すべて完了後のインデックスリスト:",orig_index_list
        print u"修飾処理すべて完了後のout_list:",out_list


    return out_list,orig_index_list




def modi_(out_list):
    """
    以下、旧コード。
    欠陥が見つかったので、使用中止。


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
    out_list,orig_index_list = modi_list(out_list)
    return out_list,orig_index_list

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
    exist_modi = u"no"
    exist_adv = u"no"
    para_case = u"no"
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

                #------------------------------
                #動作確認用
                print u"now morp is",two_dim.input_morp
                print u"now pos is",two_dim.pos
                print "------------"
                #------------------------------


                if two_dim.pos == u"副詞" and two_dim.modify_check == u"yes":
                    """
                    副詞の時の条件
                    述語にかかる副詞で、modify_checkがyesでpredicate_checkがnoの時があったので、追加
                    case_set_listを閉じる条件はしたに記述
                    ここで問題が起きてる、本来閉じたいノードがcaseがnoなので、閉じれなく、次の条件に合うノードで閉じてしまう現象が発生
                    [もし、あした雨がたくさんふったら、遠足は延期になる。]

                    """
                    if not two_dim.input_morp == u"もし":
                        case_set_list.append(two_dim)
                        exist_adv = u"yes"
                        continue

                if two_dim.pos == u"動詞" and two_dim.predicate_check == u"yes" and exist_adv == u"yes":
                    case_set_list.append(two_dim)
                    for_two_dim_list.append(case_set_list)
                    case_set_list = []
                    exist_adv = u"no"
                    continue



                if two_dim.modify_check == u"yes" and two_dim.predicate_check == u"yes" and (two_dim.pos == u"形容詞" or two_dim.pos == u"副詞") and not two_dim.case_check == u"yes":
                    case_set_list.append(two_dim)
                    exist_modi = u"yes"
                    continue

                if two_dim.case_check == u"yes" and (exist_modi == u"yes" or exist_adv == u"yes") and not para_case == u"yes":
                    """
                    two_dimが格で、かつ修飾語チェックがオンになっていた時
                    case_set_listを閉じて、for_two_dim_listに追加
                    case_set_listを初期化
                    exist_modiマーカーを初期化
                    """
                    case_set_list.append(two_dim)
                    for_two_dim_list.append(case_set_list)
                    case_set_list = []
                    exist_modi = u"no"
                    exist_adv = u"no"
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
                    #------------------------------
                    #動作確認用
                    print u"input morp",three_dim.input_morp
                    print u"pos is",three_dim.pos
                    print "-------------"
                    #------------------------------
                    if three_dim.pos == u"副詞" and three_dim.modify_check == u"yes":
                        case_set_list.append(three_dim)
                        exist_adv = u"yes"
                        continue

                    #three_dimが修飾語だった場合（修飾語が並列だった場合）
                    if three_dim.modify_check == u"yes" and three_dim.predicate_check == u"yes" and (three_dim.pos == u"形容詞" or three_dim.pos == u"副詞") :
                        exist_modi = u"yes"
                    #three_dimが格だった場合（かかり先の格が並列だった場合）
                    if three_dim.case_check == u"yes" and exist_modi == u"yes":
                        para_case = u"yes"
                    #どちらの場合にせよ、並列構造リストにノードを追加
                    for_para_list.append(three_dim)

                #並列構造リストを修飾語句リストに格納
                if exist_modi == u"yes" and not para_case == u"yes":
                    case_set_list.append(for_para_list)

                if para_case == u"yes":
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
                    para_case = u"no"

                else:
                    for_two_dim_list.append(for_para_list)
                    for_para_list = []


        out.append(for_two_dim_list)




    return out



