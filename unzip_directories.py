import glob
import os
import sys
import time
import zipfile
import datetime
import pathlib
from tqdm import tqdm

# テスト用
# input_dir = pathlib.Path("C:/tmp_from/") #コピー元
# output_dir = pathlib.Path("C:/tmp_to/") #コピー先

# 本番用（コマンドライン引数でインプットとアウトプットを指定
if len(sys.argv) < 2:
      print("インプットディレクトリを入力してください")
      sys.exit()
if len(sys.argv) < 3:
      print("アウトプットディレクトリを入力してください")
      sys.exit()

input_dir = pathlib.Path(sys.argv[1])
output_dir = pathlib.Path(sys.argv[2])

def unzip_directories(input_dir, output_dir):
    zip_files = glob.glob(f'{input_dir}/*.zip')
    # print(zip_files)
    for zip_file in tqdm(zip_files):
        print(zip_file)
        now = datetime.datetime.now()
        print(f'extract time:{now}')
        with zipfile.ZipFile(zip_file) as zf:
            extract_path =  os.path.splitext(os.path.basename(zip_file))[0]

            try:
                zf.extractall(path=output_dir/extract_path)
                time.sleep(0.5)
            except zipfile.BadZipFile:
                continue

unzip_directories(input_dir, output_dir)
now = datetime.datetime.now()
print("----------------------------------------")
print("{0}: {1:%Y/%m/%d %H:%M} xml copy files done.".format(output_dir, now))
print("----------------------------------------")
with open(str(output_dir) + '/' + '_output_result.txt', 'a', encoding='utf_8') as f_out:
    f_out.write("{0}: {1:%Y/%m/%d %H:%M} extract zipfiles done.\n".format(output_dir, now))

# def copy_xml_and_chg_ipt_codec(input_dir, output_dir):
#     # ipt_path = Path(ipt)
#     # opt_path = Path(opt)
#     xml_files = glob.glob(f'{input_dir}/**/*.xml')
#     print(xml_files)
#     for xml_file in tqdm(xml_files):
#         output_file_path = str(output_dir) + "/" + str(os.path.basename(os.path.dirname(xml_file)) + "/" + "xml") 
#         os.makedirs(output_file_path, exist_ok=True)
#         output_filename = output_file_path + "/" + str(pathlib.Path(xml_file).name)
#         print(pathlib.Path(output_filename))
#         with open(output_filename, 'w', encoding='utf_8') as f_out:
#             with open(xml_file, encoding='euc_jp') as f_in:
#                 # 下記はxmlからcsvに変換する際に、euc-jpの記載があると「マルチバイト文字列は使えません」みたいなエラーが出て進まないのでやむを得ず外科手術を行った結果がこれである…
#                 f_out.write(f_in.read().replace('<?xml version="1.0" encoding="EUC-JP"?>', '<?xml version="1.0" encoding="UTF-8"?>'))
#         time.sleep(0.1)
# def copy_pdf(ipt, opt): #copy pdf file
#     ipt_path = Path(ipt)
#     opt_path = Path(opt)
#     pdf_path = ipt_path.glob('**/*.pdf')
#     for i in pdf_path:
#         print(opt_path, i.name )
#         shutil.copyfile(i, str(opt_path) + '/' + i.name)


# copy_xml_and_chg_ipt_codec(input_dir, output_dir)

# copy_pdf(ipt, opt)
# now = datetime.datetime.now()
# print("----------------------------------------")
# print("{0}: {1:%Y/%m/%d %H:%M} pdf copy files done.".format(opt_path, now))
# print("----------------------------------------")
# with open(str(opt_path) + '/' + '_output_result.txt', 'a', encoding='utf_8') as f_out:
#     f_out.write("{0}: {1:%Y/%m/%d %H:%M} pdf copy files done.\n".format(opt_path, now))