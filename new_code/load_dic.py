#! /usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Kensuke Mitsuzawa'
__version__ = "2013/3/25"
__copyright__ = ""
__license__ = "GPL v3"

import pickle,re
import p_a.call_juman,p_a.call_KNP,p_a.modi,p_a.predicate

frag = 1


def load_pickle():

    pickle_file = file('overlap_dic.pickle','r')
    sign_dic = pickle.load(pickle_file)
    pickle_file.close()

    key_list = make_key_list(sign_dic)

    return sign_dic,key_list

def make_dic_for_input(input_snet):
    ex_dic = {u'modi':u'',u'ex_sent':u'',u'out_list':u'',u'p_a':u''}

    out_list = p_a.call_KNP.call(input_sent,frag)
    #ここでmodiモジュール内にすべての形態素の意味解析を行うモジュールを追加
    cat_dom_list = p_a.modi.add_all_morp(out_list)
    #ここに述語項構造解析をするモジュールも追加
    #いまの仕様だと，一文には一個しか述語がない，という前提のもとでコードを書いているので，かなりまずい．
    #KNPはすべての述語に対して格解析をするので，そのように改良しないとマズいだろう．
    p_a_dic = p_a.predicate.p_a_for_input(out_list)
    
    ex_dic[u'modi'] = cat_dom_list
    ex_dic[u'out_list'] = out_list
    ex_dic[u'p_a'] = p_a_dic

    return ex_dic

def make_key_list(sign_dic):
    """
    概要：見出し語検索を円滑にするために，辞書のキーをリストに保存しておく．
    """

    key_list = []

    for key in sign_dic:
        key_list.append(key)

    return key_list
    
def find_entry(japn_morp,key_list):
    """
    概要：日本語形態素を受け取って，posを判断させて，posで辞書のどの部分にアクセスすべきか決定する
    入力：new_sign.pyからの日本語形態素
    出力：データベースID
    """
    cand_list = []
    
    """
    ここの処理をもっとうまくできないか？疑問に思う．二重forで無駄がおおい．

    日本語形態素が動詞もありうると予めわかっているなら，辞書の側で例文が動詞の時には，見出し語を動詞にすべきだろう？その処理を怠ったんで，いまここでちょいと無理があることをやってるわけ
    """
    #日本語形態素も文字レベルまで分解
    for japn_char in japn_morp:
        for key_i,key in key_list:
            
            if not re.findall(japn_char,key) == []:
                cand_list.append(key)

    

def decision_pos():

    pos = call_juman.analysis_entry()
    """
    if pos == u'名詞' or u'形容詞': 
        print '辞書ないのmodiにアクセス'

    if pos == u'辞書内のpredicateにアクセス'
    
    """


if __name__ == '__main__':
    input_sent = u'今日はいい天気ですね．'
    sign_dic,key_list = load_pickle()
    make_dic_for_input(input_sent)
    
