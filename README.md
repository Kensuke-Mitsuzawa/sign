#まだα版にも達していません...

***

# 日本語ー手話（日本語ラベル表示）変換システム

##　概要

日本語を入力すると、日本語対応手話に変換してくれるシステム。日本語ラベルで表示されます。   
※手話には統一された文字表記法がないので、便宜上日本語の単語で表現する。これを日本語レベルという

## ディレクトリの構成

new_code:それなりに使えるコード   
old:使えない子   
predicate-argument:実験用

## 必要な物

juman **JUMAN Ver.7.0**   
<http://nlp.ist.i.kyoto-u.ac.jp/index.php?cmd=read&page=JUMAN&alias%5B%5D=%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%BD%A2%E6%85%8B%E7%B4%A0%E8%A7%A3%E6%9E%90%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0JUMAN>

KNP **KNP Ver.4.0.1**   
 <http://nlp.ist.i.kyoto-u.ac.jp/index.php?KNP>

古いバージョンのjumanだと文字コードの都合上、動作しません。

## 準備

new\_code/new\_sign.pyの関数knp_tabの内部にある部分を自分の環境でのjumanとKNPのパスに書き換える。   
※通常のローカルインストールの場合は不要。通常とは違う場所にインストールしたときに必要

例:/usr/local/binにjumanのパスが通っている場合   
    juman = subprocess.Popen(['/usr/local/bin/juman'],   
に書き換える。

## 使い方

new\_codeディレクトリでメインスクリプトを実行すると、日本語を入力するように。と出るので入力する。   
    python new_sign.py
