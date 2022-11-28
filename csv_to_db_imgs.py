#coding:utf-8
import os
import sys
import csv
import psycopg2
from pathlib import Path
import pathlib
import glob
import logging
import configparser

maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

src = ""
ipt = ""
opt = ""

# for test
# src = "/Users/kazuh/Dropbox/tmp/02input/"
src = "D:\\patent_db\\pupa"
# ipt = "/Users/kazuh/Dropbox/tmp/02output/"
# opt = "/Users/k-fukuzawa/Dropbox/tmp/01output/"

#for honnbann
# ipt = sys.argv[1])
# opt = sys.argv[2])

# configparserの宣言とiniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('../init/db_config.ini', encoding='utf-8')

# config,iniから値取得
host = config_ini['DEFAULT']['host']
port = config_ini['DEFAULT']['port']
dbname = config_ini['DEFAULT']['dbname']
user = config_ini['DEFAULT']['user']
password = config_ini['DEFAULT']['password']

conText = "host={} port={} dbname={} user={} password={}"
conText = conText.format(host, port, dbname, user, password)
connection = psycopg2.connect(conText)
connection.get_backend_pid()
cur = connection.cursor()

def xml_to_csv(src):
    # p = Path(ipt)
    for dir_num in range(2, 999):
        src_path = src + '/' + str(dir_num) 
        src_path = Path(src_path)
        print(src_path)
        csv_path = src_path.glob('**/*_num_of_imgs.csv')
        for cp in csv_path:
            # with open(cp, newline = '', encoding='cp932') as cpf:
            with open(cp, newline = '', encoding='cp932') as cpf:
                print(cpf)
                read = csv.reader(cpf)#1行ずつ読む
                for row in read:#任意の列をレコードごとにDBへ書き込み
                    # マスター関連のDBへのインサート処理はとりあえず実装しない

                    # 請求項の数と全ページ数にNoneが入っている場合の対応
                    # 再公表などはページ数が入っていない？
                    # if row[9] == 'None': row[9] = -1
                    # if row[10] == 'None': row[10] = -1

                    ##画像数テーブル
                    # pupa_number_of_images
                    # 20211019ユニークキー制約付加。それに伴いユニークキーがかぶった際にUPSERT（上書き）する処理を追加。最終情報がInsertされることになる
                    clm = "INSERT INTO pupa_number_of_images (publication_number, number_of_images)\
                        VALUES('{}','{}')\
                        ON CONFLICT (publication_number)\
                        DO UPDATE SET number_of_images='{}'"
                    #列の挿入
                    clm = clm.format(\
                        # 公開種別(jp)、公開種別(st16)、公開種別、公開番号
                        str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[1]).replace("'", "''")
                        )
                    cur.execute(clm)
                    connection.commit()
                
                    # print(clm)
                    cur.execute(clm)
                    connection.commit()

xml_to_csv(src)
cur.close()
connection.close()

print('done.')
