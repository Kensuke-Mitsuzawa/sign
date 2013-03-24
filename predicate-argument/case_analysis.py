#! /usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Kensuke Mitsuzawa'
__version__ = "2013/3/24"
__copyright__ = ""
__license__ = "GPL v3"

frag = 1

import sys,codecs,subprocess,readline,re,os,codecs,pickle
import call_KNP,call_juman,predicate,modi

overlap_dic = {}

entry_dic = {u'entry':u'',u'entry_h':u'',u'entry_pos':u'',u'pos_in_ex':u'',u'ex_sent':u'',u'out_list':u'',u'p_a':u'',u'modi':u'',u'ID':u''}

def conv_encoding(data, to_enc="utf_8"):
    """
    stringのエンコーディングを変換する
    @param ``data'' str object.
    @param ``to_enc'' specified convert encoding.
    @return str object.
    """
    lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
            'shift_jis', 'shift_jis_2004','shift_jisx0213',
            'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
            'iso2022_jp_ext','latin_1', 'ascii')
    for encoding in lookup:
        try:
            data = data.decode(encoding)
            print encoding
            break
        except:
            pass

def decision_analysis(entry_dic):
    """
    概要：見出し語の品詞と例文中での品詞の違いによって解析処理を別にしないといけない．そのための判断を行う．
    入力：entry_dic
    """
    
    if entry_dic[u'entry_pos'] == entry_dic[u'pos_in_ex']:
        if frag == 1:
            print u"見出し語は名詞で，例文中は名詞で利用：修飾を見る処理"
            print u'^'*40
        entry_dic = modi.add_context_word(entry_dic)
        
        
    else:
        
        if entry_dic[u'entry_pos'] == u'名詞' and entry_dic[u'pos_in_ex'] == u'動詞':
            if frag == 1:
                print u"名詞，動詞　見出し語を述語として見る処理"
                print u'^'*40
            entry_dic =  predicate.p_a(entry_dic,frag)

        elif entry_dic[u'entry_pos'] == u'動詞':
            if frag == 1:
                print u"動詞　見出し語を述語としてみる処理"
                print u'^'*40
            entry_dic = predicate.p_a(entry_dic,frag)


        elif entry_dic[u'entry_pos'] == u'形容詞':
            if frag == 1:
                print u'形容詞　修飾をみる処理'
                print u'^'*40
            modi.add_context_word(entry_dic)

    return entry_dic


def find_pos_in_ex(out_list,entry):
    """
    概要：例文中でエントリの語がどの品詞で用いられているか？を調べる．
    """
    for e_instance in out_list:
        reg_form = e_instance.reg_morp_form
        
        #entryと一致,またはentryを含む，正規化形態素を探す
        if not re.findall(entry,reg_form) == []:
            #entryを一致，または含む正規化形態素の時のposを調べる
            pos_in_ex = (e_instance.pos)
            

            return pos_in_ex


def make_entry_dic(sent):
    """
    概要：辞書エントリーとその関係する情報を含む辞書を作成する．
    辞書の内容:{entry:見出し語,entry_pos:見出し語の品詞,ex_sent:見出し語項が持つ例文,out_list:KNPによる例文の解析結果,pos_in_ex:例文中で使われている見出し語の品詞
    """
    #entry_dic = dic_initialize(entry_dic)
    entry_dic = {u'entry':u'',u'entry_h':u'',u'entry_pos':u'',u'pos_in_ex':u'',u'ex_sent':u'',u'out_list':u'',u'p_a':u'',u'modi':u'',u'ID':u''}
    #__xx__
    if frag == 1:
        print '\nNew entry starts from here'
        print u'*'*40

    u_sent = sent.decode('utf-8').strip(u'\n')
    sp_list = u_sent.split(u'\t')
    entry = sp_list[1]
    #call juman anlysis script
    entry_pos = call_juman.analysis_entry(entry)
    entry_hiragana = call_juman.get_hiragana(entry)
    
    ex_sent = sp_list[2]
    #call sentence analysis script
    out_list = call_KNP.call(ex_sent,frag)
    pos_in_ex = find_pos_in_ex(out_list,entry)
    
    entry_dic[u'ID'] = sp_list[0]
    entry_dic[u'entry'] = sp_list[1]
    entry_dic[u'entry_pos'] = entry_pos.decode('utf-8')
    entry_dic[u'ex_sent'] = sp_list[2]
    entry_dic[u'out_list'] = out_list
    entry_dic[u'pos_in_ex'] = pos_in_ex
    entry_dic[u'entry_h'] = entry_hiragana
    
                
    return entry_dic

