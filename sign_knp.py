#! /usr/bin/python
# -*- coding: utf-8 -*-


import sys,codecs,subprocess,readline,re
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

## 辞書の定義
info_dic = {"main":"none","Ga":"none","Wo":"none","Ni":"none","He":"none","To":"none","Kara":"none","Yori":"none","De":"none","Time":"none","Predict":"none","Modi":"none"}

## 節ごとの分析結果を格納するクラス
class info:
    def __init__(self,dep,per,reg,morp,pos,cat,dom,case,case_ana,order):
        self.dependency = dep
        self.person = per
        self.regular = reg
        self.morpheme = morp
        self.pos = pos
        self.category = cat
        self.domain = dom
        self.case = case
        self.case_analiyzed = case_ana
        self.order = order

def negative(clause_list,clause_num,clause):
    #否定文に関する処理を行う
    print "--------------------------"
    print "About negative information\n"

    #どの否定形か？を管理する変数
    negative = ""
    
    #カウンターの設置
    counter = 0
    
    #ここで新しい節を読みおなし
    for value in clause:

        if counter == 0:
            start_pos = 1
            end_pos = value

        else:
            start_pos = end_pos + 1
            end_pos = end_pos + value

        counter += 1

        #情報の抽出を正規表現でしていく
        for i in range(start_pos,end_pos + 1):
            sentence = clause_list[i]
            
            #+以降が単語に関する情報の（はず）なので、ここから情報を抽出する
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<否定表現>",sentence) == []:
                    print "否定表現が見つかりました。どうするか考えてください。半角英数で打ち込んでネ☆\n１たたかう２にげる３ねる\n"
                    choice = raw_input("1 意思の否定 2 所有・存在の否定 3 完了の否定 4 不可能の意味 5 経験の否定 6 必要性の否定\n")

                    #眠いのでアレだが、いちいち文字で否定種類をわけるのはいかがなものかと。数字でわけてもいいんじゃね。
                    if choice == 1:
                        negative = "willness"
                    if choice == 2:
                        negative = "posess"
                    if choice == 3:
                        negative = "perfect"
                    if choice == 4:
                        negative = "impossible"
                    if choice == 5:
                        negative = "experience"
                    if choice == 6:
                        negative = "need"


            #否定表現がなかった時。つまり否定文じゃなかった時
            else:
                negative = ""

    #-------------------------------
    #単なる表示の都合上
    if not negative == "":
        print negative,"is selected"
    #-------------------------------
                        
    return negative


