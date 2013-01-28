#! /usr/bin/python
# -*- coding: utf-8 -*-


import sys,codecs,subprocess,readline,re,string
import negative,make_sentence
from types import *

## 辞書の定義
info_dic = {"main":"none","Ga":"none","Wo":"none","Ni":"none","He":"none","To":"none","Kara":"none","Yori":"none","De":"none","Time":"none","Predict":"none","Modi":"none"}

"""
# 節ごとの分析結果を格納するクラス
#一番最初に、c_infoクラスが呼び出されて、次にそれを継承したkihon_info、最後に２つを継承したmorp_infoが呼び出される
class c_info:
    #初期化メソッドに文節単位の情報を格納
    def __init__(self,c_dependency,position,parallel_p_num,parallel_c_num,c_clause_type):
        self.c_dep = c_dependency
        self.position = position
        self.p_p_num = parallel_p_num
        self.p_c_nun = parallel_c_num
        self.c_c_type = c_clause_type

class morp:
    def __init__(self,input_morp,reg_morp_form,pos,dom,cat):
        self.input_morp
        self.reg_morp_form
        self.pos
        self.dom
        self.cat
"""


#基本句ごとの情報を格納する
#c_infoクラスを継承する
class info:
    def __init__(self,c_dependency,c_position,parallel_p_num,parallel_c_num,c_clause_type,k_dependency,predicate,main_case,tense,case_relation,kaiseki_case,morp,main,case_check,predicate_check,clause_type,k_position,para_check,para_type,modify_type,modify_check,per,input_morp,reg_morp_form,pos,dom,cat):
        
        self.c_dep = c_dependency
        self.c_position = c_position
        self.p_p_num = parallel_p_num
        self.p_c_num = parallel_c_num
        self.c_clause_type = c_clause_type
        self.k_dep = k_dependency
        self.predicate = predicate
        self.main_case = main_case
        self.tense = tense
        self.case_relation = case_relation
        self.kaiseki_case = kaiseki_case
        self.morp = morp
        self.main = main
        self.case_check = case_check
        self.predicate_check = predicate_check
        self.clause_type = clause_type
        self.k_position = k_position
        self.para_check = para_check
        self.para_type = para_type
        self.modify_type = modify_type
        self.modify_check = modify_check
        self.per = per
        self.input_morp = input_morp
        self.reg_morp_form = reg_morp_form
        self.pos = pos
        self.dom = dom
        self.cat = cat


def structure_analyzer(clause_list,clause_num,clause):
    
    struc_dic = {'nor':[],'ques':[],'passive':[],'cause':[],'if':[],'force':[]}
    struc_dic['nor'] = "yes"

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
        #情報の抽出を正規表現でしていく
        for i in range(start_pos,end_pos + 1):
            sentence = clause_list[i]
            
            
            #--------------------------------------
            #構文情報を拾う
            #基本句単位で構文情報を拾うことが多い
            
            #〜なので、〜だから、理由を表す節の場合
            if not re.findall(r"\+.*D",sentence) == []:
                #他に述語に関する条件も含めようか、検討中
                if not re.findall(r"<節機能-理由>",sentence) == [] and not re.findall(r"<連用節>",sentence) == []:
                    struc_dic["cause"] = "yes"

            #〜もし、ifを表す構文の場合
            if not re.findall(r"\+.*D",sentence) == []:
                #同じく <条件節候補>　もありえるのだが、常にこの要素が出るのか不明
                #この条件だと、条件部分が節になっていないと対応できない。
                #つまり、”もしAが真なら、Bは偽だ”のような文には対応できなくて困る
                #いっそのこと　”もし”　があれば、条件にしてもいいような気もする
                if not re.findall(r"<節機能-条件>",sentence) == []:
                    struc_dic["if"] = "yes"
            
            #疑問文のとき（個人的には疑問文は？マークで判断してもよいとは思う
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<モダリティ-疑問>",sentence) == []:
                    struc_dic[nor] = []
                    struc_dic[ques] = "yes"

            #受け身のとき
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<態:受動>",sentence) == []:
                    struc_dic[nor] = []
                    struc_dic[passive] = "yes"

            #使役文のとき
            if not re.findall(r"\+.*D",sentence) == []:
                if not re.findall(r"<態:使役>",sentence) == []:
                    struc_dic[nor] = []
                    struc_dic[force] = "yes"

    return struc_dic
            



