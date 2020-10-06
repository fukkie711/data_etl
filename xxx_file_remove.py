# this is for importing data from DVDs.
#coding:utf-8
import shutil
import os
from pathlib import Path
# opt = "/Users/k-fukuzawa/Dropbox/tmp/"
opt = "/Users/k-fukuzawa/Dropbox/tmp/output/"

def opt_remove_xml():
    p = Path(opt)
    del_path = p.glob('*.xml')
    for i in del_path:
        os.remove(i)

def opt_remove_pdf():
    p = Path(opt)
    del_path = p.glob('*.pdf')
    for i in del_path:
        os.remove(i)
opt_remove_xml()
opt_remove_pdf()
