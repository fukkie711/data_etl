import os
import csv # csvモジュール読み込み
from pathlib import Path

pt = ""
opt = ""
# src = 'G:\\pupa'
src = 'D:\\patent_db\\pupa'

def get_size(src):
    name = 'D:/patent_db/memo' + '/' + 'filesizee_list.csv'
    name2 = Path(name)

    csv_open = open(name2, "w", encoding='utf-8')
    writer = csv.writer(csv_open, lineterminator='\n')
    # p = Path(ipt)
    for dir_num in range(1, 900):
        filesize_list = [] 
        src_filepath = src + '/' + str(dir_num) + '/' + str(dir_num) + '.csv' 
        src_filepath = Path(src_filepath)
        print(src_filepath)
        filesize_list.append(src_filepath)

        if os.path.isfile(src_filepath):
            fsize = os.path.getsize(src_filepath)
            print(fsize)
            filesize_list.append(fsize)
        else:
            print(0)
            filesize_list.append(0)

        writer.writerow(filesize_list)

get_size(src)