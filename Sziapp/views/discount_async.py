from typing_extensions import ParamSpec
from django.db.models.query_utils import Q
from django.core.serializers import serialize
from django.http.response import JsonResponse
from . import sqlquery
from django.views.decorators.csrf import csrf_exempt
from . import common

# 値下げ管理表
# グリッドの描画(初期表示、セレクトボックス選択時）
def instruct_load(request):
    
    # 値下げ管理表クラスのインスタンス作成
    dc = disCountClass(request)

    # 表示ﾃﾞｰﾀ取得
    dt = dc.dcdata_get()

    # ソート
    dt = dc.dcdata_sort(dt)

    # データ集計
    dc.dcdata_syukei(dt)

    # 表示ﾃﾞｰﾀ作成２(データフォーマット変更)
    dc.dcdata_cr()

    return JsonResponse(dc.dcdictlist,safe=False)

class disCountClass:
    def __init__(self,request):
        self.Syukeilist = []

        # パラメータの取得
        # 拠点（店舗）
        # 空白（初期表示）の場合、ログインユーザの店コードを選択
        self.ktn_v = '99999' if request.GET['ktn']  == '' else request.GET['ktn']
        # セッション格納
        request.session['s_kyoten'] = self.ktn_v

        # 調理方式
        # 空白（初期表示）の場合、インストアを選択
        self.ckm_v = '1' if request.GET['ckm'] == '' else request.GET['ckm']
        # セッション格納
        request.session['s_ckm'] = self.ckm_v

        # 商品
        self.hin_v = request.GET['hin']
        # セッション格納
        request.session['s_hintb'] = self.hin_v
        
        # 日付FROM
        self.dateFROM_v = request.GET['datef']
        # セッション格納
        request.session['s_salesdatefrom'] = self.dateFROM_v

        # 日付TO
        self.dateTO_v = request.GET['datet']
        # セッション格納
        request.session['s_salesdateto'] = self.dateTO_v

    def dcdata_get(self):
        # 表示ﾃﾞｰﾀ取得
        # jsonresposeデータ
        cdtdct = {
        'ckm':self.ckm_v,
        'hin':self.hin_v,
        'ktn':self.ktn_v,
        'dtf':self.dateFROM_v,
        'dtt':self.dateTO_v,
        'bmn':'77'
        }

        # クエリーインスタンス定義
        qd = sqlquery.Discount_Query(cdtdct)

        # SQL 組み立て
        qd.querycreate()

        # SQL実行
        loaddata = qd.query_execute()

        return loaddata

    def dcdata_syukei(self,data):
        # 同一商品 かつ 小・中・大ごとに販売金額、値引き金額を計算する
        # 小区分が入っていない場合は、小・中・大を考慮しない
        
        # フォーマット
        # JANコード1、JANコード2、商品名、売上点数、売上金額、値引き金額、小区分
        # ↓
        # 0:JANコード、1:商品名、2:分類、3:値下金額合計、4:値下金額合計最大、5:値下率

        # 値下率(平均値下げ率) = 期間内の、値下金額合計÷(値下金額合計+売上金額合計)

        jancd = bunruistr = bunruistr_bk = hinname = ''
        Syukeilist_tmp = []
        # 集計金額をリセット
        syukeidict = disCountClass.dcdata_sumkng_reset()
        for i,row in enumerate(data):
            # 大中小判定
            bunruistr = common.syokbnstr_hantei(row[6],row[4]/row[3])
            
            # 同一商品判定
            # JANコードが同じかつ分類が同じ　または 初回
            if ((jancd == row[0]) and (bunruistr == bunruistr_bk)) or (i == 0):
                # 販売金額合計、値下げ金額合計を更新
                syukeidict = disCountClass.dcdata_kngsum(syukeidict,row)
            else:
                # 値下げ率が0%でない場合、リスト追加
                Syukeilist_tmp = disCountClass.dcdata_listappend(jancd,hinname,bunruistr_bk,syukeidict,Syukeilist_tmp)
                
                # 集計金額をリセット
                syukeidict = disCountClass.dcdata_sumkng_reset()
                # 販売金額合計、値下げ金額合計を更新
                syukeidict = disCountClass.dcdata_kngsum(syukeidict,row)

            if i == len(data) -1:
                # 最終行の場合
                # 値下げ率が0%でない場合、リスト追加
                Syukeilist_tmp = disCountClass.dcdata_listappend(jancd,hinname,bunruistr_bk,syukeidict,Syukeilist_tmp)

            bunruistr_bk = bunruistr
            jancd = row[0]
            hinname = row[2]
    

        # 最大値取得
        max_v = 0
        for row in Syukeilist_tmp:
            if max_v < int(row[3]):
                max_v = row[3]

        # 最大値をリストに追加
        # 0:JANコード、1:商品名、2:分類、3:値下金額合計、4:値下率、5:値下金額合計最大
        tmplst = []
        for row in Syukeilist_tmp:
            tmplst = list(row)
            tmplst.append(max_v)
            self.Syukeilist.append(tmplst)

    def dcdata_listappend(jancd,hinname,bunruistr_bk,syukeidict,Syukeilist_):

        # 値下げ率を計算
        #nesageritu = round((abs(syukeidict['sagekng']) / (syukeidict['saleskngsum'] + abs(syukeidict['sagekng']))*100),2)
        nesageritu = round((abs(syukeidict['sagekng']) / (syukeidict['saleskngsum'] )*100),2)

        # 値下げ率が0%より大きいか場合、リストに追加
        if nesageritu > 0:
            # 0:JANコード、1:商品名、2:分類、3:値下金額合計、4:値下率
            Syukeilist_.append([jancd,hinname,bunruistr_bk,abs(syukeidict['sagekng']),nesageritu])

        return Syukeilist_

    def dcdata_sumkng_reset():
        syukeidict = {
            'sagekng':0,
            'saleskngsum':0
        }
        return syukeidict

    def dcdata_kngsum(syukeidict,row):
        # 販売金額合計、値下げ金額合計を更新
        syukeidict.update(
            {
                'sagekng': syukeidict['sagekng'] + row[5],
                'saleskngsum': syukeidict['saleskngsum'] + row[4]
            }
        )
        
        return syukeidict

    def dcdata_sort(self,dt):
        # ライン、クラス、JANコード、JANコード2の昇順にソート
        sorted_data = sorted(dt, key=lambda x:(x[7], x[8],x[0],x[1]))

        return sorted_data


    def dcdata_cr(self):
        self.dcdictlist = []

        # 0:JANコード、1:商品名、2:分類、3:値下金額合計、4:値下率、5:値下金額合計最大
        for row in self.Syukeilist:
            # 値下金額
            # 値下金額合計,値下金額合計最大
            nsgkng = str(row[3]) + "," + str(row[5])
            # 商品情報
            # 商品名,JANコード,分類
            hininfo = str(row[1]) + "," + str(row[0]) + "," + str(row[2])
            # 値下げ率
            nsgritu = str(row[4])

            # 辞書リストの作成
            self.dcdictlist.append({
                'nesagekng':nsgkng,'hin':hininfo,'nesageritu':nsgritu
                })