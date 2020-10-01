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

ipt = ""
opt = ""

# for test
# ipt = "/Users/k-fukuzawa/Dropbox/tmp/02input/"
ipt = "/Users/k-fukuzawa/Dropbox/tmp/02output/"
# opt = "/Users/k-fukuzawa/Dropbox/tmp/01output/"

#for honnbann
# ipt = sys.argv[1]
# opt = sys.argv[2]

# configparserの宣言とiniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('db_config.ini', encoding='utf-8')

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

def xml_to_csv(ipt):
    p = Path(ipt)
    csv_path = p.glob('**/*.csv')
    for cp in csv_path:
        # with open(cp, newline = '', encoding='cp932') as cpf:
        with open(cp, newline = '', encoding='cp932') as cpf:
            print(cpf)
            read = csv.reader(cpf)#1行ずつ読む
            for row in read:#任意の列をレコードごとにDBへ書き込み

                # マスター関連のDBへのインサート処理はとりあえず実装しない
                # #代理人マスター
                # ##テーブル名の指定と、カラム名で列を指定する。文字列がデータの場合はプレースホルダを単一引用符でくくる
                # #conflictで主キーの重複を上書きする処理で重複回避
                # #代理人がいない場合に"Null"がデータベースに1件レコードして作成されてしまいます。
                # #setsu.exeで"Null"に関する修正する時に注意
                # clm = "INSERT INTO agent_master (agent_ident_number,agent_ident_name) VALUES ('{}','{}') on conflict(agent_ident_number) do update set agent_ident_number = '{}'"
                # clm = clm.format(str(row[28]),str(row[29]),str(row[28]))#csvファイルのデータのうちどの列を指定するか
                # ###書き込み完了処理###
                # cur.execute(clm)
                # connection.commit()

                #公開特許公報出願テーブル
                clm = "INSERT INTO pupa_application_table VALUES(\
                    '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
                    '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
                    '{}','{}'\
                    )"

                #列の挿入
                clm = clm.format(\
                    str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7]), str(row[8]), str(row[9]),\
                    str(row[10]), str(row[11]), str(row[12]), str(row[13]), str(row[14]), str(row[15]), str(row[16]), str(row[17]), str(row[18]), str(row[19]),\
                    str(row[20]), str(row[21]), str(row[22]), str(row[23]), str(row[24]), str(row[25]), str(row[26]), str(row[27]), str(row[28]), str(row[29]),\
                    str(row[30]), str(row[31]), str(row[32]), str(row[33]), str(row[34]), str(row[35]), str(row[36]), str(row[37]), str(row[38]), str(row[39]),\
                    str(row[40]), str(row[41]), str(row[42]), str(row[43]), str(row[44]), str(row[45]), str(row[46]), str(row[47]), str(row[48]), str(row[49]),\
                    str(row[50]), str(row[51])\
                    )
                cur.execute(clm)
                connection.commit()

    cur.close()
    connection.close()

xml_to_csv(ipt)
