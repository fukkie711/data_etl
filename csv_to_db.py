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

src = ""
ipt = ""
opt = ""

# for test
src = "/Users/kazuh/Dropbox/tmp/02input/"
# ipt = "/Users/kazuh/Dropbox/tmp/02output/"
# opt = "/Users/k-fukuzawa/Dropbox/tmp/01output/"

#for honnbann
# ipt = sys.argv[1])
# opt = sys.argv[2])

# configparserの宣言とiniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('../ini/db_config.ini', encoding='utf-8')

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
    p = Path(src)
    csv_path = p.glob('**/*.csv')
    for cp in csv_path:
        # with open(cp, newline = '', encoding='cp932') as cpf:
        with open(cp, newline = '', encoding='cp932') as cpf:
            print(cpf)
            read = csv.reader(cpf)#1行ずつ読む
            for row in read:#任意の列をレコードごとにDBへ書き込み
                # マスター関連のDBへのインサート処理はとりあえず実装しない

                ##公開特許公報出願テーブル
                # pupa_application_basic_info
                clm = "INSERT INTO pupa_application_basic_info VALUES(\
                    '{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}',\
                    '{}','{}'\
                    )"
                #列の挿入
                clm = clm.format(\
                    str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[2]).replace("'", "''"), str(row[3]).replace("'", "''"), str(row[4]).replace("'", "''"),\
                    str(row[5]).replace("'", "''"), str(row[6]).replace("'", "''"), str(row[7]).replace("'", "''"), str(row[8]).replace("'", "''"), str(row[9]).replace("'", "''"),\
                    str(row[10]).replace("'", "''"), str(row[11]).replace("'", "''"), str(row[12]).replace("'", "''"), str(row[13]).replace("'", "''"), str(row[14]).replace("'", "''"),\
                    str(row[15]).replace("'", "''"), str(row[16]).replace("'", "''"), str(row[29]).replace("'", "''"), str(row[30]).replace("'", "''"), str(row[39]).replace("'", "''"),\
                    str(row[40]).replace("'", "''"), str(row[59]).replace("'", "''")\
                    )
                cur.execute(clm)
                connection.commit()
                
                # 公開特許公報出願人情報
                # pupa_applicant_info
                clm = "INSERT INTO pupa_applicant_info VALUES(\
                    '{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}',\
                    '{}','{}','{}'\
                    )"
                #列の挿入
                clm = clm.format(\
                    str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[3]).replace("'", "''"), str(row[14]).replace("'", "''"), str(row[15]).replace("'", "''"),\
                    str(row[16]).replace("'", "''"), str(row[17]).replace("'", "''"), str(row[18]).replace("'", "''"), str(row[19]).replace("'", "''"), str(row[20]).replace("'", "''"),\
                    str(row[21]).replace("'", "''"), str(row[22]).replace("'", "''"), str(row[23]).replace("'", "''"), str(row[24]).replace("'", "''"), str(row[25]).replace("'", "''"),\
                    str(row[26]).replace("'", "''"), str(row[27]).replace("'", "''"), str(row[28]).replace("'", "''")\
                    )
                cur.execute(clm)
                connection.commit()

                # 公開特許公報代理人情報
                # pupa_agent_info
                clm = "INSERT INTO pupa_agent_info VALUES(\
                    '{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}',\
                    '{}','{}','{}'\
                    )"
                #列の挿入
                clm = clm.format(\
                    str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[3]).replace("'", "''"), str(row[29]).replace("'", "''"), str(row[30]).replace("'", "''"),\
                    str(row[31]).replace("'", "''"), str(row[31]).replace("'", "''"), str(row[33]).replace("'", "''"), str(row[34]).replace("'", "''"), str(row[35]).replace("'", "''"),\
                    str(row[36]).replace("'", "''"), str(row[37]).replace("'", "''"), str(row[38]).replace("'", "''")\
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
                    '{}','{}','{}'\
                    )"
                #列の挿入
                clm = clm.format(\
                    str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[3]).replace("'", "''"), str(row[39]).replace("'", "''"), str(row[40]).replace("'", "''"),\
                    str(row[41]).replace("'", "''"), str(row[42]).replace("'", "''"), str(row[43]).replace("'", "''"), str(row[44]).replace("'", "''"), str(row[45]).replace("'", "''"),\
                    str(row[46]).replace("'", "''"), str(row[47]).replace("'", "''"), str(row[48]).replace("'", "''"), str(row[49]).replace("'", "''"), str(row[50]).replace("'", "''"),\
                    str(row[51]).replace("'", "''"), str(row[52]).replace("'", "''"), str(row[53]).replace("'", "''"), str(row[54]).replace("'", "''"), str(row[55]).replace("'", "''"),\
                    str(row[56]).replace("'", "''"), str(row[57]).replace("'", "''"), str(row[58]).replace("'", "''")\
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
                    str(row[0]).replace("'", "''"), str(row[1]).replace("'", "''"), str(row[3]).replace("'", "''"),  str(row[60]).replace("'", "''"), str(row[61]).replace("'", "''"),\
                    str(row[62]).replace("'", "''"), str(row[63]).replace("'", "''"), str(row[64]).replace("'", "''"), str(row[65]).replace("'", "''"), str(row[66]).replace("'", "''"),\
                    str(row[67]).replace("'", "''"), str(row[68]).replace("'", "''"), str(row[69]).replace("'", "''"), str(row[70]).replace("'", "''")\
                    )
                # print(clm)
                cur.execute(clm)
                connection.commit()

    cur.close()
    connection.close()

xml_to_csv(src)
print('done.')
