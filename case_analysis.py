#! /usr/bin/python
# -*- coding:utf-8-*-

#------------------------------------------------------------
# KNPの解析結果から述語と格の関係のみを抽出するスクリプト
# 2012/12/31
# 大幅に修正 2013/1/7
#------------------------------------------------------------


import sys,codecs,subprocess,readline,re

def juman(word):
    cat = ""
    domain = ""

    echo = subprocess.Popen(['echo',word],
                            stdout=subprocess.PIPE,
                            )


    juman = subprocess.Popen(['/home/kensuke-mi/bin/juman'], 
                             stdin=echo.stdout,
                             stdout=subprocess.PIPE,
                             )


    end_of_pipe_tab = juman.stdout

    for result in end_of_pipe_tab:

        result_list = result.split()

        for detail in result_list:
            
            if not re.findall(r"カテゴリ:",detail) == []:
                detail = detail.strip('"')
                cat = detail

            if not re.findall(r"ドメイン:",detail) == []:
                detail = detail.strip('"')
                domain = detail

    return cat,domain

#def Syori(clause_list,clause_num,clause):
def Syori(sentence):
    # 格解析結果を保存するリスト
    a_r_list = []
    
    # 出力を一時的に保存しておくリスト
    print_list = []

    '''
    #clause_listは節ごとに切った解析結果、clause_numは節の数、clauseは各節が何行分の情報を持っているか？リスト
    #print "--------------------"

    #カウンターの設置
    counter = 0

    #語の並び情報(order)
    order = 0
    
    #ここで新しい節を読みおなし
    for value in clause:

        if counter == 0:
            start_pos = 1
            end_pos = value

        else:
            start_pos = end_pos + 1
            end_pos = end_pos + value

        counter += 1
        
        print "-------------------------"
        print " ".join(clause_list)
        #print "below sentence is result of KNP"        
        #情報の抽出を正規表現でしていく
        for i in range(start_pos,end_pos + 1):
            sentence = clause_list[i]

            #print sentence

            #-----------------------------------------------------------
            # KNPの解析結果のうち、述語の、述語と格の関係のみを記述した行のみを正規表現で切り出し

            if not re.findall(r"\+.*D",sentence) == []:
                
                if not re.findall(r"<格解析結果:.*?>",sentence) == []:
                    

                    analysis_result = re.findall(r"<格解析結果:.*?>",sentence)

                    analysis_result = "".join(sentence)
                    # <が邪魔なので切る
                    a_r_list = analysis_result.split("<")
'''
    #-----------------------------------------------------------
    # KNPの解析結果のうち、述語の、述語と格の関係のみを記述した行のみを正規表現で切り出し

    if not re.findall(r"\+.*D",sentence) == []:
        if not re.findall(r"<主節>",sentence) == []:
            if not re.findall(r"<格解析結果:.*?>",sentence) == []:
                    

                analysis_result = re.findall(r"<格解析結果:.*?>",sentence)

                analysis_result = "".join(sentence)
                # <が邪魔なので切る
                a_r_list = analysis_result.split("<")


            
    #-----------------------------------------------------------
    # 切り出された行から、さらに述語と格関係のみの箇所を切り出す
    for i in range(len(a_r_list)):
        tmp = a_r_list[i]
        tmp = tmp.strip(">")
        if not re.findall("格解析結果:.*",tmp) == []:
            print_list = []
            a_r = a_r_list[i]
            
            case_relation_list = a_r.split(":")
            predicate = case_relation_list[1]
            print_list.append(predicate)
            print_list.append(" ")
            
            case = case_relation_list[3]
            each_case_list = case.split(";")

            for ii in range(len(each_case_list)):
                each_case = each_case_list[ii]
                list = each_case.split("/")

                case = list[0]
                word_to_case = list[2]

               
                if not word_to_case == "-":

                    category,domain = juman(word_to_case)
                    format = case+" "+word_to_case+" "+category+" "+domain
                    print_list.append(format)

    return print_list

def clause_count(tmp_list):
## 節の数と各節が何行文の情報を持っているのか調べる関数    

    ## clause_numは節の数,リストclauseは各節が何行の情報を持っているか。
    clause_num = 0
    clause = []
    c_num = -1

    #print "-----------------------------"

    for tmp in tmp_list:
 
       
        if tmp == "*":   
            ## 前の節が何行分の情報を持っていたか。リストに追加する
            clause.append(c_num)
            
            ## c_numの数を初期化
            c_num = 1
            
            ## clause_numの数をひとつ増やす
            clause_num += 1
            
        ## 処理の都合上、最後の節はカウントできないので、無理やりだけど、こうする 
        elif tmp == "EOS\n":
            
            ## EOSの前には。、？！の記号しかないと仮定して-1する
            c_num = c_num - 1
            clause.append(c_num)

        else:            
            c_num += 1

    clause.pop(0)
    #print "Number of Clauses is",clause_num
    #print "List of lines in each clause",clause

    return clause_num,clause


def knp_tab(sentence):

    tmp_list = []
    clause_list = []

    echo = subprocess.Popen(['echo',sentence],
                            stdout=subprocess.PIPE,
                            )


    juman = subprocess.Popen(['/home/kensuke-mi/bin/juman'], 
                             stdin=echo.stdout,
                             stdout=subprocess.PIPE,
                             )


    knp = subprocess.Popen(['knp','-case','-tab'],
                           stdin = juman.stdout,
                           stdout=subprocess.PIPE,
                           )


    end_of_pipe_tab = knp.stdout

    for line in end_of_pipe_tab:

        #print line
       
        line_split = line.split(" ")
        tmp_list.append(line_split[0])
        clause_list.append(line)
        format_list = Syori(line)
        if not format_list == []:
            return format_list
    
    #ここで各処理関数に情報を投げる
    #clause_num, clause = clause_count(tmp_list)
    #Syori(clause_list,clause_num,clause)
    

if __name__ == '__main__':

    output_f = open('out-list','w')
    input_f = open("sentence-list",'r')
    sentence_list = input_f.readlines()
    for sentence in sentence_list:
        sen_list = []
        
        sentence_l = sentence.split('\t')
        sentence = sentence_l[2]
        sentence = sentence.strip('\n')
        for sen in sentence:
            if not sen == " ":
                sen_list.append(sen)

            else:
                pass
        sentence = "".join(sen_list)

        format = knp_tab(sentence)
        format = "".join(format)
        
        out_format = sentence_l[0] + "\t" + sentence_l[1] + "\t" +sentence + "\t" + str(format) + "\n"

        print out_format
        output_f.writelines(out_format)
    
    output_f.close()


