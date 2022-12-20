# this is for importing xml and pdf files from sources and change xml file encodings from euc-jp to utf-8.
#coding:utf-8

import shutil
import os
import codecs
import sys
import datetime
import pathlib
import time
import glob
from tqdm import tqdm


# from pathlib import Path

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

xml_mode = False
pdf_mode = False
csv_extract_mode = False
for arg in sys.argv:
    if arg == '--xml':
        xml_mode = True
    if arg == '--pdf':
        pdf_mode = True
    if arg == 'csv_extract':
        csv_extract_mode = True

input_dir = pathlib.Path(sys.argv[1])
output_dir = pathlib.Path(sys.argv[2])

def extract_xml(input_dir, output_dir):
    files = os.listdir(input_dir)
    for dir in tqdm(files):
        # if os.path.isdir(dir):
        time.sleep(0.1)
        xml_directory = pathlib.Path('xml')

        # アウトプット先にディレクトリを作成
        os.makedirs(output_dir/dir/xml_directory, exist_ok=True)

        # インプット先からxmlファイルを再帰的に捜査
        xml_files = glob.glob(f'{input_dir/dir}/**/*.xml', recursive=True)
        print(input_dir/dir)
        # xml_files = glob.glob(f'{ dir}/**/*.xml')
        print(f'number of xml_files: {len(xml_files)}')
        for xml_file in tqdm(xml_files):
            shutil.copy2(src=xml_file, dst=output_dir/dir/xml_directory)
    now = datetime.datetime.now()
    print("----------------------------------------")
    print("{0}: {1:%Y/%m/%d %H:%M} .xml copy files done.".format(output_dir, now))
    print("----------------------------------------")

def extract_pdf(input_dir, output_dir):
    start_time = datetime.datetime.now()
    files = os.listdir(input_dir)
    for dir in tqdm(files):
        # if os.path.isdir(dir):
        time.sleep(0.1)
        pdf_directory = pathlib.Path('pdf')

        # アウトプット先にディレクトリを作成
        os.makedirs(output_dir/dir/pdf_directory, exist_ok=True)

        # インプット先からxmlファイルを再帰的に捜査
        pdf_files = glob.glob(f'{input_dir/dir}/**/*.pdf', recursive=True)
        for pdf_file in tqdm(pdf_files):
            shutil.copy2(src=pdf_file, dst=output_dir/dir/pdf_directory)
    finish_time = datetime.datetime.now()
    print("--------------------------------------------------------------------")
    print("{0}: {1:%Y/%m/%d %H:%M} .pdf copy files start.".format(output_dir, finish_time))
    print("{0}: {1:%Y/%m/%d %H:%M} .pdf copy files done.".format(output_dir, finish_time))
    print("--------------------------------------------------------------------")

if xml_mode and pdf_mode:
    print('extract .xml and .pdf')
    extract_xml(input_dir, output_dir)
    extract_pdf(input_dir, output_dir)
elif xml_mode:
    print('extract .xml only')
    extract_xml(input_dir, output_dir)
elif pdf_mode:
    print('extract .pdf only')
    extract_pdf(input_dir, output_dir)
elif csv_extract_mode:
    print('csv_extract_mode')
else:
    print('[USAGE] copy_xml_and_pdf.py src dst [--xml][--pdf][--csv_extract ]')