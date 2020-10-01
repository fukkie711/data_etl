# this is for importing data from DVDs while changing encoding to utf_8.
#coding:utf-8

import shutil
import os
import codecs
import sys
from pathlib import Path

ipt = ""
opt = ""

# テスト用ディレクトリ
# ipt = "/Users/k-fukuzawa/Dropbox/tmp/01input/"
# opt = "/Users/k-fukuzawa/Dropbox/tmp/01output/"

# コマンドライン引数を使ってインプットディレクトリとアウトプットディレクトリを指定する
# 1はインプット，2はアウトプットディアレク取りを指定する

if len(sys.argv) < 2:
      print("インプットディレクトリを入力してください")
      sys.exit()
if len(sys.argv) < 3:
      print("アウトプットディレクトリを入力してください")
      sys.exit()


ipt = sys.argv[1]
opt = sys.argv[2]

ipt_path = Path(ipt)
opt_path = Path(opt)

def copy_xml_and_chg_ipt_codec():
    xml_path = ipt_path.glob('**/*.xml')
    for i in xml_path:
        with open(opt_path + i.name, 'w', encoding='utf_8') as f_out:
            print(opt_path, i.name)
            with open(i, encoding='euc_jp') as f_in:
                # 下記はxmlからcsvに変換する際に、euc-jpの記載があると「マルチバイト文字列は使えません」みたいなエラーが出て進まないのでやむを得ず外科手術を行った結果がこれである…
                f_out.write(f_in.read().replace('<?xml version="1.0" encoding="EUC-JP"?>', '<?xml version="1.0" encoding="UTF-8"?>'))
def copy_pdf(): #copy pdf file
    pdf_path = ipt_path.glob('**/*.pdf')
    for i in pdf_path:
        print(opt_path,i.name )
        shutil.copy2(i, opt_path + i.name)

copy_xml_and_chg_ipt_codec()
print("----------------------------------------")
print("----------xml copy files done.----------")
print("----------------------------------------")
copy_pdf()
print("----------------------------------------")
print("----------pdf copy files done.----------")
print("----------------------------------------")

# def ipt_copy_to_opt():
#     for i in xml_path:
#         print(i)
#         shutil.copy2(i, opt)
#
# ipt_copy_to_opt()
