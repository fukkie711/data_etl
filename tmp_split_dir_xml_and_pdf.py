import os
import shutil
# import glob
import pathlib

for dvd_num in range(1, 900):
    src_path = 'G:\\pupa\\{}\\'.format(dvd_num)
    #move xml files
    xml_dst_path = src_path + 'xml\\'
    os.makedirs(xml_dst_path, exist_ok=True)
    fname_list = pathlib.Path(src_path).glob('*.xml')
    for src in fname_list:
        print(src)
        shutil.move(str(src), xml_dst_path)
    print('-----------------------------xml done-----------------------------')
    #move pdf files
    pdf_dst_path = src_path + 'pdf\\'
    os.makedirs(pdf_dst_path, exist_ok=True)
    fname_list = pathlib.Path(src_path).glob('*.pdf')
    for src in fname_list:
        print(src)
        shutil.move(str(src), pdf_dst_path)
print('Move Done.')