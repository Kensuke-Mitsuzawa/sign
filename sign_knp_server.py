#! /usr/bin/python
# -*- coding: utf-8 -*-


import sys,codecs,subprocess,readline,re

from types import *

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
                    #print "否定表現が見つかりました。どうするか考えてください。半角英数で打ち込んでネ☆\n１たたかう２にげる３ねる\n"
                    choice = raw_input("1 意思の否定 2 所有・存在の否定 3 完了の否定 4 不可能の意味 5 経験の否定 6 必要性の否定\n")
                    choice = int(choice)
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
            #else:
            #    negative = ""

    #-------------------------------
    #単なる表示の都合上
    if not negative == "":
        print negative,"is selected"
    #-------------------------------
                        
    return negative


def Syori(clause_list,clause_num,clause,negative_choice):
    #clause_listは節ごとに切った解析結果、clause_numは節の数、clauseは各節が何行分の情報を持っているか？リスト
    #print "--------------------"

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
            if not re.findall(r"\+ \dD|\+ -\dD|\+ \dP|\+ -\dP",sentence) == []:
                tmp_dic["dep"] = re.findall(r"\+ \d|\+ -\d",sentence)
                tmp_dic["dep"] = int(("".join(tmp_dic["dep"])).strip("+ "))

            #数字情報だけ欲しいので、旧コードはコメントオフしておく
            #一応残してあるだけなんで、消してもかまわない
            '''
            if not re.findall(r"\dD|-\dD",sentence)==[]:
                tmp_dic["dep"] = re.findall("\dD|-\dD",sentence)
                print tmp_dic["dep"]
            if not re.findall(r"\dP|-\dP",sentence)==[]:
                tmp_dic["dep"] = re.findall("\dP|-\dP",sentence)
                print tmp_dic["dep"]
            '''
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
            #print "".join(tmp_dic["morp"])

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
            #品詞情報（とはいってもposはcaseかmodiかpredictのどれか）
            #品詞情報の登録処理の記述はこの関数内に散らばっている。
            #現状のままでも動作には問題なさそうだけど、きたない
            if not re.findall(r"\+.*D",sentence) == []:

                if not re.findall(r"解析格:.*",sentence) == []:
                    tmp_dic["pos"] = "case"

            #--------------------------------------

            #infoクラスに情報を移していく
            #tmp_dic["dep"]だけは中身がint型整数
            t_dep = tmp_dic["dep"]
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
            #ここの部分はあとづけでなんとかしかたので、できれば、この部分をうまく処理した方がよい
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"連体修飾",sentence) == [] or not re.findall(r"<係:連用>",sentence) == []:
                    key_name = "Modi" + chr(order)
                    clause_info.pos = "modi"

                    info_dic.setdefault(key_name,clause_info)
            #--------------------------------------

            #何格か？どんな述語か？判別してinfo_dicのそれぞれの項目に登録
            if clause_info.case_analiyzed == "主題表現":
                clause_info.case_analiyzed = "main"
                info_dic["main"] = clause_info

            if clause_info.case_analiyzed == "<解析格:ガ>":
                clause_info.case_analiyzed = "Ga"
                info_dic["Ga"] = clause_info

            if clause_info.case_analiyzed == "<解析格:ヲ>":
                clause_info.case_analiyzed = "Wo"
                info_dic["Wo"] = clause_info

            if clause_info.case_analiyzed == "<解析格:ニ>":
                clause_info.case_analiyzed = "Ni"
                info_dic["Ni"] = clause_info

            if clause_info.case_analiyzed == "<解析格:へ>":
                clause_info.case_analiyzed = "He"
                info_dic["He"] = clause_info

            if clause_info.case_analiyzed == "<解析格:ト>":
                clause_info.case_analiyzed = "To"
                info_dic["To"] = clause_info

            if clause_info.case_analiyzed == "<解析格:カラ>":
                clause_info.case_analiyzed = "Kara"
                info_dic["Kara"] = clause_info

            if clause_info.case_analiyzed == "<解析格:ヨリ>":
                clause_info.case_analiyzed = "Yori"
                info_dic["Yori"] = clause_info

            if clause_info.case_analiyzed == "<解析格:デ>":
                clause_info.case_analiyzed = "De"
                info_dic["De"] = clause_info

            if clause_info.case_analiyzed == "<解析格:時間>":
                clause_info.case_analiyzed = "Time"
                info_dic["Time"] = clause_info

            if clause_info.case_analiyzed == "状態述語":
                clause_info.case_analiyzed = "Predict"
                clause_info.pos = "predict"
                info_dic["Predict"] = clause_info

            if clause_info.case_analiyzed == "動態述語":
                clause_info.case_analiyzed = "Predict"
                clause_info.pos = "predict"
                info_dic["Predict"] = clause_info
            if clause_info.case_analiyzed == "<体言止>":
                clause_info.case_analiyzed = "Predict"
                clause_info.pos = "predict"
                info_dic["Predict"] = clause_info  
            #--------------------------------------


        #語の並び情報orderを＋１しておく
        #print "word position is",order
        order += 1
        #print "----------------"
    return info_dic,struc_dic


