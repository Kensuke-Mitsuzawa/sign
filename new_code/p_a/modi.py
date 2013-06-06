#! /usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Kensuke Mitsuzawa'
__version__ = "2013/3/24"
__copyright__ = ""
__license__ = "GPL v3"


import re
import call_juman



def find_dom_cat(context_list):
    """
    概要：call_jumanに仕事を投げて，意味カテゴリと意味ドメインを求める.意味カテゴリとドメインをまとめた辞書を作成し，それをcat_dom_listを作成して返す．

    出力：cat_dom_list　例文中の単語を単語毎に，意味ドメインと意味カテゴリの辞書を作成し，追加したリスト（表層単語は必要ない：実際に利用する時に表層を見ても意味がないから）
    """
    cat_dom_list = []


    for e_word in context_list:
        cat_dom_dic = {u'cat':u'',u'dom':u''}
        cat,dom = call_juman.get_cat_dom(e_word)
        cat_dom_dic[u'cat'] = cat
        cat_dom_dic[u'dom'] = dom

        cat_dom_list.append(cat_dom_dic)

    return cat_dom_list
        
def add_context_word(entry_dic):
    """
    概要：例文中の対象語の周辺単語をリストに追加する．find_dom_catに仕事を投げて，意味カテゴリと意味ドメインをもつリストを得る．entry_dicにそのリストを追加して，entry_dicを返す．
    """

    context_list = []
    for e_instance in entry_dic[u'out_list']:
        reg_morp_form = e_instance.reg_morp_form

        context_list.append(reg_morp_form)
    
    if entry_dic[u'entry'] in context_list:
        context_list.remove(entry_dic[u'entry'])
    if entry_dic[u'entry_h'] in context_list:
        context_list.remove(entry_dic[u'entry_h'])

    cat_dom_list = find_dom_cat(context_list)

    entry_dic[u'modi'] = cat_dom_list

    return entry_dic

def add_all_morp(out_list):
    """
    概要：解析済みの例文を受け取って，すべての形態素の意味解析をjumanに投げるモジュール
    """

    morp_list = []

    for e_instance in out_list:
        reg_morp_form = e_instance.reg_morp_form

        morp_list.append(reg_morp_form)

    cat_dom_list = find_dom_cat(morp_list)
    
    return cat_dom_list
