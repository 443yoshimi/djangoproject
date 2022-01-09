from ..models import Workplan
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import openpyxl
import os
from pathlib import Path
from django.http import HttpResponse
from . import common
from . import sqlquery

# 製造指図書
# グリッドの描画(初期表示、セレクトボックス選択時）
def instruct_load(request):
    
    # 販売実績クラスのインスタンス作成
    ir = instrClass(request)

    dt = ir.instdata_get()

    ir.instdata_cr(dt)


    return JsonResponse(ir.dictlist,safe=False)


class instrClass:
    def __init__(self,request):
        # パラメータの取得
        # 拠点（店舗）
        self.ktn_v = request.GET['ktn']
        # セッション格納
        request.session['s_instkyoten'] = self.ktn_v 

        # 調理方式
        self.ckm_v = request.GET['ckm']
        # セッション格納
        request.session['s_instckm'] = self.ckm_v

        # 商品分類
        self.cat_v = request.GET['hincat']
        # セッション格納
        request.session['s_insthincat'] = self.cat_v 

        # 日付
        self.date_v = request.GET['date'].replace('-','')
        # セッション格納
        request.session['s_instcalender'] = request.GET['date']


    def instdata_get(self):
        # 表示ﾃﾞｰﾀ取得
        # jsonresposeデータ
        cdtdct = {
        'ktn':self.ktn_v,
        'ckm':self.ckm_v,
        'ctg':self.cat_v,
        'date':self.date_v
        }

        # クエリーインスタンス定義
        qr = sqlquery.Instruct_Query(cdtdct)

        # SQL 組み立て
        qr.querycreate()

        # SQL実行
        loaddata = qr.query_execute()

        return loaddata

    def instdata_cr(self,data):
        
        # 0:id 1:sskcd 2:ktncd 3:ckmcd 4:catcd 5:hincd 6:hinnm 7:callcd 
        # 8:size 9:tray 10:baitnk 11:gozen 12:hradd 13:ggadd 14:tsadd
        # 辞書変換
        self.dictlist = []

        for row in data:
            # 合計数量
            gokeisu = row[11] + row[12] + row[13] + row[14]
            # 合計金額
            gokeibaik = gokeisu * row[10]
            # 辞書リストの作成
            #{key:1,callhin:74,hincd:'0291735500000',hinnm:'鉄板巻上げ玉子焼き入り太巻寿司',spec:'中',baik:498,
            #tray:'OSAパック13',prod1:6,prod2:3,prod3:2,prod4:0,gokei:11,sum:5478},
            self.dictlist.append({
                'key':row[0],
                'callhin':row[7],
                'hincd':row[5],
                'hinnm':row[6],
                'spec':row[8],
                'baik':row[10],
                'tray':row[9],
                'prod1':row[11],
                'prod2':row[12],
                'prod3':row[13],
                'prod4':row[14],
                'gokei':gokeisu,
                'sum':gokeibaik
                })
        


# データ更新
@csrf_exempt
def instruct_update(request, *args, **kwargs):
    
    key = request.GET['key']
    prod1 = request.GET['prod1']
    prod2 = request.GET['prod2']
    prod3 = request.GET['prod3']
    prod4 = request.GET['prod4']

    try:
        sisztrn = Workplan.objects.get(id=key)
        sisztrn.gozen = prod1
        sisztrn.hradd = prod2
        sisztrn.ggadd = prod3
        sisztrn.tsadd = prod4
        sisztrn.save()

        message = "正常終了"
        status_code = 200
    except Exception as e:
        message =  e.message
        status_code = 500

    response = JsonResponse({'status':'true','message':message})
    response.status_code = status_code

    return response


def excell_outlayout(exel_header,instruct_list):
    # テンプレートファイルの読み込み
    staticpath = os.path.join(Path(__file__).resolve().parent.parent.parent, "static")
    wb = openpyxl.load_workbook(os.path.join(staticpath, "download/instructformat.xlsx"))

    sheet = wb['Sheet1']

    # 日付
    sheet['J2'] = exel_header['date']
    # 店舗、調達方法、カテゴリ
    sheet['A4'] = exel_header['ten'] + "、" + exel_header['ckm'] + "、" + exel_header['cat']
    
    exel_header['gokei'] = 0
    
    for i,row in enumerate(instruct_list):
        # 品番
        sheet['B' + str(i+7)] = row['callhin']
        # 商品名
        sheet['C' + str(i+7)] = row['hinnm']
        # 内容量
        sheet['D' + str(i+7)] = row['spec']

        if row['spec'] == '中':
            num = 2
        elif row['spec'] == '大':
            num = 3
        else:
            num = 1
        # 本体価格（小：売価×1　中：売価×2　大：売価×3）
        sheet['E' + str(i+7)] = num * int(row['baik'])
        # トレー
        sheet['F' + str(i+7)] = row['tray']
        # 朝一
        sheet['G' + str(i+7)] = row['prod1']
        # 朝二
        sheet['H' + str(i+7)] = row['prod2']
        # 午後一
        sheet['I' + str(i+7)] = row['prod3']
        # 午後二
        sheet['J' + str(i+7)] = row['prod4']
        # 合計を足し合わせ
        exel_header['gokei'] += int(row['sum'])
    
    # 合計金額
    sheet['J4'] = "{:,.1f}".format(exel_header['gokei'] / 1000)

    # 調整行数
    # 1000行 - ヘッダー - 1ページあたり行数
    delrow = 1000 - 6 - 25

    # 行数削除 7～31 25行
    if len(instruct_list) < 26:
        # 25行以内の場合
        
        sheet.delete_rows(32, delrow)
    else:
        sheet.delete_rows(32 + (len(instruct_list) - 25), delrow - ((len(instruct_list) - 25)))
        
    return wb

@csrf_exempt
def instruct_excellout(request):

    # jsonデータの取り出し
    for row in request.POST:
        instruct_list = json.loads(row)

    exel_header = {}
    if instruct_list[0]['date'] != '':
        # 日付クラスのインスタンス作成
        dtcmn = common.DateCalccmn(instruct_list[0]['date'].replace('年','-').replace('月','-').replace('日',''))
        # 日付
        exel_header['date'] = dtcmn.dateformcnv1() + '(' + dtcmn.yobiget() + ')'
    else:
        # 日付
        exel_header['date'] = ''

    # カテゴリー
    exel_header['cat'] = instruct_list[1]['cat']
    # 調達方法
    exel_header['ckm'] = instruct_list[2]['ckm']
    # 店舗
    exel_header['ten'] = instruct_list[3]['ten']

    # 日付、カテゴリー、調達方法、店舗の削除
    for i in range(4):
        instruct_list.pop(0)

    # エクセル作成    
    wb = excell_outlayout(exel_header,instruct_list)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'report.xlsx'

    # データの書き込みを行なったExcelファイルを保存する
    wb.save(response)

    # 生成したHttpResponseをreturnする
    return response
