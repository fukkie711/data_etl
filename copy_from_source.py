# this is for importing data from DVDs.
#coding:utf-8
import shutil
import os
import codecs
from pathlib import Path
ipt = ""
opt = ""

ipt = "/Users/k-fukuzawa/Documents/bin/JPG_2014039/DOCUMENT/A/2014132001/2014132801/"
opt = "/Users/k-fukuzawa/Documents/bin/output/"

p = Path(ipt)
xml_path = p.glob('**/*.xml')
pdf_path = p.glob('**/*.pdf')

def chg_ipt_codec():
    for i in xml_path:
        with open(opt + i.name, 'w', encoding='utf_8') as fout:
            with open(i, encoding='euc_jp') as fin:
                fout.write(fin.read())
chg_ipt_codec()

# def ipt_copy_to_opt():
#     for i in xml_path:
#         print(i)
#         shutil.copy2(i, opt)
#
# ipt_copy_to_opt()
