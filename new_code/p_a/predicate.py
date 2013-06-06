#! /usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Kensuke Mitsuzawa'
__version__ = "2013/3/25"
__copyright__ = ""
__license__ = "GPL v3"

import re
import call_juman

def find_dom_cat(out_list,p_a_dic,arg_cont):
    a_c_d_dic = {u'arg':u'',u'cat':u'',u'dom':u''}

    #探すのはarg_cont，これをout_listのインスタンスから探し出す
    for e_instance in out_list:
        if e_instance.reg_morp_form == arg_cont:

            #__xx__
            #print "found!!"
            #print arg_cont
            a_c_d_dic[u'arg'] = arg_cont
            cat,dom = call_juman.get_cat_dom(arg_cont)
            a_c_d_dic[u'cat'] = cat
            a_c_d_dic[u'dom'] = dom

            return a_c_d_dic


def p_a(entry_dic,frag):
    """
    概要：述語解析の結果から，項を特定し，項の名詞が属する意味カテゴリと意味ドメインを判定する

    入力：entry_dic
    出力：内部構造が深くなったentry_dic.内部構造は以下の通り
    entry_dic = {見出し語，見出し語の品詞，例文中での品詞の使われ方，例文，KNPの解析結果，p_a:{述語表層名詞,述語に対応する項:{}}}
    """
    tmp_dic = {}
    p_a_dic = {u'predicate':u'',u'argument':u''}

    out_list = entry_dic['out_list']

    #__xx__
    if frag == 1:
        print '見出し',entry_dic[u'entry']
        print '見出し（ひらがな）',entry_dic[u'entry_h']

    for e_index,e_instance in enumerate(out_list):
        #__xx__
        if frag == 1:
            print 'このループでの正規化表現',e_instance.reg_morp_form
        
        #out_list中のインスタンスで，格関係リストが空でなく，かつ正規化形態素が見出し語と部分一致する時に，条件を実行する．見出し語が名詞で例文中では動詞的に利用されている時に該当
        if not e_instance.case_relation == [] and (not re.findall(entry_dic['entry'],e_instance.reg_morp_form) == [] or not re.findall(entry_dic['entry_h'],e_instance.reg_morp_form) == []):
            p_a_dic[u'predicate'] = e_instance.reg_morp_form
            
            #argument項を個別に登録していく
            for i_arg,e_arg in enumerate(e_instance.case_relation):
                
                #print e_arg
                #print e_arg.split(u':')
                arg_name = e_arg.split(':')[0]
                arg_cont = e_arg.split(':')[1]
                a_c_d_dic = find_dom_cat(out_list,p_a_dic,arg_cont)

                #argumentの名前をキーに，argumentの内容を値に持つ辞書（仮）を作成
                tmp_dic.setdefault(arg_name,a_c_d_dic)

            p_a_dic[u'argument'] = tmp_dic
            #__xx__
            #print p_a_dic
    #entry_dicにp_a_dicの内容を移しかえて戻り値とする
    entry_dic[u'p_a'] = p_a_dic
    #__xx__
    #print entry_dic

    return entry_dic

def p_a_for_input(out_list):
    """
    概要：入力文に対して，述語項構造解析をして，意味解析を返すモジュール
    """
    tmp_dic = {}
    p_a_dic = {u'predicate':u'',u'argument':u''}


    for e_instance in out_list:
        
        if not e_instance.case_relation == []:
            print e_instance.reg_morp_form
            print e_instance.case_relation

            for i_arg,e_arg in enumerate(e_instance.case_relation):
                
                arg_name = e_arg.split(':')[0]
                arg_cont = e_arg.split(':')[1]
                a_c_d_dic = find_dom_cat(out_list,p_a_dic,arg_cont)

                tmp_dic.setdefault(arg_name,a_c_d_dic)
                
            p_a_dic[u'argument'] = tmp_dic
            
    #__xx__
    print 'p_a_for_inputの内部で実行中'
    print p_a_dic
    #この述語項構造辞書を返り値にする
    return p_a_dic