def Syori(clause_list,clause_num,clause,negative_choice):
    #clause_listは節ごとに切った解析結果、clause_numは節の数、clauseは各節が何行分の情報を持っているか？リスト
    #print "--------------------"

    #関数の出力。入力文と同じ並び順にしている
    out_list = []

    #カウンターの設置
    counter = 0

    #語の並び情報(order)
    order = 0

    #文節用の語の並び情報
    bnst_order = 0
    
    #ここで新しい節を読みおなし
    for value in clause:

        if counter == 0:
            start_pos = 1
            end_pos = value

        else:
            start_pos = end_pos + 1
            end_pos = end_pos + value

        counter += 1

        """
        自信がないので、コメントオフ
        bnstで必要にしてる情報は
        dep,position,parallel_type(p_type),parallel_p_num(p_p_num),parallel_c_num(p_c_num),c_clause_type(c_c_type)
        """
        

        #使用するハッシュマップは先にすべて定義しておく
        bnst_dic = {"dep":[],"position":[],"parallel_type":[],"parallel_p_num":[],"parallel_c_num":[],"c_clause_type":[]}
        kihon_dic = {"dep":[],"predicate":[],"main_case":[],"tense":[],"case_relation":[],"kaiseki_case":[],"morp":[],"main":"","case_check":"","predicate_check":"","clause_type":[],"position":"","para_check":"","para_type":[],"modify_type":[],"modify_check":"","per":""}
        morp_tmp_dic = {"input_morp":[],"reg_morp_form":[],"pos":[],"dom":[],"cat":[]}
        #形態素区別用のindex
        m_index = 0

        #情報の抽出を正規表現でしていく
        for i in range(start_pos,end_pos + 1):
            sentence = clause_list[i]

            if not re.findall(r"\*.*D|\*.*P",sentence) == []:
                #--------------------------------------------------
                #並列構造に関する記述
                #<並キ:名>は並列構造の存在を示すタグ ただ、:名　が何を示すのか？は不明
                if not re.findall(r"<並キ:.*?>",sentence) == []:
                    parallel_type = "".join((re.findall(r"<並列タイプ:.*?>",sentence))).replace("<並列タイプ:","").strip(">")
                    bnst_dic["parallel_type"] = parallel_type
                    
                    #並列の句がいくつ続いているのか？
                    parallel_p_num = "".join((re.findall(r"<並結句数:.*?>",sentence))).replace("<並結句数:","").strip(">")
                    bnst_dic["parallel_p_num"] = parallel_p_num


                    #並列の文節がいくつ続いているのか？
                    parallel_c_num = "".join((re.findall(r"<並結文節数:.*?>",sentence))).replace("<並結文節数:","").strip(">")
                    bnst_dic["parallel_c_num"] = parallel_c_num

                if not re.findall(r"\* \dD|\* -\dD|\* \dP|\* -\dP",sentence) == []:
                    bnst_dependency = re.findall(r"\* \d|\* -\d",sentence)
                    bnst_dic["dep"] = int(("".join(bnst_dependency)).strip("* "))
                
                #--------------------------------------------------
                bnst_dic["position"] = bnst_order
                #--------------------------------------------------
                #節の種類に関する記述
                c_clause_type = ""
                if not re.findall(r"<主節>",sentence) == []:
                    c_clause_type = "".join(re.findall(r"<主節>",sentence)).translate(string.maketrans("",""),"<>")  
                if not re.findall(r"<連用節>",sentence) == []:
                     c_clause_type = "".join(re.findall(r"<連用節>",sentence)).translate(string.maketrans("",""),"<>")
                if not re.findall(r"<連体節>",sentence) == []:
                    c_clause_type = "".join(re.findall(r"<連体節>",sentence)).translate(string.maketrans("",""),"<>")
                     
                bnst_dic["c_clause_type"] = c_clause_type
                
                #文節用の並び番号を＋１
                bnst_order += 1


                """
                # def __init__(self,c_dependency,position,parallel_p_num,parallel_c_num,c_clause_type):
                #c_infoクラスに移していく
                clause_info = c_info(bnst_dic["dep"],bnst_dic["position"],bnst_dic["parallel_p_num"],bnst_dic["parallel_c_num"],bnst_dic["c_clause_type"])

                """
            #基本句単位での情報をパーズしていく
            if not re.findall(r"\+.*D|\+.*P",sentence) == []:

                kihon_dic = {"dep":[],"predicate":[],"main_case":[],"tense":[],"case_relation":[],"kaiseki_case":[],"morp":[],"main":"","case_check":"","predicate_check":"","clause_type":[],"position":"","para_check":"","para_type":[],"modify_type":[],"modify_check":"","per":""}
                
                #kihon_key_name = "kihon" + str(order)
                kihon_key_name = "kihon"

                kihon_dic["position"] = order 
                #----------------------------------------------------
                #述語情報の獲得はここら辺がひっかかるはず
                predicate = []
                if not re.findall(r"<状態述語>",sentence) == []:
                    predicate = re.findall(r"<状態述語>",sentence)
                if not re.findall(r"<動態述語>",sentence) == []:
                    predicate = re.findall(r"<動態述語>",sentence)
                if not re.findall(r"<体言止>",sentence) == []:
                    predicate = re.findall(r"<体言止>",sentence)
                
                predicate = "".join(predicate).translate(string.maketrans("",""),"<>")
                kihon_dic["predicate"] = predicate
                
                if not predicate == "":
                    kihon_dic["predicate_check"] = "yes"

                #動詞の時制について
                if not re.findall(r"<時制.*?>",sentence) == []:
                    t_c = "".join(re.findall(r"<時制.*?>",sentence))
                    tense = t_c.replace("時制-","").translate(string.maketrans("",""),"<>")
                
                    kihon_dic["tense"] = tense
                

                #述語に対する主題格
                #なんか、いつも<主題格:一人称優位>な気がするんだが...
                main_case = re.findall(r"<主題格:.*?>",sentence)
                main_case = "".join(main_case).replace("<主題格:","").strip(">")

                kihon_dic["main_case"] = main_case
                #<文末>タグについて
                position_t = re.findall(r"<文末>",sentence)
                
                #IDについて
                #ID = re.findall(r"<ID:.*?>",sentence)
                #品詞について
                #pos = re.findall(r"<助詞>",sentence)

                #体言か用言か
                #taigen = re.findall(r"<体言>",sentence)
                #yougen = re.findall(r"<用言:.*?>",sentence)


                #----------------------------------------------------
                #並列構造に関する記述（アルファ版）
                if not re.findall(r"<並キ:.*?>",sentence) == []:
                    kihon_dic["para_check"] = "yes"
                    kihon_dic["para_type"] = "".join(re.findall(r"<並列タイプ:.*?>",sentence)).replace("<並列タイプ:","").strip(">")


                #----------------------------------------------------
                #節の種類に関する記述
                clause_type = ""
                if not re.findall(r"<主節>",sentence) == []:
                    clause_type = "".join(re.findall(r"<主節>",sentence)).translate(string.maketrans("",""),"<>")  
                if not re.findall(r"<連用節>",sentence) == []:
                     clause_type = "".join(re.findall(r"<連用節>",sentence)).translate(string.maketrans("",""),"<>")
                if not re.findall(r"<連体節>",sentence) == []:
                    clause_type = "".join(re.findall(r"<連体節>",sentence)).translate(string.maketrans("",""),"<>")
                     
                kihon_dic["clause_type"] = clause_type

                
                #----------------------------------------------------
                #修飾のタイプに関する記述
                #以下の３パターンについてはいずれも単に「修飾」とみなしてよい（手話の文法では）

                #その語が形容詞で用言の場合
                modify_type = ""
                if not re.findall(r"<用言:形>",sentence) == []:
                    modify_type = "".join(re.findall(r"<用言:形>",sentence)).translate(string.maketrans("",""),"<>")
                #「おおきくて」のような場合、形容詞でなく、連体詞となる
                if not re.findall(r"<連体修飾>",sentence) == []:
                    modify_type = "".join(re.findall(r"<連体修飾>",sentence)).translate(string.maketrans("",""),"<>")
                    
                #別に条件は「副詞」だけでもいいんだろうが、念のため
                if not re.findall(r"<副詞>",sentence) == [] and not re.findall(r"<修飾>",sentence) == []:
                    modify_type = "副詞"
                
                #一応、チェックを入れておく
                if not modify_type == "":
                    kihon_dic["modify_check"] = "yes"

                kihon_dic["modify_type"] = modify_type
                

                
                #----------------------------------------------------
                #パラメータが複数の状態を取りうるものは以下に記述
                #モダリティ情報リスト
                modality_list = []
                #
                #respect_list = []
                #格関係リスト
                case_relation_list = []
                i_tmp_list = []
                i_tmp_list = sentence.split("<")

                for para in i_tmp_list:
                    para = para.replace(">","")
                    if not re.findall(r"モダリティ",para) == []:
                        para = para.replace("モダリティ-","")
                        modality_list.append(para)
                             
                    if not re.findall(r"敬語:.*",para) == []:
                        para = para.replace("敬語:","")
                        respect = para
                 
                    if not re.findall(r"格関係.*",para) == []:
                        para = re.sub(r"格関係\d:","",para)
                        case_relation_list.append(para)

                        kihon_dic["case_relation"] = case_relation_list

                    if not re.findall(r"解析格:.*",para) == []:
                        kaiseki_case = para.replace("解析格:","").strip("\n")
                        
                        kihon_dic["kaiseki_case"] = kaiseki_case

                #----------------------------------------------------
                #格に関する情報の獲得
                if not re.findall(r"<格要素>",sentence) == []:
                    kihon_dic["case_check"] = "yes"
                    
                #格解析については上の方で記述しているので省略

                #主題表現をとってくる 述語のところでチェックできるから、別にいらない気もするが..
                #とりあえず、以下の記述であれば、主格　かつ　私　→一人称　となるから間違いではないだろう
                if not re.findall(r"<主題表現>",sentence) == []:
                    kihon_dic["main"] = "yes"

                    if not re.findall(r"私",sentence) == []:
                        kihon_dic["per"] = 1

                    if not re.findall(r"あなた",sentence) == []:
                        kihon_dic["per"] = 2

                    if not kihon_dic["per"] == 1 and not kihon_dic["per"] == 2:
                        kihon_dic["per"] = 3
                    

                #文頭タグにたいして
                #position_t = re.findall(r"<文頭>",sentence)
                #人称について
                #person = re.findall(r"<.*人称?>",sentence)
                #格要素(述語の箇所にも現れることがある)
                
                #品詞については述語の箇所で記述しているので省略
                #用言か体言かは述語の箇所で記述しているので省略




                #--------------------------------------
                #正規化表記を拾う
                reg_exp = re.findall(r"(<正規化代表表記:.*?>)",sentence)
                if not reg_exp == []:
                    split_list = []
                    split_list = "".join(reg_exp).split("/")
                    kihon_dic["morp"] = split_list
                

                #基本句単位でのかかりうけ情報を獲得
                if not re.findall(r"\+ \dD|\+ -\dD|\+ \dP|\+ -\dP",sentence) == []:
                    kihon_dic["dep"] = re.findall(r"\+ \d|\+ -\d",sentence)
                    kihon_dic["dep"] = int(("".join(kihon_dic["dep"])).strip("+ "))

                #--------------------------------------
                

                #文節単位のハッシュに基本句のハッシュマップを登録
                bnst_dic.setdefault(kihon_key_name,kihon_dic)

                

                print '-----------------------------'
                for one in kihon_dic:
                    print one,kihon_dic[one]
            #--------------------------------------
            #形態素情報
            if re.findall(r"\+.*D|\+.*P",sentence) == [] and re.findall(r"\*.*D|\*.*P",sentence) == []:
                #m_key_name = "morp" + str(m_index)
                m_key_name = "morp"
                morp_tmp_dic = {"input_morp":[],"reg_morp_form":[],"pos":[],"dom":[],"cat":[]}
                m_tmp_list = []
                m_tmp_list =  sentence.split(" ")
                
                morp_tmp_dic["input_morp"] = m_tmp_list[0]
                morp_tmp_dic["reg_morp_form"] = m_tmp_list[2]
                morp_tmp_dic["pos"] = m_tmp_list[3]
                
                morp_tmp_dic["dom"] = "".join(re.findall(r"<ドメイン:.*?>",sentence)).replace("<ドメイン:","").strip(">")
                morp_tmp_dic["cat"] = "".join(re.findall(r"<カテゴリ:.*?>",sentence)).replace("<カテゴリ:","").strip(">")

                #文節単位のハッシュに形態素のハッシュを登録
                bnst_dic.setdefault(m_key_name,morp_tmp_dic)
                m_index += 1

            #ここで毎回、クラスに情報を移していくとうまくいくだろう。
            #あと修正ポイント、ここですべて統合したクラスに書き込んでいってもたぶん、うまくいく。形態素から文節までの構造はすべて、bnst_dicに集約されている
            #基本句と形態素は辞書のキー、固定してやる
            #冗長だが、一度ハッシュマップから変数に代入してから、インスタンスを作成（ぼくのわかりやすさ優先）
            #--------------------------------------------
            #文節に関する情報
            c_dependency = bnst_dic["dep"]
            c_position = bnst_dic["position"]
            parallel_p_num = bnst_dic["parallel_p_num"]
            parallel_c_num = bnst_dic["parallel_c_num"]
            c_clause_type = bnst_dic["c_clause_type"]
            #--------------------------------------------
            #基本句に関する情報
            k_dependency = kihon_dic["dep"]
            predicate = kihon_dic["predicate"]
            main_case = kihon_dic["main_case"]
            tense = kihon_dic["tense"]
            case_relation = kihon_dic["case_relation"]
            kaiseki_case = kihon_dic["kaiseki_case"]
            morp = kihon_dic["morp"]
            main = kihon_dic["main"]
            case_check = kihon_dic["case_check"]
            predicate_check = kihon_dic["predicate_check"]
            clause_type = kihon_dic["clause_type"]
            k_position = kihon_dic["position"]
            para_check = kihon_dic["para_check"]
            para_type = kihon_dic["para_type"]
            modify_type = kihon_dic["modify_type"]
            modify_check = kihon_dic["modify_check"]
            per = kihon_dic["per"]
            #--------------------------------------------
            #形態素に関する情報
            input_morp = morp_tmp_dic["input_morp"]
            reg_morp_form = morp_tmp_dic["reg_morp_form"]
            pos = morp_tmp_dic["pos"]
            dom = morp_tmp_dic["dom"]
            cat = morp_tmp_dic["cat"]

            #一応、ネーミングは形態素から文節まで。という意味
            m_k_c_info = info(c_dependency,c_position,parallel_p_num,parallel_c_num,c_clause_type,k_dependency,predicate,main_case,tense,case_relation,kaiseki_case,morp,main,case_check,predicate_check,clause_type,k_position,para_check,para_type,modify_type,modify_check,per,input_morp,reg_morp_form,pos,dom,cat)

            #クラスに移し替えたら、入力文の順にリストに追加していく...ただ、これだと形態素ごとにリストに追加されちゃうよなあ
            out_list.append(m_k_c_info)

            
            
            """
            以下、クラスをいじる時に使うだろうと（思われるメモ）
            morp_tmp_dic = {"input_morp":[],"reg_morp_form":[],"pos":[],"dom":[],"cat":[]}

            kihon_dic = {"dep":[],"predicate":[],"main_case":[],"tense":[],"case_relation":[],"kaiseki_case":[],"morp":[],"main":"","case_check":"","predicate_check":"","clause_type":[],"position":"","para_check":"","para_type":[],"modify_type":[],"modify_check":"","per":""}
            参考、クラスは以下のとおり
            def __init__(self,c_dependency,c_position,parallel_p_num,parallel_c_num,c_clause_type,k_dependency,predicate,main_case,tense,case_relation,kaiseki_case,morp,main,case_check,predicate_check,clause_type,k_position,para_check,para_type,modify_type,modify_check,per,input_morp,reg_morp_form,pos,dom,cat):

            info = info(bnst_dic["c_dep"],bnst_dic["c_position"],bnst_dic["parallel_p_num"],bnst_dic["parallel_c_num"],bnst_dic["c_clause_type"],bnst_dic[],)
            """

        #語の並び情報orderを＋１しておく
        #print "word position is",order
        order += 1
        print "----------------"
        #for one in bnst_dic:
        #    print one,bnst_dic[one]
        print out_list
        for one in out_list:
            print one.input_morp
        print "morpheme is:"
        


            
    return info_dic

