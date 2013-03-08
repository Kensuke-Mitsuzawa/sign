# -*- coding:utf-8 -*-

__author__ = 'Kensuke Mitsuzawa'
__version__ = "2013/3/9"
__copyright__ = ""
__license__ = "GPL v3"


"""
開発途中の重要なコメントは
# __xx__

のすぐ直下
"""

frag = 1

import sys,codecs,subprocess,re,string
import negative,make_sentence,syori,struc_analyze,parallel,modifier,make_clause,demo,predicate_dic
from types import *
import commands

## 辞書の定義
info_dic = {"main":"none","Ga":"none","Wo":"none","Ni":"none","He":"none","To":"none","Kara":"none","Yori":"none","De":"none","Time":"none","Predict":"none","Modi":"none"}


def add_negative(set_dic,negative):
    predict_list = set_dic["Predict"]

    dep = 'n'
    per='n'
    pos='negative'
    cat='n'
    dom='n'
    case='n'
    case_ana='n'
    order='n'

    if negative == "willness":
        reg = "ない（意思）"
        morp = "ない（意思）"

    if negative == "posess":
        reg = "ない（両手）"
        morp = "ない（両手）"

    if negative == "perfect":
        reg = "ない（未完了）"
        morp = "ない（未完了）"

    if negative == "impossible":
        reg = "無理"
        morp = "無理"

    if negative == "experience":
        reg = "。。。"
        morp = "。。。"

    if negative == "need":
        reg = "不必要"
        morp = "不必要"

    negative_info = info(dep,per,reg,morp,pos,cat,dom,case,case_ana,order)
    predict_list.append(negative_info)

    set_dic["Predict"] = predict_list


    return set_dic

def clause_count(tmp_list):
## 節の数と各節が何行文の情報を持っているのか調べる関数

    ## clause_numは節の数,リストclauseは各節が何行の情報を持っているか。
    clause_num = 0
    clause = []
    c_num = -1

    # __xx__
    #print "-----------------------------"
    for tmp in tmp_list:
        if tmp == u"*":
            ## 前の節が何行分の情報を持っていたか。リストに追加する
            clause.append(c_num)

            ## c_numの数を初期化
            c_num = 1

            ## clause_numの数をひとつ増やす
            clause_num += 1

        ## 処理の都合上、最後の節はカウントできないので、無理やりだけど、こうする
        #ここは機種に大きく依存する可能性がある。re.findallに切り替えてもいいかもしれない
        #windows では "EOS\r\n" Linuxでは"EOS\n"
        elif tmp == u"EOS\n":
            ## EOSの前には。、？！の記号しかないと仮定して-1する
            c_num = c_num - 1
            clause.append(c_num)

        else:
            c_num += 1

    clause.pop(0)
    if frag == 1:
        print "Number of Clauses is",clause_num
        print "List of lines in each clause",clause

    return clause_num,clause


def knp_tab(sentence):

    tmp_list = []
    clause_list = []

    sentence = check_kuten(sentence)

    #windowsでは以下のsubprocessはコメントオフ

    echo = subprocess.Popen(['echo',sentence],
                            stdout=subprocess.PIPE,
                            )


    juman = subprocess.Popen(['juman'],
                             stdin=echo.stdout,
                             stdout=subprocess.PIPE,
                             )


    knp = subprocess.Popen(['knp','-case','-tab'],
                           stdin = juman.stdout,
                           stdout=subprocess.PIPE,
                           )

    """
    #以下、windows用のコード
    #windows用のjuman,knpの入力はcp932でないといけない
     __xx__
    str = sentence.encode('cp932')
    
    juman = subprocess.Popen(["juman"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    knp = subprocess.Popen(["knp", "-tab"], stdin=juman.stdout, stdout=subprocess.PIPE, shell=True)
    juman.stdin.write(str)
    juman.stdin.close()
    juman.stdout.close()
    """
    
    end_of_pipe_tab = knp.stdout

    for line in end_of_pipe_tab:
        #if windows, convertion from cp932 to unicode
        #if linux, conversion from 'utf-8'
        line = unicode(line,'utf-8')
        #check KNP analysis error
        error_check = check_knp_error(line)
        if error_check == u'error': 
            print 'error!'
            return '',''
        else: 
            line_split = line.split(" ")
            tmp_list.append(line_split[0])
            clause_list.append(line)
        


    #--------------------------------------
    #ここで各処理関数に情報を投げる
    clause_num, clause = clause_count(tmp_list)
    #returns 0 if not negation, returns 1 if negation
    negative_value = negative.find_negation(clause_list,clause_num,clause)

    if negative_value == 0:
        negative_choice = ""
    else:
        negative_choice = negative.negation(clause_list,clause_num,clause)

    #文の構文に関する情報。返ってくるのはハッシュマップ
    struc_dic = struc_analyze.structure_analyzer(clause_list,clause_num,clause)
    #文の情報を抽出。返ってくるのはリスト
    out_list = syori.Syori(clause_list,clause_num,clause,negative_choice,frag)
    #節が複数節なのか？単節なのか？を判断する。返ってくるのは二値。yes or no
    clause_check_result = make_clause.clause_check(out_list)

    #そもそもif分けする必要はどこにもないので、そのうち修正すること
    if clause_check_result == u"yes":
        out_list = make_clause.make_clause_set(out_list)
    #別に記述せんでもいいが、明文化しておけばわかりやすいじゃん
    if clause_check_result == u"no":
        out_list = make_clause.make_clause_set(out_list)
    if frag == 1:
        print u"*"*40
        print u"result of make clause:",out_list
        print u"*"*40
    out_list,orig_index_list = parallel.heiretsu(out_list,frag)

    if frag == 1:
        print u"*"*40
    out_list,orig_index_list = modifier.modi(out_list,orig_index_list,frag)

    if frag == 1:
        print u"*"*40
        print u"after make modifier list:",out_list
        print u"*"*40
        print u"structure information is:",struc_dic
        print u"*"*40

    #__xx__
    #demo.demo_test(out_list)

    p_a_dic = predicate_dic.make_p_a_dic(out_list,orig_index_list,frag)

    make_sentence.sentence(struc_dic,p_a_dic,out_list,frag)

    #__xx__
    #out_list = parallel.c_heiretsu(out_list,frag)


    if frag == 1:
        print "*"*40
        print u"Is clause multi or not?:",clause_check_result

    return out_list,struc_dic

def check_kuten(sent):
    if re.findall(ur'。',sent) == []:
        if re.findall(ur'？',sent) == [] or re.findall(ur'！',sent) == []:
            sent = sent + u'。'
            print u'--------------------------'
            print u'句点が自動挿入されました。'
            print u'--------------------------'
            return sent

        else:
            pass
    else:
        pass

def check_knp_error(line):
    if not re.findall(ur'ERROR:Cannot make mrph',line) == []: return u'error'
    else: return u'n'

if __name__ == '__main__':
    sentence = raw_input(u"input sentence\r\n")
    sentence = u"私は先生に怒られた"
    info_dic,struc_dic = knp_tab(sentence)