def overlap_key(entry_dic,prev_key,i):
    """
    概要：見出し語をキーにして登録しようとすると，見出し語の重複のためにキーの区別ができなくなる．そこで，見出し語の末尾に数字をつけることで実現．
    入力：entry_dic,prev_key(ひとつ前の見出し語),i(見出し語末尾につける数字)
    出力：prev_key,i

    見出し語が直前と同じ見出し語である限り，数字に＋１を続ける．見出し語が違う見出し語になったら数字を０に戻す．
    """

    if prev_key == entry_dic[u'entry']:

        i = i + 1        
        new_key = entry_dic[u'entry'] + str(i)
        overlap_dic.setdefault(new_key,entry_dic)

    else:
        i = 0
        new_key = entry_dic[u'entry'] + str(i)
        overlap_dic.setdefault(new_key,entry_dic)
        
    if frag == 1:
        for e_key in overlap_dic:
            print 'overlap_dic key:',e_key

    prev_key = entry_dic[u'entry']
    return prev_key,i


def load_sentence():
    
    #prev_keyとkey_indexはdef overlap_keyの中で使用ために，ここで初期化
    prev_key = ''
    key_index = 0
    if os.path.exists('./sentence-list'):
        sent_list = open('./sentence-list','r').readlines()
        for sent_i,sent in enumerate(sent_list):
            entry_dic = make_entry_dic(sent)
            entry_dic = decision_analysis(entry_dic)
            prev_key,key_index = overlap_key(entry_dic,prev_key,key_index)
            write_tsv(entry_dic)
            #for developping test
            if sent_i == 10:
                #sys.exit()
                break
    else:
        sys.exit()

    pickle_dump(overlap_dic)

def write_tsv(entry_dic):
    """
    概要：tsvファイルにして書き出す
    """
    write_f = open('cat_dom_plus.tsv','w')
    
    head = (u'ID'+u'\t'+u'見出し語'+u'\t'+u'見出し語（ひらがな)'+u'\t'+u'見出し語品詞'+u'\t'+u'例文'+u'\t'+u'例文中の品詞'+u'\t'+u'|'+u'述語'+u'\t'+u'格'+u'\t'+u'項'+u'\t'+u'項１：ドメイン'+u'\t'+u'項１：カテゴリ'+u'|'+u'\n').encode('utf-8') 
    write_f.write(head)
    
    #__xx__
    if frag == 1:
        print 'entry dic is:{0}'.format(entry_dic)
        print '='*40
        print 'ID',entry_dic[u'ID']
        print '見出し語:',entry_dic[u'entry']
        print '見出し語（ひらがな）：',entry_dic[u'entry_h']
        print '見出し語の品詞：',entry_dic[u'entry_pos']
        print '例文：',entry_dic[u'ex_sent']
        print '例文中の品詞：',entry_dic[u'pos_in_ex']
        if isinstance(entry_dic[u'p_a'],dict):
            print '述語：',entry_dic[u'p_a'][u'predicate']
            for key in entry_dic[u'p_a'][u'argument']:
                print '格：',key
                if isinstance(entry_dic[u'p_a'][u'argument'][key],dict):
                    print 'カテゴリー：',entry_dic[u'p_a'][u'argument'][key][u'cat']
                    print 'ドメイン：',entry_dic[u'p_a'][u'argument'][key][u'dom']
                    print '項：',entry_dic[u'p_a'][u'argument'][key][u'arg']

        if isinstance(entry_dic[u'modi'],list):
            for e_element in entry_dic[u'modi']:
                print '意味ドメイン（修飾）',e_element[u'dom']
                print '意味カテゴリ（修飾）',e_element[u'cat']
                  
            


                         
    write_f.close()

def pickle_dump(overlap_dic):
    pic_f = open('overlap_dic.pickle','w')
    pickle.dump(overlap_dic,pic_f)

    pic_f.close()

if __name__ == '__main__':
    load_sentence()

    
