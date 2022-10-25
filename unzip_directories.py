import glob
import re
import os
import time
import zipfile
import datetime
import pathlib
import shutil
from tqdm import tqdm

input_dir = pathlib.Path("C:/tmp_from/") #コピー元
output_dir = pathlib.Path("C:/tmp_to/") #コピー先

def unzip_directories(input_dir, output_dir):
    zip_files = glob.glob(f'{input_dir}/*.zip')
    # print(zip_files)
    for zip_file in zip_files:
        print(zip_file)
        with zipfile.ZipFile(zip_file) as zf:
            zf.extractall(os.path.dirname(zip_file))
            time.sleep(0.5)

def copy_xml_and_chg_ipt_codec(input_dir, output_dir):
    # ipt_path = Path(ipt)
    # opt_path = Path(opt)
    xml_files = glob.glob(f'{input_dir}/**/*.xml')
    print(xml_files)
    for xml_file in tqdm(xml_files):
        output_file_path = str(output_dir) + "/" + str(os.path.basename(os.path.dirname(xml_file)) + "/" + "xml") 
        os.makedirs(output_file_path, exist_ok=True)
        output_filename = output_file_path + "/" + str(pathlib.Path(xml_file).name)
        print(pathlib.Path(output_filename))
        with open(output_filename, 'w', encoding='utf_8') as f_out:
            with open(xml_file, encoding='euc_jp') as f_in:
                # 下記はxmlからcsvに変換する際に、euc-jpの記載があると「マルチバイト文字列は使えません」みたいなエラーが出て進まないのでやむを得ず外科手術を行った結果がこれである…
                f_out.write(f_in.read().replace('<?xml version="1.0" encoding="EUC-JP"?>', '<?xml version="1.0" encoding="UTF-8"?>'))
        time.sleep(0.05)

def copy_pdf(input_dir, output_dir): #copy pdf file
    pdf_files = glob.glob(f'{input_dir}/**/*.pdf')
    for pdf_file in tqdm(pdf_files):
        output_file_path = str(output_dir) + "/" + str(os.path.basename(os.path.dirname(pdf_file)) + "/" + "pdf") 
        os.makedirs(output_file_path, exist_ok=True)
        output_filename = output_file_path + "/" + str(pathlib.Path(pdf_file).name)
        print(pathlib.Path(output_filename))
        shutil.copyfile(pdf_file, output_filename)
        time.sleep(0.05)


unzip_directories(input_dir, output_dir)
copy_xml_and_chg_ipt_codec(input_dir, output_dir)
copy_pdf(input_dir, output_dir)


# now = datetime.datetime.now()
# print("----------------------------------------")
# print("{0}: {1:%Y/%m/%d %H:%M} xml copy files done.".format(opt_path, now))
# print("----------------------------------------")
# with open(str(opt_path) + '/' + '_output_result.txt', 'a', encoding='utf_8') as f_out:
#     f_out.write("{0}: {1:%Y/%m/%d %H:%M} xml copy files done.\n".format(opt_path, now))

# copy_pdf(ipt, opt)
# now = datetime.datetime.now()
# print("----------------------------------------")
# print("{0}: {1:%Y/%m/%d %H:%M} pdf copy files done.".format(opt_path, now))
# print("----------------------------------------")
# with open(str(opt_path) + '/' + '_output_result.txt', 'a', encoding='utf_8') as f_out:
#     f_out.write("{0}: {1:%Y/%m/%d %H:%M} pdf copy files done.\n".format(opt_path, now))