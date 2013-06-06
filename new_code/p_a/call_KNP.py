#! /usr/bin/python
# -*-coding:utf-8 -*-

"""
このスクリプトの説明
KNPの解析結果をパーズしてくれるスクリプトsyori.pyへの橋渡しの役割をする．
このスクリプト内で最初に呼び出すべき関数はcall.
"""


__author__ = 'Kensuke Mitsuzawa'
__version__ = "2013/3/24"
__copyright__ = ""
__license__ = "GPL v3"


import sys,codecs,subprocess,re,string
import syori
from types import *
import commands

def check_kuten(sent):
    """
    このスクリプトの説明：入力する日本語文の末尾に句点，もしくは疑問符，感嘆符がないと，解析結果がおかしくなる．なので，末尾にいずれもついてない場合に，強制的に句点を挿入する．
    """
    if re.findall(ur'。',sent) == []:
        if re.findall(ur'？',sent) == [] or re.findall(ur'！',sent) == []:
            sent = sent + u'。'
            
            """
            print u'--------------------------'
            print u'句点が自動挿入されました。'
            print u'--------------------------'
            """
            return sent

        else:
            pass
    else:
        pass

def check_knp_error(line):
    """
    このスクリプトの説明：KNPが何らかの事情で解析エラー（文字コードエラー等）を起こしたときに，error messageを返す．
    """
    if not re.findall(ur'ERROR:Cannot make mrph',line) == []: return u'error'
    else: return u'n'


def clause_count(tmp_list,frag):
    """
    節の数と各節が何行文の情報を持っているのか調べる関数
    """

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



def call(sentence,frag):
    """
    この関数の説明：subprocessを利用してKNPに解析処理を行わせる．syori.pyに解析結果を投げて解析結果から情報を抽出する．
    入力：sentence 日本語文（pythonのunicodeで与えること），frag スクリプト内部の詳細な結果を制御する．２にすると，詳細な結果がでる．
    
    出力：解析結果のインスタンスをまとめたリスト
    """
    code = ''
    tmp_list = []
    clause_list = []

    #Add Kuten before analysing with KNP
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

    end_of_pipe_tab = knp.stdout

    for line in end_of_pipe_tab:
        #__xx__
        #print line
        #if windows, convertion from cp932 to unicode
        #if linux, conversion from 'utf-8'
        line = unicode(line,'utf-8')
        #check KNP analysis error
        error_check = check_knp_error(line)

        if error_check == u'error': 
            print 'error! KNP fails to analyze'
            code = u'error'
            return u'error'
        else: 
            line_split = line.split(" ")
            tmp_list.append(line_split[0])
            clause_list.append(line)

    #--------------------------------------
    if code == '':

        try:
            #ここで各処理関数に情報を投げる
            clause_num, clause = clause_count(tmp_list,frag)
            #文の情報を抽出。返ってくるのはリスト
            out_list = syori.Syori(clause_list,clause_num,clause,frag)

            return out_list

        except:
            print 'something error happens.Skip this entry'
            return u'error'
