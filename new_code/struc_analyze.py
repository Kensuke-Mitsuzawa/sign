#! /usr/bin/python
# -*- coding:utf-8 -*-

import re

def structure_analyzer(clause_list,clause_num,clause):
    
    struc_dic = {'nor':[],'ques':[],'passive':[],'cause':[],'if':[],'force':[]}
    struc_dic['nor'] = "yes"

    #カウンターの設置
    counter = 0

    #語の並び情報(order)
    order = 0
    
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
            
            
            #--------------------------------------
            #構文情報を拾う
            #基本句単位で構文情報を拾うことが多い
            
            #〜なので、〜だから、理由を表す節の場合
            if not re.findall(r"\+.*D",sentence) == []:
                #他に述語に関する条件も含めようか、検討中
                if not re.findall(r"<節機能-理由>",sentence) == [] and not re.findall(r"<連用節>",sentence) == []:
                    struc_dic["cause"] = "yes"

            #〜もし、ifを表す構文の場合
            if not re.findall(r"\+.*D",sentence) == []:
                #同じく <条件節候補>　もありえるのだが、常にこの要素が出るのか不明
                #この条件だと、条件部分が節になっていないと対応できない。
                #つまり、”もしAが真なら、Bは偽だ”のような文には対応できなくて困る
                #いっそのこと　”もし”　があれば、条件にしてもいいような気もする
                if not re.findall(r"<節機能-条件>",sentence) == []:
                    struc_dic["if"] = "yes"
            
            #疑問文のとき（個人的には疑問文は？マークで判断してもよいとは思う
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<モダリティ-疑問>",sentence) == []:
                    struc_dic[nor] = []
                    struc_dic[ques] = "yes"

            #受け身のとき
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<態:受動>",sentence) == []:
                    struc_dic[nor] = []
                    struc_dic[passive] = "yes"

            #使役文のとき
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<態:使役>",sentence) == []:
                    struc_dic[nor] = []
                    struc_dic[force] = "yes"

    return struc_dic