def Syori(clause_list,clause_num,clause,negative_choice):
    #clause_listは節ごとに切った解析結果、clause_numは節の数、clauseは各節が何行分の情報を持っているか？リスト
    print "--------------------"

    struc_dic = {"nor":[],"ques":[],"passive":[],"cause":[],"if":[],"force":[]}

    #カウンターの設置
    counter = 0

    #語の並び情報(order)
    order = 0
    
    #ここで新しい節を読みおなし
    for value in clause:

        tmp_dic = {"dep":[],"per":[],"reg":[],"morp":[],"pos":[],"cat":[],"dom":[],"case":[],"case_ana":[]}


        if counter == 0:
            start_pos = 1
            end_pos = value

        else:
            start_pos = end_pos + 1
            end_pos = end_pos + value

        counter += 1
        
        
        #情報の抽出を正規表現でしていく
        for i in range(start_pos,end_pos + 1):
            sentence = clause_list[i]

            #--------------------------------------
            #構文情報を拾う
            #構文情報は+のところに出現するので、ここでif文分岐する
            if not re.findall(r"\+.*D",sentence) == []:
                #疑問文のとき（個人的には疑問文は？マークで判断してもよいとは思う）
                if not re.findall(r"<モダリティ-疑問>",sentence) == []:
                    struc_dic["ques"] = "OK"

                #受け身のとき
                if not re.findall(r"<態:受動>",sentence) == []:
                    struc_dic["passive"] = "OK"

                #使役文のとき
                if not re.findall(r"<態:使役>",sentence) == []:
                    struc_dic["force"] = "OK"

                else:
                    struc_dic["nor"] = "OK"
            
            #--------------------------------------
            #かかりうけ情報
            if not re.findall(r"\dD|-\dD",sentence) == []:
                tmp_dic["dep"] = re.findall("\dD|-\dD",sentence)


            #--------------------------------------
            #人称情報
            if not re.findall(r".人称",sentence) == []:
                tmp_dic["per"] = re.findall(".人称",sentence)

                            
            #--------------------------------------
            #カテゴリー情報
            if not re.findall(r"(<カテゴリ:.*?>)",sentence) == []:
                tmp_dic["cat"] = re.findall("(<カテゴリ:.*?>)",sentence)
            #--------------------------------------
            #ドメイン情報

            if not re.findall(r"(<ドメイン:.*?>)",sentence) == []:
                tmp_dic["dom"] = re.findall("(<ドメイン:.*?>)",sentence)

            #--------------------------------------
            #格情報その１
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"(<係:.*?>)",sentence) == []:
                    tmp_dic["case"] = re.findall("(<係:.*?>)",sentence)
            #格情報その２(格解析結果）
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<解析格:.*?>",sentence) == []:
                    tmp_dic["case_ana"] = re.findall("<解析格:.*?>",sentence)
                
                if not re.findall(r"<主題表現>",sentence) == []:
                    tmp_dic["case_ana"] = "主題表現"



            #--------------------------------------
            #正規化表記を拾う
            if not re.findall(r"\*.*D",sentence) == []:
                if tmp_dic["reg"] == []:
                    tmp_dic["reg"] = re.findall(r"(<正規化代表表記:.*?>)",sentence)

                    #正規化代表表記から形態素を取り出す
                    if not tmp_dic["reg"] == []:
                        #このif文内だけで使うreg_exp_listの定義
                        reg_exp_list = []
                        reg_exp = "".join(tmp_dic["reg"])
                        reg_exp = re.sub(r"<正規化代表表記:","",reg_exp) 
                        reg_exp = re.sub(r">","",reg_exp)
                
                        #大学院生が同一節内で「大学＋院生」のように分離されるのに対処
                        if not re.findall("\+",reg_exp) == []:
                            reg_exp_split = reg_exp.split("+")
                            for i in range(0,len(reg_exp_split)):
                                tmp_list = ("".join(reg_exp_split[i])).split("/")
                                reg_exp_list.append(tmp_list[0])
                                tmp_dic["morp"] = ["".join(reg_exp_list)]
                        else:
                            reg_exp_list = reg_exp.split("/")
                            #morp_1が漢字表記でmorp_2がひらがな表記
                            morp_1 = reg_exp_list[0]
                            morp_2 = reg_exp_list[1]
                            #とりあえず、漢字表記を形態素として登録する
                            tmp_dic["morp"] = [morp_1]
            #--------------------------------------    


            #テスト用
            print "".join(tmp_dic["morp"])

            #--------------------------------------
            #述語情報を拾う。述語になって欲しいところは<係:文末>になっているので、これを述語に置きかえる
            if not re.findall(r"\+.*D",sentence) == []:

                #このif条件に注意。修飾語と関係するエラーが起きることあり
                if not re.findall(r"<状態述語>",sentence) == []  and not re.findall(r"<格要素>",sentence) == []:
                    tmp_dic["case_ana"] = re.findall(r"状態述語",sentence)
                if not [] == re.findall(r"<動態述語>",sentence):
                    tmp_dic["case_ana"] = re.findall(r"動態述語",sentence)
                if not [] == re.findall(r"<体言止>",sentence):
                    tmp_dic["case_ana"] = re.findall(r"<体言止>",sentence)

            #--------------------------------------
            #infoクラスに情報を移していく
            t_dep = "".join(tmp_dic["dep"])
            t_per = "".join(tmp_dic["per"])
            t_reg = "".join(tmp_dic["reg"])
            t_morp = "".join(tmp_dic["morp"])
            t_pos = "".join(tmp_dic["pos"])
            t_cat = "".join(tmp_dic["cat"])
            t_dom = "".join(tmp_dic["dom"])
            t_case = "".join(tmp_dic["case"])
            t_case_ana = "".join(tmp_dic["case_ana"])

            clause_info = info(t_dep,t_per,t_reg,t_morp,t_pos,t_cat,t_dom,t_case,t_case_ana,order)


            #--------------------------------------
            #修飾語を拾う
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"連体修飾",sentence) == [] or not re.findall(r"<係:連用>",sentence) == []:
                    key_name = "Modi" + chr(order)
                    clause_info.pos = "ok"

                    info_dic.setdefault(key_name,clause_info)

            #--------------------------------------
            #何格か？どんな述語か？判別してinfo_dicのそれぞれの項目に登録
            if clause_info.case_analiyzed == "主題表現":
                info_dic["main"] = clause_info
            if clause_info.case_analiyzed == "<解析格:ガ>":
                info_dic["Ga"] = clause_info
            if clause_info.case_analiyzed == "<解析格:ヲ>":
                info_dic["Wo"] = clause_info
            if clause_info.case_analiyzed == "<解析格:ニ>":
                info_dic["Ni"] = clause_info
            if clause_info.case_analiyzed == "<解析格:へ>":
                info_dic["He"] = clause_info
            if clause_info.case_analiyzed == "<解析格:ト>":
                info_dic["To"] = clause_info
            if clause_info.case_analiyzed == "<解析格:カラ>":
                info_dic["Kara"] = clause_info
            if clause_info.case_analiyzed == "<解析格:ヨリ>":
                info_dic["Yori"] = clause_info
            if clause_info.case_analiyzed == "<解析格:デ>":
                info_dic["De"] = clause_info
            if clause_info.case_analiyzed == "<解析格:時間>":
                info_dic["Time"] = clause_info
            if clause_info.case_analiyzed == "状態述語":
                info_dic["Predict"] = clause_info
            if clause_info.case_analiyzed == "動態述語":
                info_dic["Predict"] = clause_info
            if clause_info.case_analiyzed == "<体言止>":
                info_dic["Predict"] = clause_info  
            #--------------------------------------


        #語の並び情報orderを＋１しておく
        print "word position is",order
        order += 1
        print "----------------"
    return info_dic,struc_dic



