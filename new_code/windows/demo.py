#! /usr/bin/python
#! -*- coding:utf-8 -*-

def demo_test(out_list):
    """
    This function is written for demo.
    Sometimes Error happens bacasue of lack of rules.

    This script tries to open lists as much as possible.
    If error which I have not known occures, this script prints just "error".
    2013/2/24
    """
    demo_list = []

    # __xx__
    #print out_list
    for one_dim in range(len(out_list)):
        for two_dim in range(len(out_list[one_dim])):

            try:
                morp = out_list[one_dim][two_dim].reg_morp_form
                if not out_list[one_dim][two_dim].nms == "":
                    nms = out_list[one_dim][two_dim].nms
                    print nms

                print morp

            except AttributeError:
                try:

                    for three_dim in range(len(out_list[one_dim][two_dim])):
                        print out_list[one_dim][two_dim][three_dim].reg_morp_form

                except AttributeError:
                    print "error"