def make_case_set(info_dic):

    #stackは文中に存在する修飾語と格をとりあえず保存するリスト
    stack = []
    #case_set_listは修飾語と格の組を保存するリスト
    case_set_list =[]
    #checked_listは処理を終えた語を保存するリスト。whileの終了条件用に作成
    checked_list = []
    #index_listは入力文の語の並びを保存しておくリスト
    index_list = []
    #mod_index_listは修飾語のみを保存しておくリスト。（修飾語だけ先に処理したいから）
    modi_index_list = []
    #set_dicは修飾語と格のセットを保存する辞書。keyは格の名前or述語,valueがセット（リスト）
    set_dic = {}

    #add all words from info_dic to stack
    for one in info_dic:
        if not info_dic[one] == 'none':
            stack.append(info_dic[one])
            index_list.append(info_dic[one].order)
            
            if info_dic[one].pos == 'modi':
                modi_index_list.append(info_dic[one].order)
                #code for check
                #print "modifier address in memory",info_dic[one]
                #print "word for one is:",info_dic[one].morpheme
                #print "dependency of it modi is:",info_dic[one].dependency
    modi_index_list.sort()

    #以下、コメントアウト中。上の記述で代用できている
    """
    for one in stack:
        if one.pos == "modi":
            modi_index_list.append(info_dic[one].order)
            # code for check
            print "modifier address in memory",one
            print "word for one is:",one.morpheme
            print "dependency of it modi is:",one.dependency
    modi_index_list.sort()
    """
    #print "modi_list is:",modi_index_list

    #初回のみ修飾語のindex listであるmodi_index_listの一番最初を指定
    if not len(modi_index_list) == 0:
        next_w = modi_index_list[0]
    else:
        next_w = index_list[0]
    
    while not len(checked_list) == len(stack):
        
        for one in stack:
            if next_w == one.order:
                checking_word = one
                break
        
        #-----------------------------------------------------------------
        #code for check
        #print "---------------------------------------"
        #print "stack is",stack
        #print index_list
        #print "next_w is",next_w
        #print "checking_word is",checking_word
        #print "pos of above word is",checking_word.pos
        #-----------------------------------------------------------------

        if checking_word.pos == "modi":
            #print "modi route is succeeful"
            case_set_list.append(checking_word)
            index_list.remove(next_w)
            modi_index_list.remove(next_w)

            next_w = checking_word.dependency
            checked_list.append(checking_word)

        if checking_word.pos == "case":
            case_set_list.append(checking_word)
            checked_list.append(checking_word)
            index_list.remove(next_w)

            case_name = checking_word.case_analiyzed

            set_dic.setdefault(case_name,case_set_list)
        
            case_set_list = []
            #もし、まだ修飾語リストが空でなかったら（他の格にかかる修飾語が存在する場合）
            if not len(modi_index_list) == 0: 
                next_w = modi_index_list[0]
            else:
                if not len(index_list) == 0:
                    next_w = index_list[0]
                else:
                    pass
                
        if checking_word.pos == "predict":
            case_set_list.append(checking_word)
            checked_list.append(checking_word)
            if next_w in index_list:
                index_list.remove(next_w)

            predict_name = checking_word.case_analiyzed
            set_dic.setdefault(predict_name,case_set_list)

            case_set_list = []
            #もし、まだ修飾語リストが空でなかったら（他の格にかかる修飾語が存在する場合）
            if not len(modi_index_list) == 0:
                next_w = modi_index_list[0]
            else:
                if not len(index_list) == 0:
                    next_w = index_list[0]
                else:
                    pass

    return set_dic


