#! /usr/bin/python
# -*- coding: utf-8 -*-


import sys,codecs,subprocess,readline,re
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

## 辞書の定義
info_dic = {"structure":"none","Ga":"none","Wo":"none","Ni":"none","He":"none","To":"none","Kara":"none","Yori":"none","De":"none","Time":"none","Predict":"none"}

## 節ごとの分析結果を格納するクラス
class info:
    def __init__(self,dep,per,reg,morp,pos,cat,dom,case,case_ana):
        self.dependency = dep
        self.person = per
        self.regular = reg
        self.morpheme = morp
        self.pos = pos
        self.category = cat
        self.domain = dom
        self.case = case
        self.case_analiyzed = case_ana

def Syori(clause_list,clause_num,clause):
    #clause_listは節ごとに切った解析結果、clause_numは節の数、clauseは各節が何行分の情報を持っているか？リスト
    print "--------------------"
    
    #構文読み取り用の変数
    struc = ""

    #カウンターの設置
    counter = 0
    
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

        print start_pos,end_pos

        #情報の抽出を正規表現でしていく
        for i in range(start_pos,end_pos + 1):

            sentence = clause_list[i]

            #構文情報を拾う
            #疑問文のとき
            if not re.findall(r"<モダリティ-疑問>",sentence) == []:
                struc = "interrogative"
            
            #否定文のとき
            if not re.findall(r"<否定表現>",sentence) == []:
                struc = "negative"

            
            
            #かかりうけ情報
            if not re.findall(r"\dD|-\dD",sentence) == []:
                tmp_dic["dep"] = re.findall("\dD|-\dD",sentence)
            #人称情報
            if not re.findall(r".人称",sentence) == []:
                tmp_dic["per"] = re.findall(".人称",sentence)
                            
            #品詞情報
            #info.pos = re.findall("
            #カテゴリー情報
            if not re.findall(r"(<カテゴリ:.*?>)",sentence) == []:
                tmp_dic["cat"] = re.findall("(<カテゴリ:.*?>)",sentence)

            #ドメイン情報
            if not re.findall(r"(<ドメイン:.*?>)",sentence) == []:
                tmp_dic["dom"] = re.findall("(<ドメイン:.*?>)",sentence)

            #格情報その１
            if not re.findall(r"(<係:.*?>)",sentence) == []:
                tmp_dic["case"] = re.findall("(<係:.*?>)",sentence)
            #格情報その２(格解析結果）
            if not re.findall(r"<解析格:.*?>",sentence) == []:
                tmp_dic["case_ana"] = re.findall("<解析格:.*?>",sentence)

            #正規化表記 
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



            #テスト用
            print "".join(tmp_dic["morp"])


            #述語情報を拾う。述語になって欲しいところは<係:文末>になっているので、これを述語に置きかえる
            if tmp_dic["case"] == ["<係:文末>"]:

                if not [] == re.findall(r"<状態述語>",sentence):
                    tmp_dic["case_ana"] = re.findall(r"状態述語",sentence)
                if not [] == re.findall(r"<動態述語>",sentence):
                    tmp_dic["case_ana"] = re.findall(r"動態述語",sentence)
                if not [] == re.findall(r"<体言止>",sentence):
                    tmp_dic["case_ana"] = re.findall(r"<体言止>",sentence)

            
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
            clause_info = info(t_dep,t_per,t_reg,t_morp,t_pos,t_cat,t_dom,t_case,t_case_ana)

            #何格か？どんな述語か？判別してinfo_dicのそれぞれの項目に登録
            if clause_info.case_analiyzed == "<解析格:ガ>":
                info_dic["Ga"] = clause_info
            if clause_info.case_analiyzed == "<解析格:ヲ>":
                info_dic["Wo"] = clause_info
            if clause_info.case_analiyzed == "<解析格:二>":
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

        #構文
        info_dic["structure"] = struc
            
        
        print "----------------"
    return info_dic

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
        
    clause_num, clause = clause_count(tmp_list)
    info_dic = Syori(clause_list,clause_num,clause)

    print info_dic


    return info_dic

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

    sentence = raw_input("文を入力してネ☆\n")
    info_dic = knp_tab(sentence)
         



#    knp_tree(sentence)
#    sentence = sentence.encode('utf_8')
