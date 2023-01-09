#coding:utf-8
import sys # sysモジュール読み込み
import glob # globモジュール読み込み
import os # osモジュール読み込み
import codecs # codecsモジュールの読み込み
import csv # csvモジュール読み込み
import re
# import xml.etree.ElementTree as ET
# from xml.etree.ElementTree import *
import xml.etree.ElementTree as ET
from pathlib import Path

import shutil
import datetime
import pathlib
import time
from tqdm import tqdm
import chardet
from tqdm import tqdm


# コマンドライン引数を使ってインプットディレクトリとアウトプットディレクトリを指定する
# 1はインプット，2はアウトプットディレクトリを指定する
if len(sys.argv) < 2:
      print("インプットディレクトリを入力してください")
      sys.exit()
# if len(sys.argv) < 3:
#       print("アウトプットディレクトリを入力してください")
#       sys.exit()

src_dir = pathlib.Path(sys.argv[1])
# output_dir = pathlib.Path(sys.argv[2])
print(src_dir)
def xml_to_csv(src_dir):
    start_time = datetime.datetime.now()
    # dirs = os.listdir(src_dir)
    dirs = glob.glob(f"{sys.argv[1]}/**/")
    for dir in tqdm(dirs):
        # print(dir)
        # if os.path.isdir(dir):
        # time.sleep(0.1)
        # xml_directory = pathlib.Path('xml')    # p = Path(ipt)



    # for dir_num in range(390, 401):
        # src_path = src + '/' + str(dir_num) 
        # src_path = Path(src_path)
        # csv_open = open(str(src_path) + '/' + str(dir_num) + '.csv', "w", encoding='cp932')
        # ファイル名をつけるのは一工夫がいる。下記参照
        # Python でディレクトリのファイルをフルパスで取得する - それマグで！ https://takuya-1st.hatenablog.jp/entry/2014/04/26/030540
        # Pythonで条件を満たすパスの一覧を再帰的に取得するglobの使い方 | note.nkmk.me https://note.nkmk.me/python-glob-usage/
        csv_open = open(str(dir)  + str(os.path.basename(dir.rstrip(os.sep))) + '.csv', 'w', encoding='cp932')
        writer = csv.writer(csv_open, lineterminator='\n') # 改行しながらオーバーライト
        # xml_path = dir.glob('**/*.xml')
        xml_path = glob.glob(f'{dir}/**/*.xml', recursive=True)

        # ※出力されたcsvファイルをExcelで開くと謎の改行がある場合があるが，これはおそらくExcelで開くときのCSV最大表示可能文字数の上限を超えたためだと思われる．
        for xml_file in tqdm(xml_path):
            encoding_setting = ''
            with open(xml_file, 'rb') as f:
                # print(xml_file)
                encoding_setting_raw = chardet.detect(f.read())['encoding']

                # 確認用
                # print(encoding_setting_raw)

                # 基本的にはEUC-JPのみを抽出すればいい。その他の文字コード（言語）で書かれたものは分析対象ではないため
                if encoding_setting_raw == "UTF-8-SIG":
                    encoding_setting = 'utf_8'
                if encoding_setting_raw == 'EUC-JP':
                    encoding_setting = 'euc_jp'
                # if encoding_setting == 'utf-8-SIG':
                #     encoding_setting = 'utf-8'
            try:
                with open(xml_file, encoding=encoding_setting) as f:
                # with open(xml_files, encoding='cp932') as f:
                    list_in = [] # リストの初期化

                    # tree = parse(f)
                    # root = tree.getroot()
                    
                    # 上記の従来の処理だとValueError: multi-byte encodings are not supportedが出てしまうため下記に変更予定
                    xml = f.read()
                    root = ET.fromstring(xml)
                    # データ抽出
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
                    #FI ここはappendでスペース入れないとスペース入れてくれない
                    list_in.append("      ".join((root.find('.//classification-national')).itertext()).replace('JP', '').strip().replace('\n', '')) if root.find('.//classification-national') != None else list_in.append('None')
                    #テーマコード
                    list_in.append("".join((root.find('.//jp:theme-code-info', namespaces={'jp': 'http://www.jpo.go.jp'}).itertext())).replace('\n', '').strip()) if root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}) != None else list_in.append('None')
                    # Fターム（一部Fタームの記載の無い公開特許公報（A) があるのでエラーを吐き出す. replaceメソッドで改行文字を削除している．よくわからないけどスペースが6つついている
                    list_in.append("".join((root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}).itertext())).replace('\n', '').strip()) if root.find('.//jp:f-term-info', namespaces={'jp': 'http://www.jpo.go.jp'}) != None else list_in.append('None')
                    # 出願人情報
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="1"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="1"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="1"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
                    
                    # 2021/03/13 fixed applicant-agents sequence number to 1 (not 2, 3, ...5)
                    # list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="2"]/applicant[@sequence="2"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    # list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="2"]/applicant[@sequence="2"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    # list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="2"]/applicant[@sequence="2"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="2"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="2"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="2"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="3"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="3"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="3"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="4"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="4"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="4"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="5"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="5"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="5"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="6"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="6"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="6"]/addressbook[@lang="ja"]/address/text', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="7"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="7"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="7"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="8"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="8"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="8"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="9"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="9"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="9"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="10"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="10"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="10"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="11"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="11"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="11"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="12"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="12"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="12"]/addressbook[@lang="ja"]/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    # 代理人情報
                    # 2021/03/13 fixed applicant-agents sequence number to 1 (not 2, 3, ...5)
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="1"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="1"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="2"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="2"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="3"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="3"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="4"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="4"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="5"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="5"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="6"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="6"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="7"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="7"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="8"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="8"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="9"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="9"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="10"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="10"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="11"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="11"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="12"][@jp:kind="representative"]/addressbook/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})))
                    list_in.append(str(root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/agent[@sequence="12"][@jp:kind="representative"]/addressbook/name', namespaces={'jp':'http://www.jpo.go.jp'})))
                    # 発明者情報
                    # 2021/03/13 fixed applicant-agents sequence number to 1 (not 2, 3, ...5)
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
                    list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="11"]/addressbook/name')))
                    list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="11"]/addressbook/address/text')))
                    list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="12"]/addressbook/name')))
                    list_in.append(str(root.findtext('.//parties/inventors/inventor[@sequence="12"]/addressbook/address/text')))
                    #要約【課題】＋【解決手段】＋【選択図】
                    list_in.append("    ".join((root.find('.//abstract/p').itertext())).replace('\n', '').strip())  if root.find('.//abstract/p') != None else list_in.append('None')
                    # 請求項（すべて）
                    list_in.append("    ".join((root.find('.//claims').itertext())).replace('\n', '').strip()) if root.find('.//claims') != None else list_in.append('None')
                    # 技術分野（すべて）
                    list_in.append("    ".join((root.find('.//technical-field').itertext())).replace('\n', '').strip()) if root.find('.//technical-field') != None else list_in.append('None')
                    # 背景技術（すべて）
                    list_in.append("    ".join((root.find('.//background-art').itertext())).replace('\n', '').strip()) if root.find('.//background-art') != None else list_in.append('None')
                    # 特許文献（すべて）
                    list_in.append("    ".join((root.find('.//patent-literature').itertext())).replace('\n', '').strip()) if root.find('.//patent-literature') != None else list_in.append('None')
                    # 非特許文献（すべて）
                    list_in.append("    ".join((root.find('.//non-patent-literature').itertext())).replace('\n', '').strip()) if root.find('.//non-patent-literature') != None else list_in.append('None')
                    # 発明が解決しようとする課題
                    list_in.append("    ".join((root.find('.//tech-problem').itertext())).replace('\n', '').strip()) if root.find('.//tech-problem') != None else list_in.append('None')
                    # 発明を解決するための手段
                    list_in.append("    ".join((root.find('.//tech-solution').itertext())).replace('\n', '').strip()) if root.find('.//tech-solution') != None else list_in.append('None')
                    # 発明の効果
                    list_in.append("    ".join((root.find('.//advantageous-effects').itertext())).replace('\n', '').strip()) if root.find('.//advantageous-effects') != None else list_in.append('None')
                    # 発明を実施するための形態
                    list_in.append("    ".join((root.find('.//description-of-embodiments').itertext())).replace('\n', '').strip().rstrip('\n')) if root.find('.//description-of-embodiments') != None else list_in.append('None')
                    # 産業利用上の可能性
                    list_in.append("    ".join((root.find('.//industrial-applicability').itertext())).replace('\n', '').strip()) if root.find('.//industrial-applicability') != None else list_in.append('None')
                    # 図面の簡単な説明
                    list_in.append("    ".join((root.find('.//description-of-drawings').itertext())).replace('\n', '').strip()) if root.find('.//description-of-drawings') != None else list_in.append('None')

                    # print(list_in)
                    # 結果がNoneの行を排除
                    if list_in[0] == 'None':
                        continue
                    writer.writerow(list_in) # csvの書き出し
            # "Big5"(香港・台湾の文字コード？)などが出てくると「LookupError: unknown encoding:」が出てくるので対策
            except LookupError:
                continue
            except Exception as e:
                print("exception type: ", type(e), "messege: ", e)
                print(xml_file)
    csv_open.close()
    finish_time = datetime.datetime.now()
    print("--------------------------------------------------------------------")
    print("{0}: {1:%Y/%m/%d %H:%M} .pdf copy files start.".format(src_dir, start_time))
    print("{0}: {1:%Y/%m/%d %H:%M} .pdf copy files done.".format(src_dir, finish_time))
    print("--------------------------------------------------------------------")# コマンドライン引数からCSVを検索して作成するディレクトリを指定する
# xml_to_csv(ipt, opt)
xml_to_csv(src_dir)