def add_negative(set_dic,negative):
    predict_list = set_dic["Predict"]
    
    dep = 'n'
    per='n'
    pos='negative'
    cat='n'
    dom='n'
    case='n'
    case_ana='n'
    order='n'

    if negative == "willness":
        reg = "ない（意思）"
        morp = "ない（意思）"

    if negative == "posess":
        reg = "ない（両手）"
        morp = "ない（両手）"

    if negative == "perfect":
        reg = "ない（未完了）"
        morp = "ない（未完了）"

    if negative == "impossible":
        reg = "無理"
        morp = "無理"

    if negative == "experience":
        reg = "。。。"
        morp = "。。。"

    if negative == "need":
        reg = "不必要"
        morp = "不必要"
        
    negative_info = info(dep,per,reg,morp,pos,cat,dom,case,case_ana,order)
    predict_list.append(negative_info)
    
    set_dic["Predict"] = predict_list


    return set_dic
    

'''
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
    
    print "ordered list is:",order_list
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
                    
                    
                

def make_sentence(info_dic,struc_dic,negative_choice,clause_num):

#---------------------------------------------------------------------
#このあたりで格とmodifierの並び替えをあらかじめしておく
#~格set = ~格 + modifier_1 + modifier_2 ... とする
#出力は print ~格set,~格set,....　とする
#---------------------------------------------------------------------    
    print "This section is Function make_sentence\n"
    
    dep_list = []
    case_set_dic = {}
    #単語数の分だけリストの要素を用意する
    position_list = []
    for temp in range(clause_num):
        position_list.append(0)
    
    print position_list

    #単語の並び順にposition_listを構成する
    #このイテレーションの後には、position_listとdep_listが出来上がっている
    for i in range(clause_num):
        for case in info_dic:
            if not (info_dic[case]) == "none":
                if i == info_dic[case].order:
                    print i,info_dic[case].morpheme
                    position_list[i] = info_dic[case]
                    dep_list.append(info_dic[case].dependency)

    #position_listは格インスタンスを、入力文と同じに並び変えた状態のリスト
    #dep_listは係り先の番号のみを入力文と同じ並びで記述した状態のリスト

        

    number = 0
    start_number = number
    end_number = number
    case_list = []

    print "test",position_list[end_number].pos
    end_number,set_list,position_list = turn_modify(number,end_number,position_list)
    del position_list[start_number:end_number+1]  


def turn_modify(number,end_number,position_list):

    index = 0
    next_index = 0
    
    for index in range(len(position_list)):

        if next_index > index:
            index = next_index

        #終了条件。もし調べた対象が「格」なら、そこで終了
            if position_list[index].pos == "case": 
                case_set.append(position_list[index])
                #key = position_list[index].case
                #case_set_dic.setdefault(key,case_set)
                case_set = []

                #継続して再帰する条件。調べた対象が「修飾語」なら、継続して再帰
            if (position_list[index].pos) == "modi":

                case_set.append(position_list[index].morpheme)
                next_index = (position_list[index].dependency)

    return set_list
    '''


def make_sentence(set_dic,negative_choice):
    if not struc_dic["nor"] == []:
        print info_dic["main"].morpheme,info_dic["Ga"].morpheme,info_dic["Predict"].morpheme

    if not struc_dic["passive"] == []:
        print info_dic["main"].morpheme, info_dic["Ni"].morpheme,info_dic["Predict"].morpheme,"pt()"

    if not struc_dic["force"] == []:
        print info_dic["main"].morpheme, info_dic["Ni"].morpheme, "pt() ",info_dic["Wo"].morpheme, info_dic["Predict"].morpheme,"+顎あげ ","わかる(+うなずき) ",info_dic["Wo"].morpheme, info_dic["Predict"].morpheme

    if not struc_dic["if"] == []:
        info_dic["main"].morpheme,info_dic["Ni"].morpheme,info_dic["Predict"].morpheme




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
        
    #ここで各処理関数に情報を投げる
    clause_num, clause = clause_count(tmp_list)
    negative_choice = negative(clause_list,clause_num,clause)
    info_dic,struc_dic = Syori(clause_list,clause_num,clause,negative_choice)
    set_dic = make_case_set(info_dic)
    if not negative_choice == "":
        set_dic = add_negative(set_dic,negative_choice)
    #make_sentence(info_dic,struc_dic,negative_choice,clause_num)
    #reorder(info_dic,struc_dic)

    print set_dic
    #print info_dic
    #print struc_dic


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
