#! /usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Kensuke Mitsuzawa'
__version__ = '2013/3/8'
__copyright__ = ''
__license__ = 'GPL v3'

def find_arg(out_list,case_name,p_a_dic):
    '''
    辞書に追加していく。
    後で辞書のキーをどんどんと追加していけば対応できる格は多くなる

    '''
    for one_i,one_ins in enumerate(out_list):
        for two_i,two_ins in enumerate(one_ins):
            
            if not isinstance(two_ins,list):
                if two_ins.kaiseki_case == case_name:
                    
                    if case_name == u'ガ':
                        p_a_dic[u'ga'] = two_ins
                    
                    if case_name == u'ニ':
                        p_a_dic[u'ni'] = two_ins

                    if case_name == u'ヲ':
                        p_a_dic[u'wo'] = two_ins

    #__xx__
    print p_a_dic
    return p_a_dic
                         

def split_relation(out_list,case_relation_list,two_ins,frag):
    
    p_a_dic = {u'pred':'',u'ga':'',u'ni':'',u'main':'',u'wo':''}
    
    p_a_dic[u'pred'] = two_ins

    if frag == 1:
        print u'-'*40
        print u'述語と格関係情報'

    for case in case_relation_list:
        case_name =  (case.split(u':'))[0]
        case_morp = (case.split(u':'))[1]

        if frag == 1:
            #__xx__
            print case_name,case_morp
            pass
            
        if case_name == u'ガ':
            p_a_dic = find_arg(out_list,case_name,p_a_dic)
            
        if case_name == u'ニ':
            p_a_dic = find_arg(out_list,case_name,p_a_dic)

        if case_name == u'ヲ':
            p_a_dic = find_arg(out_list,case_name,p_a_dic)


    return p_a_dic

def make_p_a_dic(out_list,orig_index_list,frag):

    if frag == 1:
        print u'*'*40
        print u'predicate_dicの詳細'

    #for index_orig,num_orig in enumerate(orig_index_list):
        
    for index_out,ins_out in enumerate(out_list):
        for two_i,two_ins in enumerate(ins_out):

            if not isinstance(two_ins,list):
                if two_ins.predicate_check == u'yes' and not two_ins.case_relation == []:
                    p_a_dic = split_relation(out_list,two_ins.case_relation,two_ins,frag)

            if isinstance(two_ins,list):
                    print u"list is!"
        


    return p_a_dic
