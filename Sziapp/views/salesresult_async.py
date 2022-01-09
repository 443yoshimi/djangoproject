from typing_extensions import ParamSpec
from django.db.models.query_utils import Q
from django.core.serializers import serialize
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from . import sqlquery
from . import common

#　販売実績一覧表
# グリッドの描画(初期表示、セレクトボックス選択時）
def salesresult_load(request):

    # 販売実績クラスのインスタンス作成
    sr = salesRClass(request)

    # 表示ﾃﾞｰﾀ取得
    dt = sr.srdata_get()

    # ソート
    dt = sr.srdata_sort(dt)

    # 重複行の削除、大中小集計
    sr.srdata_uniqsum(dt)

    # 表示ﾃﾞｰﾀ作成２
    sr.srdata_cr()
            
    return JsonResponse(sr.srdictlist,safe=False)

class salesRClass:
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

        # 日付
        self.date_v = request.GET['date']
        # セッション格納
        request.session['s_srsalesdate'] = self.date_v

        # 過去1～4週
        self.kk4w_v = request.GET['kk4w']
        # セッション格納
        request.session['s_srkako4'] = self.kk4w_v

        # 曜日チェックボックス
        self.ybckl_v = request.GET['ybckl']
        # セッション格納
        request.session['s_sryobinum'] = self.ybckl_v

        # 部門
        self.bmn = '77'

        # カテゴリー
        self.catgcd = ''

        self.loaddata3 = []
        

    def srdata_get(self):
        # 表示ﾃﾞｰﾀ取得
        # jsonresposeデータ
        cdtdct = {
        'ktn':self.ktn_v,
        'ckm':self.ckm_v,
        'ctg':self.catgcd,
        'hin':self.hin_v,
        'date':self.date_v,
        'kk4w':self.kk4w_v,
        'ybckl':self.ybckl_v,
        'bmn':self.bmn
        }

        # クエリーインスタンス定義
        qr = sqlquery.Salesresult_Query(cdtdct)

        # SQL 組み立て
        qr.querycreate()

        # SQL実行
        # 日付(0)、曜日コード(1)、店コード(2)、JAN1(3)、JAN2(4)、商品名(5)、販売数量(6)、販売金額(7)、
        # 値引なし販売数(8)、値引1-30%販売数(9)、値引31%以上販売数(10)、
        # 廃棄数(11)、小分類(12)、最終販売時刻コード(13)
        loaddata = qr.query_execute()

        return loaddata

    def srdata_sort(self,dt):
        # ライン、クラス、JANコード、JANコード2の昇順にソート
        sorted_data = sorted(dt, key=lambda x:(x[14],x[15],x[3], x[4]))

        return sorted_data

    def srdata_uniqsum(self,dt): 
        # 初期化
        tencd = jancd = jancd2 = selsu = selgaku = 0
        loaddata1 = []
        gokeirow = ''

        # 合計行を1行にする
        for i,row in enumerate(dt):
            rowlst = list(row)
            if rowlst[11] is None:
                # 廃棄がNoneの場合 0にする
                rowlst[11] = 0
            
            # 合計行リストが空 かつ 合計行の場合
            if (gokeirow == '') and (rowlst[4] == ''):
                # 合計行リストに代入
                gokeirow = rowlst
            elif (rowlst[3] == jancd) and (rowlst[4] == ''):
                # 集計対象の場合、合計行を集計
                # JAN(3)が同じ かつ　JAN(4)が空の場合(合計行の場合）
                gokeirow = salesRClass.syokbnbetu_gokei(gokeirow,rowlst)
            else:
                if gokeirow != '':
                    # 小区分は空白にしておく
                    gokeirow[12] = ''
                    # リストに合計行を追加
                    loaddata1.append(gokeirow)
                    # 合計行と明細行の重複を削除するために記憶
                    tencd = gokeirow[2]
                    jancd2 = gokeirow[3]
                    selsu = gokeirow[6]
                    selgaku = gokeirow[7]
                    gokeirow = ''
            
                # 明細追加
                # 小区分(12)が入っている場合、リスト追加
                if ((rowlst[12] != '0') and (rowlst[12] != '')):
                    # 日付(0)、曜日コード(1)、店コード(2)、JAN1(3)、JAN2(4)、商品名(5)、販売数量(6)、販売金額(7)、
                    # 値引なし販売数(8)、値引1-30%販売数(9)、値引31%以上販売数(10)、
                    # 廃棄数(11)、小分類(12)、最終販売時刻コード(13)、ライン(14)、クラス(15)、値引金額合計(16)、大中小値段範囲(17)
                    loaddata1.append(salesRClass.syokbn_str(rowlst))
            jancd = rowlst[3]

        # 大中小集計
        smrow = midrow = lgrow = ''
        for i,row2 in  enumerate(loaddata1):
            # JAN2が入っている かつ 、小分類が大中小のどれかの場合（明細行の場合）
            if (row2[4] != '') and (any(v == row2[12] for v in ['小','中','大'])):
                # 分類ごとに集計
                # 販売数量、販売金額、値引なし販売数、値引1-30%販売数、値引31%以上販売数、廃棄数を足し算、最終販売時刻コードが大きい値を取得
                if row2[12] == '小':
                    # 小分類が小の場合
                    # smrowが空→初期化 空ではない→加算
                    smrow = row2 if (smrow == '') else salesRClass.syokbnbetu_gokei(smrow,row2)

                elif row2[12] == '中':
                    # 小分類が中の場合
                    # midrowが空→初期化 空ではない→加算
                    midrow = row2 if (midrow == '') else salesRClass.syokbnbetu_gokei(midrow,row2)

                elif row2[12] == '大':
                    # 小分類が大の場合
                    # lgrowが空→初期化 空ではない→加算
                    lgrow = row2 if (lgrow == '') else salesRClass.syokbnbetu_gokei(lgrow,row2)

                if (len(loaddata1) == (i + 1)):
                    # 最後のリスト追加
                    salesRClass.syokbn_listadd(self,smrow,midrow,lgrow,row2)
            else:
                # 明細行または、合計行をリストに追加
                salesRClass.syokbn_listadd(self,smrow,midrow,lgrow,row2)
                
                # 明細行と合計行が両方ある場合の対処
                if any(v != '' for v in [smrow,midrow,lgrow]):
                    # 合計行を追加
                    salesRClass.syokbn_listadd(self,'','','',row2)
                smrow = midrow = lgrow = ''

    def syokbn_str(sblst):
        # 大、中、小を区別
        # 小区分
        bunruistr = ''
        mid = ''
        lg = ''
        if (sblst[4] != '') and (sblst[12] != '0') and (sblst[12] != ''):
            # jan2が入っている場合 かつ 小分類が設定されている場合

            # ～中
            # 1～4桁かつ0以外の場合
            mid = sblst[12][-4:]

            # ～大
            # 5～8桁の場合
            lg = sblst[12][-8:-4] if ((len(sblst[12])) > 4 and (len(sblst[12]) < 9)) else 10000

            # 原価金額の算出
            genk = sblst[7]/sblst[6]

            # 大中小の判定
            if genk <= int(mid):
                bunruistr = '小'
            elif genk <= int(lg):
                bunruistr = '中'
            else:
                bunruistr = '大'

        # 分類金額範囲(ツールチップ用)
        if mid != '':
            if len(sblst[12]) > 4:
                # 分類が4桁より大きい場合、
                sblst.append(str(int(mid)) + "," + str(int(lg)))
            else:
                sblst.append(str(int(mid)) + ",0")
        else:
            sblst.append('')

        # 分類
        sblst[12] = bunruistr

        return sblst

    def syokbn_listadd(self,smrow,midrow,lgrow,row2):

        if (smrow != '') and (midrow == '') and (lgrow == ''):
            # 小のみ存在
            self.loaddata3.append(smrow)
        elif (smrow == '') and (midrow != '') and (lgrow == ''):
            # 中のみ存在
            self.loaddata3.append(midrow)
        elif (smrow == '') and (midrow == '') and (lgrow != ''):
            # 大のみ存在
            self.loaddata3.append(lgrow)
        elif (smrow != '') and (midrow != '') and (lgrow == ''):
            # 小、中が存在
            self.loaddata3.append(smrow)
            self.loaddata3.append(midrow)
        elif (smrow != '') and (midrow == '') and (lgrow != ''):
            # 小、大が存在
            self.loaddata3.append(smrow)
            self.loaddata3.append(lgrow)
        elif (smrow == '') and (midrow != '') and (lgrow != ''):
            # 中、大が存在
            self.loaddata3.append(midrow)
            self.loaddata3.append(lgrow)
        elif (smrow != '') and (midrow != '') and (lgrow != ''):
            # 小、中、大が存在
            self.loaddata3.append(smrow)
            self.loaddata3.append(midrow)
            self.loaddata3.append(lgrow)
        else:
            # 明細なし
            self.loaddata3.append(row2)

    def syokbnbetu_gokei(sumrow,rowlst):
        # 販売数量
        sumrow[6] = int(sumrow[6]) + int(rowlst[6])
        # 販売金額
        sumrow[7] = int(sumrow[7]) + int(rowlst[7])
        # 値引なし販売数
        sumrow[8] = int(sumrow[8]) + int(rowlst[8])
        # 値引1-30%販売数
        sumrow[9] = int(sumrow[9]) + int(rowlst[9])
        # 値引31%以上販売数
        sumrow[10] = int(sumrow[10]) + int(rowlst[10])
        # 廃棄数
        sumrow[11] = int(sumrow[11]) + int(rowlst[11])
        # 最終販売時刻コード
        sumrow[13] = int(rowlst[13]) if int(sumrow[13]) < int(rowlst[13]) else int(sumrow[13])

        # 値引き額
        sumrow[16] = int(abs(sumrow[16])) + int(abs(rowlst[16]))

        return sumrow

    def srdata_cr(self):
        Cvtcmn = common.Convertcmn()

        self.srdictlist = []

        # 曜日数
        yobisu = len(self.ybckl_v.split(','))
        # 過去週の数
        weeksu = int(self.kk4w_v)
        # 小数点以下
        syosuten = 2

        for row in self.loaddata3:
            # 定価販売数量,値下30%未満販売数量,値下30%以上販売数量,廃棄数量
            graph = str(round((Cvtcmn.nonecvt(row[8],0) / yobisu) / weeksu ,syosuten)) + "," + \
                str(round((Cvtcmn.nonecvt(row[9],0) / yobisu) / weeksu ,syosuten)) + "," +\
                str(round((Cvtcmn.nonecvt(row[10],0) / yobisu) / weeksu ,syosuten)) + "," + \
                str(round((Cvtcmn.nonecvt(row[11],0) / yobisu) / weeksu ,syosuten))

            # 商品名,JANCD
            hinnm = str(row[5]) + "," + str(row[3])

            # 分類
            bunrui = '' if row[12] == '' else row[12]

            # 販売金額,点数
            # 販売金額 = (販売金額 / 曜日数) / 過去週の数
            # 点数 = (点数 / 曜日数) / 過去週の数
            saleskngsu = str(round((row[7] / yobisu) / weeksu,syosuten)) + "," + \
                        str(round((row[6] / yobisu) / weeksu,syosuten))
            
            # 値引き率
            # 平均値引額 / 平均販売額
            nebikiritu =  str(round((float((abs(row[16]) / yobisu) / weeksu) / float((row[7] / yobisu) / weeksu)) *100,1) )

            # 最終販売時刻コード
            timelst = []
            lastselcd = row[13]

            # 分類金額範囲
            if bunrui != '':
                brgkrng = row[17]
            else:
                brgkrng = ''

            for i in range(17):
                # time3 ～ time16までを初期化
                timelst.append(0)

            if lastselcd < 4:
                # ～ 11:00 (時間帯コード 1,2,3)
                timelst[3] = 1
            elif lastselcd < 16:
                # 11:00 ～ 23:00 (時間帯コード 4 ～ 15)
                timelst[lastselcd] = 1
            else:
                # 23:00 ～ (時間帯コード 16 ～)
                timelst[-1] = 1
        
            # {graph:"100,0,0,0", hinnm:"りんご,0215456555551", bunrui:"大", saleskngsu:"24510,15", nebikiritu:"12.0"
            # time3:0,time4:0, time5:0, time6:0, time7:0, time8:0, time9:0,
            # time10:0, time11:0, time12:0, time13:0, time14:0, time15:0, time16:1 }

            # 辞書リストの作成
            self.srdictlist.append({
                'graph':graph,'hinnm':hinnm,'bunrui':bunrui,'saleskngsu':saleskngsu,'nebikiritu':nebikiritu,
                'time3':timelst[3],'time4':timelst[4],'time5':timelst[5],'time6':timelst[6],'time7':timelst[7],
                'time8':timelst[8],'time9':timelst[9],'time10':timelst[10],'time11':timelst[11],'time12':timelst[12],
                'time13':timelst[13],'time14':timelst[14],'time15':timelst[15],'time16':timelst[16],'brgkrng': brgkrng
                })
