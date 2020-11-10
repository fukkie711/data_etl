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
# ipt = "C:/Users/kazuh/Dropbox/tmp/02input"
# opt = "C:/Users/kazuh/Dropbox/tmp/02output"

#for honnbann
ipt = sys.argv[1]
opt = sys.argv[2]

def xml_to_csv(ipt, opt):
    p = Path(ipt)
    xml_path = p.glob('**/*.xml')
    # [機能]抽出
    # 必要な情報のみ抜き出して、新規作成したcsvファイルに書き出す
    # ※出力されたcsvファイルをExcelで開くと謎の改行がある場合があるが，これはおそらくExcelで開くときのCSV最大表示可能文字数の上限を超えたためだと思われる．
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
            list_in.append("".join((root.find('.//classification-national')).itertext()).replace('JP', '').strip().replace('\n', '')) if root.find('.//classification-national') != None else list_in.append('')#FI 
            list_in.append("".join((root.find('.//jp:theme-code-info', namespaces={'jp': 'http://www.jpo.go.jp'}).itertext())).replace('\n', '').strip()) if root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}) != None else list_in.append('') #テーマコード
            list_in.append("".join((root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}).itertext())).replace('\n', '').strip()) if root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}) != None else list_in.append('') # Fターム（一部Fタームの記載の無い公開特許公報（A) があるのでエラーを吐き出す. replaceメソッドで改行文字を削除している．よくわからないけどスペースが6つついている
            # fterm_temp.append("".join((root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}).itertext())).replace('\n', '')) if root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}) != None else list_in.append('') #Fターム
            # fterm_temp.append(re.sub('^      ', '', "".join(fterm_temp)))
            # 出願人情報
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
            # 代理人情報
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
            # 発明者情報
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
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="9"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="9"]/addressbook/address/text')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="10"]/addressbook/name')))
            list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="10"]/addressbook/address/text')))
            #要約【課題】＋【解決手段】＋【選択図】
            list_in.append("    ".join((root.find('.//abstract/p').itertext())).replace('\n', '').strip())  if root.find('.//abstract/p') != None else list_in.append('')
            # 請求項（すべて）
            list_in.append("    ".join((root.find('.//claims').itertext())).replace('\n', '').strip()) if root.find('.//claims') != None else list_in.append('')
            # 技術分野（すべて）
            list_in.append("    ".join((root.find('.//technical-field').itertext())).replace('\n', '').strip()) if root.find('.//technical-field') != None else list_in.append('')
            # 背景技術（すべて）
            list_in.append("    ".join((root.find('.//background-art').itertext())).replace('\n', '').strip()) if root.find('.//background-art') != None else list_in.append('')
            # 特許文献（すべて）
            list_in.append("    ".join((root.find('.//patent-literature').itertext())).replace('\n', '').strip()) if root.find('.//patent-literature') != None else list_in.append('')
            # 非特許文献（すべて）
            list_in.append("    ".join((root.find('.//non-patent-literature').itertext())).replace('\n', '').strip()) if root.find('.//non-patent-literature') != None else list_in.append('')
            # 発明が解決しようとする課題
            list_in.append("    ".join((root.find('.//tech-problem').itertext())).replace('\n', '').strip()) if root.find('.//tech-problem') != None else list_in.append('')
            # 発明を解決するための手段
            list_in.append("    ".join((root.find('.//tech-solution').itertext())).replace('\n', '').strip()) if root.find('.//tech-solution') != None else list_in.append('')
            # 発明の効果
            list_in.append("    ".join((root.find('.//advantageous-effects').itertext())).replace('\n', '').strip()) if root.find('.//advantageous-effects') != None else list_in.append('')
            # 発明を実施するための形態
            list_in.append("    ".join((root.find('.//description-of-embodiments').itertext())).replace('\n', '').strip().rstrip('\n')) if root.find('.//description-of-embodiments') != None else list_in.append('')
            # 産業利用上の可能性
            list_in.append("    ".join((root.find('.//industrial-applicability').itertext())).replace('\n', '').strip()) if root.find('.//industrial-applicability') != None else list_in.append('')
            # 図面の簡単な説明
            list_in.append("    ".join((root.find('.//description-of-drawings').itertext())).replace('\n', '').strip()) if root.find('.//description-of-drawings') != None else list_in.append('')

            print(list_in)
            # 結果がNoneの行を排除
            if list_in[0] == 'None':
                continue
            writer.writerow(list_in) # csvの書き出し
    csv_open.close()

xml_to_csv(ipt, opt)