def reorder(info_dic,struc_dic):
    order_num_list = []
    order_list = []
    #------------------------------------------
    #　入力された文の順番通りに再構成する
    #　info_dicのorderインスタンスに順番情報があるので、この順番情報を元にきちんと並び替え処理を行う
    #------------------------------------------
    #info_dic内のそれぞれの格の入力時の並び番号を調べて、並び替え
    for key in info_dic:
        if not info_dic[key] == "none":
           # print info_dic[key].morpheme
            order_number = info_dic[key].order
            order_num_list.append(order_number)
    
    order_num_list.sort()
    print order_num_list
    #------------------------------------------
    
    #order_num_listと同じに並びになるように格インスタンスも並び替え
    for num in order_num_list:
        for key in info_dic:
            if not info_dic[key] == "none":
                if info_dic[key].order == num:
                    order_list.append(info_dic[key])
    
    print order_list
    #------------------------------------------
    #ここで入力文の通りに単語が並んでいるはず
    #------------------------------------------


    #------------------------------------------
    #修飾語のみを並び替える処理

    relation_list = []
    
    for iteration in range(0,len(order_list)):
        word_i = order_list[iteration]
        
        if (order_list[iteration]).pos == "ok":
            pointer = iteration
            

            #いまここらへんにバグっぽいのがあるのがわかっている
            while (order_list[iteration]).pos == "ok":
                relation_list.append(order_list[iteration])
                iteration += 1
                for tmp in relation_list:
                    print tmp.morpheme
                print "-------------"
                
            else:
                relation_list = [x for x in reversed(relation_list)]
                print len(relation_list)
                #for tmp in relation_list:
                    
                    
                

def make_sentence(info_dic,struc_dic,negative_choice):

    
    print "This section is Function make_sentence\n"

    if not struc_dic["nor"] == []:
        print info_dic["main"].morpheme,info_dic["Ni"].morpheme,info_dic["Predict"].morpheme

    if not struc_dic["passive"] == []:
        print info_dic["main"].morpheme, info_dic["Ni"].morpheme,info_dic["Predict"].morpheme,"pt()"

    if not struc_dic["force"] == []:
        print info_dic["main"].morpheme, info_dic["Ni"].morpheme, "pt() ",info_dic["Wo"].morpheme, info_dic["Predict"].morpheme,"+顎あげ ","わかる(+うなずき) ",info_dic["Wo"].morpheme, info_dic["Predict"].morpheme

    if not struc_dic["if"] == []:
        info_dic["main"].morpheme,info_dic["Ni"].morpheme,info_dic["Predict"].morpheme


    print "-----------------------------"


def clause_count(tmp_list):
## 節の数と各節が何行文の情報を持っているのか調べる関数    

    ## clause_numは節の数,リストclauseは各節が何行の情報を持っているか。
    clause_num = 0
    clause = []
    c_num = -1

    print "-----------------------------"

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
    print "Number of Clauses is",clause_num
    print "List of lines in each clause",clause

    return clause_num,clause


def knp_tab(sentence):

    tmp_list = []
    clause_list = []

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
        print line
        line_split = line.split(" ")
        tmp_list.append(line_split[0])
        clause_list.append(line)
        
    #ここで各処理関数に情報を投げる
    clause_num, clause = clause_count(tmp_list)
    negative_choice = negative(clause_list,clause_num,clause)
    info_dic,struc_dic = Syori(clause_list,clause_num,clause,negative_choice)
    make_sentence(info_dic,struc_dic,negative_choice)
    reorder(info_dic,struc_dic)

    print info_dic
    print struc_dic


    return info_dic,struc_dic

def knp_tree(sentence):

    echo = subprocess.Popen(['echo',sentence],
                            stdout=subprocess.PIPE,
                            )


    juman = subprocess.Popen(['juman'], 
                             stdin=echo.stdout,
                             stdout=subprocess.PIPE,
                             )


    knp = subprocess.Popen(['knp','-case','-tree'],
                           stdin = juman.stdout,
                           stdout=subprocess.PIPE,
                           )


    end_of_pipe_tree = knp.stdout

    for line in end_of_pipe_tree:
        print line




if __name__ == '__main__':

    sentence = raw_input("文を入力してネ☆\n※必ず文末に読点かクエスチョンマークで終了してください。\n")
    info_dic,struc_dic = knp_tab(sentence)
         



