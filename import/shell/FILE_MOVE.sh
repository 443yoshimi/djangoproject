#!/bin/bash
#処理
#初期設定--------------------------------------------------------

#定義
selzsk_filename=selzsk.csv
haiki_filename=haikizsk.csv
hin_filename=SSBMST.csv

pathfrom=/home/SeizoKanri/DATA/
hin_pathfrom=${pathfrom}MST/impmst/
haiki_pathfrom=${pathfrom}TRAN/
selzsk_pathfrom=${pathfrom}TRAN/

pathto=/home/SoziAid/import/data/
hin_pathto=${pathto}hin/
haiki_pathto=${pathto}haiki/
selzsk_pathto=${pathto}selzsk/

#処理開始-------------------------------------------------------

cp ${hin_pathfrom}${hin_filename} ${hin_pathto}${hin_filename}
cp ${haiki_pathfrom}${haiki_filename} ${haiki_pathto}${haiki_filename}
cp ${selzsk_pathfrom}${selzsk_filename} ${selzsk_pathto}${selzsk_filename}
