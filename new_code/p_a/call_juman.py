#! /usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Kensuke Mitsuzawa'
__version__ = "2013/3/24"
__copyright__ = ""
__license__ = "GPL v3"

import subprocess,re

def juman(_input):
    cat = ""
    domain = ""

    echo = subprocess.Popen(['echo',_input],
                            stdout=subprocess.PIPE,
                            )


    juman = subprocess.Popen(['juman'], 
                             stdin=echo.stdout,
                             stdout=subprocess.PIPE,
                             )


    end_of_pipe_juman = juman.stdout

    return end_of_pipe_juman

def get_cat_dom(arg):
    """
    概要：引き数の文字列をjumanに解析させて，意味ドメインと意味カテゴリの情報を得る
    入力：文字列
    出力：意味ドメイン，意味カテゴリ
    """
    dom = ''
    cat = ''
    
    for line in juman(arg):
        line = line.decode('utf-8')

        sp_line = line.split()
        for i,element in enumerate(sp_line):

            #print element
            if not re.findall(ur'ドメイン',element) == []:
                dom = (element.split(u':')[1]).translate({ord(u'"') : None})
                
            if not re.findall(ur'カテゴリ',element) == []:
                cat = (element.split(u':')[1]).translate({ord(u'"') : None})
                
        return cat,dom


def get_hiragana(entry):
    """
    概要：辞書の見出し語をひらがなをjumanから取得する
    """
    end_of_pipe_juman = juman(entry)

    for result_juman in end_of_pipe_juman:
        try:
            hiragana = ((result_juman.split())[1]).decode('utf-8')
        except:
            pass
        
    return hiragana


def analysis_entry(entry):
    """
    概要：辞書の見出し語をjumanで解析を行う．
    入力：見出し語

    """
    end_of_pipe_juman = juman(entry)

    for result_juman in end_of_pipe_juman:
        try:
            pos = (result_juman.split())[3]
        except IndexError:
            pass

    return pos

