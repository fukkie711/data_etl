#coding:utf-8
import sys # sysモジュール読み込み
import glob # globモジュール読み込み
import os # osモジュール読み込み
import codecs # codecsモジュールの読み込み
import csv # csvモジュール読み込み
import re
# import xml.etree.ElementTree as ET
from xml.etree.ElementTree import *
from pathlib import Path

ipt = ""
opt = ""

# for test
# ipt = "/Users/k-fukuzawa/Dropbox/tmp/02input/"
# opt = "/Users/k-fukuzawa/Dropbox/tmp/02output/"

# for test (windows)
ipt = "C:/Users/kazuh/Dropbox/tmp/02input"
opt = "C:/Users/kazuh/Dropbox/tmp/02output"

#for honnbann
# ipt = sys.argv[1]
# opt = sys.argv[2]

def xml_to_csv(ipt, opt):
    p = Path(ipt)
    xml_path = p.glob('**/*.xml')
    # [機能]抽出
    # 必要な情報のみ抜き出して、新規作成したcsvファイルに書き出す
    cd_path = opt # 代入
    os.chdir(cd_path) # 読み込み先に移動
    # csv_open = open(opt + "test" + ".csv", 'w', encoding='cp932') # shift-jisで書く。utf-8でやると文字化けする… 
    # csv_open = open(opt + "/" + "xml_to_csv_output" + ".csv", 'w', encoding='cp932') # shift-jisで書く。utf-8でやると文字化けする… 
    csv_open = open(opt + "/" + p.name + ".csv", 'w', encoding='cp932') # ディレクトリ名をCSVのファイル名にする．shift-jisで書く。utf-8でやると文字化けする… 
    writer = csv.writer(csv_open, lineterminator='\n') # 改行しながらオーバーライト

    for xml_files in xml_path:
        with open(xml_files, encoding='utf_8') as f:
            print(xml_files)
            list_in = [] # リストの初期化

            # fterm_temp = []
            # csv_name = "" # CSVファイル名文字列準備
            # target = os.path.basename(f) # ファイル名を取得
            tree = parse(f) # パースコード１
            root = tree.getroot() # パースコード２

            # judge_status 廃止。すべて取る
            # judge_status = str(root.findtext('.//publication-reference/document-id/kind')) # 種別情報を抜き取り
            # * * *
            # if judge_status == "公開特許公報(A)" or judge_status == "公表特許公報(A)": # 公開&公表を篩にかける # Trueで実行

            # csvファイル作成 ←一番上のxmlファイルのファイル名＝出願番号をファイル名にしているが，あまり良くないのでやめようかと思っている
            # csv_name = str(root.findtext('.//publication-reference/document-id/date')) # 発行年月の情報を抜き取り
            # csv_open = open(csv_name + ".csv", 'a', encoding='utf_8') # なければ新規作成
            # csv_open = open(csv_name + ".csv", 'a', encoding='cp932') # shift-jisで書く。utf-8でやると文字化けする… 
            # writer = csv.writer(csv_open, lineterminator='\n') # 改行しながらオーバーライト

            # 格納
            # list_in.append(str(root.findtext('.//publication-reference/document-id/country'))) # 発行国←不要
            list_in.append(str(root.get('kind-of-jp'))) # 公開種別（jp）
            list_in.append(str(root.get('kind-of-st16'))) # 公開種別（st16）
            list_in.append(str(root.findtext('.//publication-reference/document-id/kind'))) # 公開種別（日本語）
            list_in.append(str(root.findtext('.//publication-reference/document-id/doc-number'))) # 公開番号
            list_in.append(str(root.findtext('.//publication-reference/document-id/date'))) # 公開日
            list_in.append(str(root.findtext('.//application-reference/document-id/doc-number'))) # 出願番号
            list_in.append(str(root.findtext('.//application-reference/document-id/date'))) # 出願日
            list_in.append(str(root.findtext('.//invention-title'))) # 発明の名称

            list_in.append(str(root.findtext('.//classification-ipc/main-clsf'))) # 国際特許分類(IPC)
            list_in.append(str(root.findtext('.//number-of-claims'))) # 請求項の数
            list_in.append(str(root.findtext('.//jp:total-pages', namespaces={'jp':'http://www.jpo.go.jp'}))) # 全頁数
            list_in.append("    ".join((root.find('.//classification-national')).itertext()).replace('JP', '').strip()) #FI
            list_in.append("".join((root.find('.//jp:theme-code-info', namespaces={'jp': 'http://www.jpo.go.jp'}).itertext())).replace('\n', '').strip()) if root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}) != None else list_in.append('') #テーマコード
            list_in.append("".join((root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}).itertext())).replace('\n', '').strip()) if root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}) != None else list_in.append('') # Fターム（一部Fタームの記載の無い公開特許公報（A) があるのでエラーを吐き出す. replaceメソッドで改行文字を削除している．よくわからないけどスペースが6つついている
            # fterm_temp.append("".join((root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}).itertext())).replace('\n', '')) if root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}) != None else list_in.append('') #Fターム
            # fterm_temp.append(re.sub('^      ', '', "".join(fterm_temp)))

            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="1"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="1"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="1"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="2"]/applicant[@sequence="2"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="2"]/applicant[@sequence="2"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="2"]/applicant[@sequence="2"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="3"]/applicant[@sequence="3"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="3"]/applicant[@sequence="3"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="3"]/applicant[@sequence="3"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="4"]/applicant[@sequence="4"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="4"]/applicant[@sequence="4"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="4"]/applicant[@sequence="4"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="5"]/applicant[@sequence="5"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="5"]/applicant[@sequence="5"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="5"]/applicant[@sequence="5"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="1"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="1"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="2"]/agent[@sequence="2"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="2"]/agent[@sequence="2"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="3"]/agent[@sequence="3"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="3"]/agent[@sequence="3"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="4"]/agent[@sequence="4"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="4"]/agent[@sequence="4"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="5"]/agent[@sequence="5"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="5"]/agent[@sequence="5"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="1"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="1"]/addressbook/address/text')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="2"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="2"]/addressbook/address/text')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="3"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="3"]/addressbook/address/text')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="4"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="4"]/addressbook/address/text')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="5"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="5"]/addressbook/address/text')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="6"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="6"]/addressbook/address/text')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="7"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="7"]/addressbook/address/text')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="8"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="8"]/addressbook/address/text')))

            list_in.append("    ".join((root.find('.//abstract/p').itertext()))) #要約【課題】＋【解決手段】＋【選択図】
            list_in.append("      ".join((root.find('.//claims')).itertext()).replace('\n', '').replace(' ', '')) # 請求項（すべて）
            # print(list_in)
            writer.writerow(list_in) # csvの書き出し
            # csv_open.close()
    csv_open.close()

xml_to_csv(ipt, opt)
