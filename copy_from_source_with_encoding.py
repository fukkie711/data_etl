# this is for importing data from DVDs while changing encoding to utf_8.
#coding:utf-8

import shutil
import os
import codecs
from pathlib import Path
ipt = ""
opt = ""

ipt = "/Users/k-fukuzawa/Dropbox/tmp/input/"
opt = "/Users/k-fukuzawa/Dropbox/tmp/output/"

p = Path(ipt)
xml_path = p.glob('**/*.xml')
pdf_path = p.glob('**/*.pdf')

def copy_xml_and_chg_ipt_codec():
    for i in xml_path:
        with open(opt + i.name, 'w', encoding='utf_8') as fout:
            with open(i, encoding='euc_jp') as fin:
                fout.write(fin.read())
def copy_pdf(): #copy pdf file
    for i in pdf_path:
        shutil.copy2(i, opt + i.name)

copy_xml_and_chg_ipt_codec()
copy_pdf()

# def ipt_copy_to_opt():
#     for i in xml_path:
#         print(i)
#         shutil.copy2(i, opt)
#
# ipt_copy_to_opt()
