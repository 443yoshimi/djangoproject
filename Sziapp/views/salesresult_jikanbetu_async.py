from typing_extensions import ParamSpec
from django.db.models.query_utils import Q
from django.core.serializers import serialize
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from Sziapp.views.salesresult_async import salesRClass
from . import sqlquery
from . import common
import pandas as pd
#　販売実績一覧表
# グリッドの描画(初期表示、セレクトボックス選択時）
def salesresultjikanbetu_load(request):

    # 販売実績クラスのインスタンス作成
    sjb = salesJBClass(request)

    # 表示ﾃﾞｰﾀ取得
    dt = sjb.sjdata_get()

    # 表示ﾃﾞｰﾀ集計1
    dt = sjb.sjdata_syukei1(dt)

    sjb.sjdata_cr(dt)
            
    return JsonResponse(sjb.dictlist,safe=False)

class salesJBClass:
    def __init__(self,request):
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

        # 曜日チェックボックス
        self.ybckl_v = request.GET['ybckl']
       # セッション格納
        request.session['s_sjbyobinum'] = self.ybckl_v

        # 部門
        self.bmn = '77'

        self.dictlist = []

    def sjdata_get(self):
        # 表示ﾃﾞｰﾀ取得
        # jsonresposeデータ
        cdtdct = {
        'ktn':self.ktn_v,
        'ckm':self.ckm_v,
        'hin':self.hin_v,
        'dtf':self.dateFROM_v,
        'dtt':self.dateTO_v,
        'ybckl':self.ybckl_v,
        'bmn':self.bmn
        }

        # クエリーインスタンス定義
        qr = sqlquery.Salesresult_jikanbetu_Query(cdtdct)

        # SQL 組み立て
        qr.querycreate()

        # SQL実行
        # JANコード(0)、JANコード2(1)、商品名(2)、販売点数(3)、販売金額(4)、販売時間(5)、小分類(6)
        # "JANCD","JANCD_2","HINNM","SALES_ITM","SALES_AMT","SELTMZNCD","SYOKBN"
        loaddata = qr.query_execute()

        return loaddata

    def sjdata_syukei1(self,dt):
        col_names1 = ['JANCD','HINNM','SALES_ITM','SALES_AMT','SELTMZNCD','SYOKBN','LINE','CLASS']
        # データフレームとして読み込み
        df = pd.DataFrame(dt,columns=col_names1)

        if df.size != 0:
            # 小分類を中、大に分ける
            
            # 小分類が数値ではない場合、0にする
            df.loc[(df["SYOKBN"].astype('str').str.isdigit() == False), 'SYOKBN'] = 0

            # 右から1～4桁を取得
            df.loc[(df["SYOKBN"].apply(lambda x: len(str(x))) < 9), 'SYOKBN_M'] = df['SYOKBN'].astype(str).str[-4:]
            #df['SYOKBN_L'] = np.where(df.SYOKBN > 5, 0, None)
            df.loc[(df["SYOKBN"].apply(lambda x: len(str(x))) < 5), 'SYOKBN_L'] = 0
            # 右から5～8桁を取得
            df.loc[(df["SYOKBN"].apply(lambda x: len(str(x))) > 4), 'SYOKBN_L'] = df['SYOKBN'].astype(str).str[-8:-4]

            # 大中小を計算
            # (販売金額 / 販売数) <= 中の金額　の場合、分類は小
            df.loc[(df['SALES_ITM'] > 0) & ((df['SALES_AMT']/df['SALES_ITM']) <= df['SYOKBN_M'].astype(float)), 'BUNRUI'] = '小'
            # 大の金額 == 0 かつ　(販売金額 / 販売数) => 小の金額　の場合、分類は中
            df.loc[(df['SYOKBN_L'].astype(int) == 0) & ((df['SALES_AMT']/df['SALES_ITM']) > df['SYOKBN_M'].astype(float)), 'BUNRUI'] = '中'
            # 大の金額 > 0 かつ　(販売金額 / 販売数) > 中の金額　かつ　(販売金額 / 販売数) <= 大の金額　の場合、分類は中
            df.loc[(df['SYOKBN_L'].astype(int) > 0) & ((df['SALES_AMT']/df['SALES_ITM']) > df['SYOKBN_M'].astype(float)) & ((df['SALES_AMT']/df['SALES_ITM']) <= df['SYOKBN_L'].astype(float)), 'BUNRUI'] = '中'
            # 大の金額 > 0 かつ　(販売金額 / 販売数) > 大の金額　の場合、分類は大
            df.loc[(df['SYOKBN_L'].astype(int) > 0) & ((df['SALES_AMT']/df['SALES_ITM']) > df['SYOKBN_L'].astype(float)), 'BUNRUI'] = '大'
            # 小分類が入っていないデータは0にする
            df.loc[(df['SYOKBN_M'].astype(int) == 0), 'BUNRUI'] = ''

            # 時間帯の修正
            # 8:00 ～ 10:00は11:00扱いとする
            # 0:00 ～ 1:00は23:00扱いとする
            df.loc[(df['SELTMZNCD'] < 3), 'SELTMZNCD'] = 3
            df.loc[(df['SELTMZNCD'] > 16), 'SELTMZNCD'] = 16
            

            # 欠損値を含む行を削除（販売数 or 販売金額が0の場合、分類がnanになる）
            df = df.dropna(how='any')

            # ライン、クラス、JANコードでソート
            df = df.sort_values(['LINE','CLASS','JANCD'])
            #df = df.sort_values(['JANCD'])

            # 不要項目を削除
            #df.drop(['LINE','CLASS'], axis=1)

            # 必要項目の抽出
            df_gp1 = df.loc[:,['JANCD','HINNM','BUNRUI','SALES_ITM','SALES_AMT','SYOKBN_M','SYOKBN_L','SELTMZNCD']]
        else:
            df_gp1 = df

        # dataframeをリストに変換
        return df_gp1.to_numpy().tolist()

    def sjdata_cr(self,data):
        # リストのデータ
        # JANCD(JANコード),HINNM(商品コード),BUNRUI(分類名),SALES_ITM(販売点数),SALES_AMT(販売金額),SYOKBN_M(小分類1),SYOKBN_L(小分類2),SELTMZNCD(販売時間コード)
        # ↓
        # JANコード、分類名ごと
        # JANCD[0],HINNM[1],SYOKBN_M[2],SYOKBN_L[3],BUNRUI[4],SALES_ITM[5],SALES_AMT[6],
        # 販売時間数量(3) [7],販売時間数量(4) [8],販売時間数量(5) [9],販売時間数量(6) [10],
        # 販売時間数量(7) [11],販売時間数量(8) [12],販売時間数量(9) [13],販売時間数量(10) [14],
        # 販売時間数量(11) [15],販売時間数量(12) [16],販売時間数量(13) [17],販売時間数量(14) [18],
        # 販売時間数量(15) [19],販売時間数量(16) [20]
        for i,row in enumerate(data):
            if i == 0:
                # 1回目のループの場合、JANコードを記憶
                tmpjan = row[0]
                # 変数（フラグ、リスト）の初期化
                self.dj_hensu_reset() 

            if tmpjan != row[0]:
                # JANコードが変わった場合
                for rowlst in [self.smalllst,self.middlelst,self.largelst,self.blanklst]:
                    if rowlst != '':
                        self.dictlist.append(salesJBClass.sjdictdt_cr(self.dictlist,rowlst))
                # 変数（フラグ、リスト）の初期化
                self.dj_hensu_reset()
                # JANコードを保持
                tmpjan = row[0]
            
            # JANコードが同じ場合
            if tmpjan == row[0]:
                self.bunruihantei(row)

            if i == len(data) - 1:
                # 最後のループの時
                for rowlst in [self.smalllst,self.middlelst,self.largelst,self.blanklst]:
                    if rowlst != '':
                        self.dictlist.append(salesJBClass.sjdictdt_cr(self.dictlist,rowlst))
            # JANコードを保持
            tmpjan = row[0]

    def dj_hensu_reset(self):
        self.smallflg = self.middleflg = self.largeflg = self.brankflg = 1
        self.smalllst = self.middlelst = self.largelst = self.blanklst = '' 

    def bunruihantei(self,row):
        # 分類が小の場合
        if row[2] == '小':
            if self.smallflg == 1:
                # 初回の場合、初期化
                self.smalllst = salesJBClass.tmpdt_syokika(row)
                self.smallflg = 0
            # データ加算
            self.smalllst = salesJBClass.tmpdt_add(self.smalllst,row)
        elif row[2] == '中':
            if self.middleflg == 1:
                # 初回の場合、初期化
                self.middlelst = salesJBClass.tmpdt_syokika(row)
                self.middleflg = 0
            # データ加算
            self.middlelst = salesJBClass.tmpdt_add(self.middlelst,row)    
        elif row[2] == '大':
            if self.largeflg == 1:
                # 初回の場合、初期化
                self.largelst = salesJBClass.tmpdt_syokika(row)
                self.largeflg = 0
            # データ加算
            self.largelst = salesJBClass.tmpdt_add(self.largelst,row)
        else:
            if self.brankflg == 1:
                # 初回の場合、初期化
                self.blanklst = salesJBClass.tmpdt_syokika(row)
                self.brankflg = 0
            # データ加算
            self.blanklst = salesJBClass.tmpdt_add(self.blanklst,row)

    def tmpdt_syokika(data):
        # JANCD(JANコード)、HINNM(商品コード)、BUNRUI(分類名),SALES_ITM(販売点数),
        # SALES_AMT(販売金額),SYOKBN_M(小分類1),SYOKBN_L(小分類2),SELTMZNCD(販売時間コード)
        tmplst = []
        # JANCD(JANコード)
        tmplst.append(data[0])
        # HINNM(商品コード)
        tmplst.append(data[1])
        # SYOKBN_M(小分類1)
        tmplst.append(data[5])
        # SYOKBN_L(小分類2)
        tmplst.append(data[6])
        # BUNRUI(分類名)
        tmplst.append(data[2])
        for i in range(21):
            # SALES_ITM、SALES_AMT、SYOKBN_M、SYOKBN_L、time3 ～ time16までを初期化
            tmplst.append(0)
        
        return tmplst

    def tmpdt_add(data,row):
        # SALES_ITM(販売点数)
        data[5] += int(row[3])
        # SALES_AMT(販売金額)
        data[6] += int(row[4])
        # 時間帯ごとに数量を代入する
        # time3 ～ time16
        # 配列7～20
        data[int(row[7]) + 4] += int(row[3])

        return data

    def sjdictdt_cr(dictlist,data):

        # JANCD[0],HINNM[1],SYOKBN_M[2],SYOKBN_L[3],BUNRUI[4],SALES_ITM[5],SALES_AMT[6],
        # 販売時間数量(3) [7],販売時間数量(4) [8],販売時間数量(5) [9],販売時間数量(6) [10],
        # 販売時間数量(7) [11],販売時間数量(8) [12],販売時間数量(9) [13],販売時間数量(10) [14],
        # 販売時間数量(11) [15],販売時間数量(12) [16],販売時間数量(13) [17],販売時間数量(14) [18],
        # 販売時間数量(15) [19],販売時間数量(16) [20]
        # 商品名,JANCD
        hinnm = str(data[1]) + "," + str(data[0])

        # 分類
        bunrui = data[4]

        # 販売金額
        saleskng = str(data[6])
        # 販売点数
        salessu = str(data[5])

        # 分類金額範囲
        if data[2] == 0:
            brgkrng = ''
        elif data[3] == 0:
            brgkrng = str(data[2]) + ",0"
        else:
            brgkrng = str(data[2]) + "," + str(data[3])

        for i in range(14):
            # 販売数量（time3 ～ time16）が0の場合、空白にする
            if data[i+7] == 0:
                data[i+7] = ''

        # 表示データ
        # hinnm:"りんご,0215456555551", bunrui:"大", saleskng:"24510",salessu:"15", 
        # time3:2,time4:3, time5:0, time6:0, time7:0, time8:0, time9:0,
        # time10:0, time11:0, time12:0, time13:0, time14:0, time15:0, time16:1, brgkrng:"200,500"

        # 辞書リストの作成
        dictlist={
            'hinnm':hinnm,'bunrui':bunrui,'saleskng':saleskng,'salessu':salessu,
            'time3':data[7],'time4':data[8],'time5':data[9],'time6':data[10],'time7':data[11],
            'time8':data[12],'time9':data[13],'time10':data[14],'time11':data[15],'time12':data[16],
            'time13':data[17],'time14':data[18],'time15':data[19],'time16':data[20],'brgkrng': brgkrng
            }

        return dictlist
