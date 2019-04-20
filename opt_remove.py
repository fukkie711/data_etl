# this is for importing data from DVDs.
#coding:utf-8
import shutil
import os
from pathlib import Path
opt = ""
opt = "/Users/k-fukuzawa/Documents/bin/output"

def opt_remove():
    p = Path(opt)
    del_path = p.glob('*.xml')
    for i in del_path:
        os.remove(i)
opt_remove()
