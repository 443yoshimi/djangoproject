#!/bin/bash

#処理
#初期設定--------------------------------------------------------

#定義
CMD_MYSQL="mysql -u szi -ppass1234 SZI"
path=/home/SoziAid/import/data/
CSVPATH1=${path}selzsk/selzsk.csv

#処理開始-------------------------------------------------------

#取込ファイル行数カウント
FILECNT1=$(cat ${CSVPATH1} | wc -l)

#ファイル形式変換
nkf -w --overwrite ${CSVPATH1}

#テーブルデータのカウント(インポート前)
MYSQLRES1_BEF=$($CMD_MYSQL -e "SELECT COUNT(*) FROM TIMESALESMEILOG;" -B | tail -n 1)

#取込
$CMD_MYSQL <<EOF
#仕入データ取込
LOAD DATA LOCAL INFILE "${CSVPATH1}"
INTO TABLE TIMESALESMEILOG
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' ESCAPED BY '' LINES TERMINATED BY '\n' IGNORE 1 LINES;
EOF


#テーブルデータのカウント(インポート後)
MYSQLRES1_AFT=$($CMD_MYSQL -e "SELECT COUNT(*) FROM TIMESALESMEILOG;" -B | tail -n 1)

#取込結果出力
#日付
DT=$(date +"%Y%m%d")

#取り込み件数カウント
MYSQLRES1_RESULT=$(( MYSQLRES1_AFT-MYSQLRES1_BEF ))


#echo $DT
echo "$DT 売上取込結果(取込数/取込対象行数): $MYSQLRES1_RESULT / $FILECNT1" >> ${path}imp_result_log.csv

rm -rf ${CSVPATH1}
