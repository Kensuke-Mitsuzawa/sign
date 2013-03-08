#!usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Kensuke Mistuzawa'
__version__ = '2013/3/9'
__copyright__ = ''
__license__ = 'GPL v3'


def sentence(struc_dic,p_a_dic,out_list,frag):

    sent = []

    if frag == 1:
        print u'*'*40
        print u'手話構文に関する情報'

    if struc_dic[u'force'] == u'yes':
        sent = [(p_a_dic[u'ga']).reg_morp_form,(p_a_dic['ni']).reg_morp_form,u'pt3',p_a_dic['wo'].reg_morp_form,p_a_dic['pred'].reg_morp_form,u'jaw_up',p_a_dic['wo'].reg_morp_form,p_a_dic['pred'].reg_morp_form,u'pt3']

    if struc_dic[u'passive'] == u'yes':
        sent = [p_a_dic['ga'].reg_morp_form,p_a_dic['ni'].reg_morp_form,p_a_dic['pred'].reg_morp_form,u'pt3']

    

    print ' '.join(sent)
    