#修飾語と格の関係を構築する関数
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
            #ここで、modifierとcaseの順番を逆にしておく
            case_set_list.reverse()

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
        #print line
        line_split = line.split(" ")
        tmp_list.append(line_split[0])
        clause_list.append(line)
        
    #ここで各処理関数に情報を投げる
    clause_num, clause = clause_count(tmp_list)
    #returns 0 if not negation, returns 1 if negation
    negative_value = negative.find_negation(clause_list,clause_num,clause)
    
    if negative_value == 0:
        negative_choice = ""
    else:
        negative_choice = negative.negation(clause_list,clause_num,clause)

    struc_dic = structure_analyzer(clause_list,clause_num,clause)
    info_dic = Syori(clause_list,clause_num,clause,negative_choice)

    '''
    set_dic = make_case_set(info_dic)
    if not negative_choice == "":
        set_dic = add_negative(set_dic,negative_choice)
        
    print "--------------------------"
    print "About structure information"
    print struc_dic
    print "--------------------------"
    print "About case dictionary information"
    print set_dic
    print "--------------------------"

    make_sentence.sentence_rule(set_dic,struc_dic)
        
    #print set_dic
    #print info_dic

    '''

    return info_dic,struc_dic


if __name__ == '__main__':

    sentence = raw_input("文を入力してネ☆\n※必ず文末に句点かクエスチョンマークで終了してください。\n")
    info_dic,struc_dic = knp_tab(sentence)
