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
    for dir_num in range(1, 900):
        src_path = src + '/' + str(dir_num) 
        src_path = Path(src_path)
        print(src_path)
        csv_path = src_path.glob('**/*.csv')
        for cp in csv_path:
            # with open(cp, newline = '', encoding='cp932') as cpf:
            with open(cp, newline = '', encoding='cp932') as cpf:
                print(cpf)
                read = csv.reader(cpf)#1行ずつ読む
                for row in read:#任意の列をレコードごとにDBへ書き込み
                    # マスター関連のDBへのインサート処理はとりあえず実装しない

                    # 請求項の数と全ページ数にNoneが入っている場合の対応
                    # 再公表などはページ数が入っていない？
                    if row[9] == 'None': row[9] = -1
                    if row[10] == 'None': row[10] = -1

                    ##公開特許公報出願テーブル
                    # pupa_application_basic_info
                    clm = "INSERT INTO pupa_application_basic_info VALUES(\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}'\
                        )"
                    #列の挿入
                    clm = clm.format(\
                        # 公開種別(jp)、公開種別(st16)、公開種別、公開番号
                        str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[2]).replace("'", "''"), str(row[3]).replace("'", "''"),\
                        # 公開日、出願番号、出願日、
                        str(row[4]).replace("'", "''"), str(row[5]).replace("'", "''"), str(row[6]).replace("'", "''"),\
                        # 発明の名称、国際特許分類、
                        str(row[7]).replace("'", "''"), str(row[8]).replace("'", "''"),\
                        # 請求項の数＆頁数（replaceしない）
                        row[9], row[10],\
                        # FI, テーマコード, Fターム
                        str(row[11]).replace("'", "''"), str(row[12]).replace("'", "''"), str(row[13]).replace("'", "''"),\
                        # 出願人1
                        str(row[14]).replace("'", "''"), str(row[15]).replace("'", "''"), str(row[16]).replace("'", "''"),\
                        # 出願人2
                        str(row[17]).replace("'", "''"), str(row[18]).replace("'", "''"), str(row[19]).replace("'", "''"),\
                        # 代理人1
                        str(row[50]).replace("'", "''"), str(row[51]).replace("'", "''"),\
                        # 発明者1
                        str(row[74]).replace("'", "''"), str(row[75]).replace("'", "''"),\
                        # 要約
                        str(row[98]).replace("'", "''")
                        )
                    cur.execute(clm)
                    connection.commit()
                
                    # 公開特許公報出願人情報
                    # pupa_applicant_info
                    clm = "INSERT INTO pupa_applicant_info VALUES(\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}'\
                        )"
                    #列の挿入
                    clm = clm.format(\
                        # 公開種別(jp)、公開種別(st16)、公開番号
                        str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[3]).replace("'", "''"),\
                        # 出願人1～出願人12の情報
                        str(row[14]).replace("'", "''"), str(row[15]).replace("'", "''"), str(row[16]).replace("'", "''"),\
                        str(row[17]).replace("'", "''"), str(row[18]).replace("'", "''"), str(row[19]).replace("'", "''"),\
                        str(row[20]).replace("'", "''"), str(row[21]).replace("'", "''"), str(row[22]).replace("'", "''"),\
                        str(row[23]).replace("'", "''"), str(row[24]).replace("'", "''"), str(row[25]).replace("'", "''"),\
                        str(row[26]).replace("'", "''"), str(row[27]).replace("'", "''"), str(row[28]).replace("'", "''"),\
                        str(row[29]).replace("'", "''"), str(row[30]).replace("'", "''"), str(row[31]).replace("'", "''"),\
                        str(row[32]).replace("'", "''"), str(row[33]).replace("'", "''"), str(row[34]).replace("'", "''"),\
                        str(row[35]).replace("'", "''"), str(row[36]).replace("'", "''"), str(row[37]).replace("'", "''"),\
                        str(row[38]).replace("'", "''"), str(row[39]).replace("'", "''"), str(row[40]).replace("'", "''"),\
                        str(row[41]).replace("'", "''"), str(row[42]).replace("'", "''"), str(row[43]).replace("'", "''"),\
                        str(row[44]).replace("'", "''"), str(row[45]).replace("'", "''"), str(row[46]).replace("'", "''"),\
                        str(row[47]).replace("'", "''"), str(row[48]).replace("'", "''"), str(row[49]).replace("'", "''")\
                        )
                    cur.execute(clm)
                    connection.commit()

                    # 公開特許公報代理人情報
                    # pupa_agent_info
                    clm = "INSERT INTO pupa_agent_info VALUES(\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}'\
                        )"
                    #列の挿入
                    clm = clm.format(\
                        # 公開種別(jp)、公開種別(st16)、公開番号
                        str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[3]).replace("'", "''"),\
                        str(row[50]).replace("'", "''"), str(row[51]).replace("'", "''"),\
                        str(row[52]).replace("'", "''"), str(row[53]).replace("'", "''"),\
                        str(row[54]).replace("'", "''"), str(row[55]).replace("'", "''"),\
                        str(row[56]).replace("'", "''"), str(row[57]).replace("'", "''"),\
                        str(row[58]).replace("'", "''"), str(row[59]).replace("'", "''"),\
                        str(row[60]).replace("'", "''"), str(row[61]).replace("'", "''"),\
                        str(row[62]).replace("'", "''"), str(row[63]).replace("'", "''"),\
                        str(row[64]).replace("'", "''"), str(row[65]).replace("'", "''"),\
                        str(row[66]).replace("'", "''"), str(row[67]).replace("'", "''"),\
                        str(row[68]).replace("'", "''"), str(row[69]).replace("'", "''"),\
                        str(row[70]).replace("'", "''"), str(row[71]).replace("'", "''"),\
                        str(row[72]).replace("'", "''"), str(row[73]).replace("'", "''")\
                        )
                    cur.execute(clm)
                    connection.commit()

                    # 公開特許公報発明者情報
                    # pupa_inventor_info
                    clm = "INSERT INTO pupa_inventor_info VALUES(\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}',\
                        '{}','{}'\
                        )"
                    #列の挿入
                    clm = clm.format(\
                        # 公開種別(jp)、公開種別(st16)、公開番号
                        str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[3]).replace("'", "''"),\
                        str(row[74]).replace("'", "''"), str(row[75]).replace("'", "''"),\
                        str(row[76]).replace("'", "''"), str(row[77]).replace("'", "''"),\
                        str(row[78]).replace("'", "''"), str(row[79]).replace("'", "''"),\
                        str(row[80]).replace("'", "''"), str(row[81]).replace("'", "''"),\
                        str(row[82]).replace("'", "''"), str(row[83]).replace("'", "''"),\
                        str(row[84]).replace("'", "''"), str(row[85]).replace("'", "''"),\
                        str(row[86]).replace("'", "''"), str(row[87]).replace("'", "''"),\
                        str(row[88]).replace("'", "''"), str(row[89]).replace("'", "''"),\
                        str(row[90]).replace("'", "''"), str(row[91]).replace("'", "''"),\
                        str(row[92]).replace("'", "''"), str(row[93]).replace("'", "''"),\
                        str(row[94]).replace("'", "''"), str(row[95]).replace("'", "''"),\
                        str(row[96]).replace("'", "''"), str(row[97]).replace("'", "''")
                        )
                    cur.execute(clm)
                    connection.commit()


                    # 公開特許公報文書情報
                    # pupa_text_info
                    clm = "INSERT INTO pupa_text_info VALUES(\
                        '{}', '{}', '{}', '{}', '{}',\
                        '{}', '{}', '{}', '{}', '{}',\
                        '{}', '{}', '{}', '{}'\
                        )"
                    clm = clm.format(\
                        # 公開種別(jp)、公開種別(st16)、公開番号
                        str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[3]).replace("'", "''"),\
                        str(row[99]).replace("'", "''"), str(row[100]).replace("'", "''"),\
                        str(row[101]).replace("'", "''"), str(row[102]).replace("'", "''"),\
                        str(row[103]).replace("'", "''"), str(row[104]).replace("'", "''"),\
                        str(row[105]).replace("'", "''"), str(row[106]).replace("'", "''"),\
                        str(row[107]).replace("'", "''"), str(row[108]).replace("'", "''"),\
                        str(row[109]).replace("'", "''")\
                        )
                    # print(clm)
                    cur.execute(clm)
                    connection.commit()

xml_to_csv(src)
cur.close()
connection.close()

print('done.')
