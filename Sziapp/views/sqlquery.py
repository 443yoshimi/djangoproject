from django.db import connection
import datetime
from . import common

#　販売実績一覧表
# グリッドの描画(初期表示、セレクトボックス選択時）

class MainSql:
    def __init__(self):
        pass

    def query_execute(self):
        with connection.cursor() as cursor:
            cursor.execute(self.sql)

            result = cursor.fetchall()

            return result

class Salesresult_Query(MainSql):
    def __init__(self,cdt):
        
        self.cnditiondct = cdt

         # 商品
        if self.cnditiondct['hin'] == "":
            self.hincndition = ""
        else:
            # 数値判定
            if self.cnditiondct['hin'].isdigit():
                # 数値の場合
                # 全角→半角変換
                self.hincndition = " AND TSML.JANCD LIKE '" + self.cnditiondct['hin'].translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})) + "%'"
            else:
                # 数値以外の場合
                self.hincndition = " AND HNM.HINNM LIKE '%" + str(self.cnditiondct['hin']) + "%'"
        
        # 店舗
        if (self.cnditiondct['ktn'] == '99999') or (self.cnditiondct['ktn'] == ''):
            # 初期表示 or 全店表示
            self.ktncndition = ""
        else:
            self.ktncndition = " AND TSML.STORE_CD = " + self.cnditiondct['ktn']

        # カテゴリーコード
        if self.cnditiondct['ctg'] == '':
            self.ctgcondition = ""
        else:
            self.ctgcondition = " AND HNM.CATCD = '77006'"


        # 取得日付範囲、曜日の条件
        # 日付インスタンスの定義
        dtcmn = common.DateCalccmn(self.cnditiondct['date'])

        # 基準日をマイナス1する
        dtcmn.datekeisan(-1)

        # to日付の取得
        todt = dtcmn.dateformcnv1()

        # from日付の取得
        fromdt = dtcmn.dateformcnv2(dtcmn.fromdate_timedelta(self.cnditiondct['kk4w']))

       # 日付範囲 FROM,TO日付を設定
        self.datecondition = "((TSML.DEAL_DATE BETWEEN '" + str(fromdt) + "' AND '" + todt + "')"

        # 曜日条件を設定
        self.datecondition += " AND (TSML.YOBI IN ("
        for row in self.cnditiondct['ybckl'].split(','):
            self.datecondition += str(row) + ","

        # 末尾のカンマを削除して、かっこを閉じる
        self.datecondition = self.datecondition.strip(',') + ")))"
        
        # 使用するﾃｰﾌﾞﾙを定義
        if self.ktncndition == "":
            self.TSMLTB = "TIMESALESMEILOG"
            self.HIKTB = "HIKMEILOG"
        else:
            self.TSMLTB = "TIMESALESMEILOG_" + self.cnditiondct['ktn']
            self.HIKTB = "HIKMEILOG_" + self.cnditiondct['ktn']

    def querycreate(self):

        self.sql = (
            "SELECT " +\
            "SLRSLT1.DEAL_DATE,SLRSLT1.YOBI,SLRSLT1.STORE_CD,SLRSLT1.JANCD,'' AS JANCD2," +\
            "SLRSLT1.HINNM,SLRSLT1.SALES_ITM,SLRSLT1.SALES_AMT,SLRSLT1.nebiki0,SLRSLT1.nebiki30," +\
            "SLRSLT1.nebiki99,HKML.HIKSU,SLRSLT1.SYOKBN,SLRSLT1.LASTSELTMZNCD,SLRSLT1.LINECD,SLRSLT1.CLASSCD,SLRSLT1.NEBIKI_KNG " +\
            "FROM ( " +\
            "SELECT TSML.DEAL_DATE,TSML.YOBI,TSML.STORE_CD,TSML.JANCD,TSML.JANCD_2," +\
            "HNM.HINNM,HNM.LINECD,HNM.CLASSCD,HNM.CATCD," +\
            "SUM(TSML.SALES_ITM) AS SALES_ITM,SUM(TSML.SALES_AMT) AS SALES_AMT,SUM(TSML.ITEM_DIS_AMT) AS NEBIKI_KNG," +\
            "SUM((TSML.NebikiRitu0)) AS nebiki0," +\
            "SUM((TSML.NebikiRitu10+TSML.NebikiRitu20+TSML.NebikiRitu30)) AS nebiki30," +\
            "SUM((TSML.NebikiRitu40+TSML.NebikiRitu50+TSML.NebikiRitu99)) AS nebiki99,HNM.SYOKBN," +\
            "MAX(TSML.LASTSELTMZNCD) AS LASTSELTMZNCD FROM " + self.TSMLTB + " TSML " +\
            "LEFT JOIN HINMST HNM ON HNM.JANCD = TSML.JANCD " +\
            "WHERE " + self.datecondition +\
            " AND HNM.CKMCD = " + self.cnditiondct['ckm'] +\
            self.ktncndition +\
            " AND HNM.BMNCD = " + self.cnditiondct['bmn'] +\
            self.ctgcondition +\
            self.hincndition +\
            " GROUP BY DEAL_DATE,YOBI,STORE_CD,JANCD " +\
            ") AS SLRSLT1 LEFT JOIN " + self.HIKTB + " HKML ON " +\
            "(HKML.HIKDT = SLRSLT1.DEAL_DATE)  AND " +\
            "(HKML.STORE_CD = SLRSLT1.STORE_CD) AND " +\
            "(HKML.JANCD = SLRSLT1.JANCD) " +\
            "UNION ALL " +\
            "(SELECT " +\
            "SLRSLT2.DEAL_DATE,SLRSLT2.YOBI,SLRSLT2.STORE_CD,SLRSLT2.JANCD,SLRSLT2.JANCD_2," +\
            "SLRSLT2.HINNM,SLRSLT2.SALES_ITM,SLRSLT2.SALES_AMT,SLRSLT2.nebiki0,SLRSLT2.nebiki30," +\
            "SLRSLT2.nebiki99,0,SLRSLT2.SYOKBN,SLRSLT2.LASTSELTMZNCD,SLRSLT2.LINECD,SLRSLT2.CLASSCD,SLRSLT2.NEBIKI_KNG " +\
            "FROM (" +\
            "SELECT TSML.DEAL_DATE,TSML.YOBI,TSML.STORE_CD,TSML.JANCD,TSML.JANCD_2," +\
            "HNM.HINNM,HNM.LINECD,HNM.CLASSCD,HNM.CATCD," +\
            "SUM(TSML.SALES_ITM) AS SALES_ITM,SUM(TSML.SALES_AMT) AS SALES_AMT,SUM(TSML.ITEM_DIS_AMT) AS NEBIKI_KNG," +\
            "SUM((TSML.NebikiRitu0)) AS nebiki0," +\
            "SUM((TSML.NebikiRitu10+TSML.NebikiRitu20+TSML.NebikiRitu30)) AS nebiki30," +\
            "SUM((TSML.NebikiRitu40+TSML.NebikiRitu50+TSML.NebikiRitu99)) AS nebiki99,HNM.SYOKBN," +\
            "TSML.LASTSELTMZNCD FROM  " + self.TSMLTB + " TSML " +\
            "LEFT JOIN HINMST HNM ON HNM.JANCD = TSML.JANCD " +\
            "WHERE " + self.datecondition +\
            " AND HNM.CKMCD = " + self.cnditiondct['ckm'] +\
            self.ktncndition  +\
            " AND HNM.BMNCD = " + self.cnditiondct['bmn'] +\
            self.ctgcondition +\
            self.hincndition +\
            " AND TSML.JANCD <> TSML.JANCD_2 " +\
            " GROUP BY DEAL_DATE,YOBI,STORE_CD,JANCD,JANCD_2,LASTSELTMZNCD " +\
            ") AS SLRSLT2);"
        )


class Discount_Query(MainSql):
    def __init__(self,cdt):
        self.cnditiondct = cdt

         # 商品
        if self.cnditiondct['hin'] == "":
            self.hincndition = ""
        else:
            # 数値判定
            if self.cnditiondct['hin'].isdigit():
                # 数値の場合
                # 全角→半角変換
                self.hincndition = " AND TSML.JANCD LIKE '" + self.cnditiondct['hin'].translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})) + "%'"
            else:
                # 数値以外の場合
                self.hincndition = " AND HNM.HINNM LIKE '%" + str(self.cnditiondct['hin']) + "%'"
        
        # 店舗
        if (self.cnditiondct['ktn'] == '99999') or (self.cnditiondct['ktn'] == ''):
            # 初期表示 or 全店表示
            self.ktncndition = ""
        else:
            self.ktncndition = " AND TSML.STORE_CD = " + self.cnditiondct['ktn']

        # 日付
        self.datecondition = " TSML.DEAL_DATE BETWEEN '" + self.cnditiondct['dtf'] + "' AND '" + self.cnditiondct['dtt'] + "'"

        # 使用するﾃｰﾌﾞﾙを定義
        if self.ktncndition == "":
            self.TSMLTB = "TIMESALESMEILOG"
        else:
            self.TSMLTB = "TIMESALESMEILOG_" + self.cnditiondct['ktn']
            
    def querycreate(self):
        # JANコード1、JANコード2、商品名、売上点数、売上金額、値引き金額、小区分
        self.sql = (
            "SELECT" +\
            " TSML.JANCD,TSML.JANCD_2,HNM.HINNM,TSML.SALES_ITM,TSML.SALES_AMT," +\
            " TSML.ITEM_DIS_AMT,HNM.SYOKBN,HNM.LINECD,HNM.CLASSCD" +\
            " FROM " + self.TSMLTB  + " TSML" +\
            " LEFT JOIN HINMST HNM ON HNM.JANCD = TSML.JANCD" +\
            " WHERE" + self.datecondition +\
            " AND HNM.CKMCD = " + self.cnditiondct['ckm'] +\
            self.ktncndition +\
            self.hincndition +\
            " AND HNM.BMNCD = " + self.cnditiondct["bmn"] +\
            " AND TSML.SALES_ITM > 0" +\
            " ORDER BY TSML.JANCD,TSML.JANCD_2;"
        )


class Salesresult_jikanbetu_Query(MainSql):
    def __init__(self,cdt):
        
        self.cnditiondct = cdt

         # 商品
        if self.cnditiondct['hin'] == "":
            self.hincndition = ""
        else:
            # 数値判定
            if self.cnditiondct['hin'].isdigit():
                # 数値の場合
                # 全角→半角変換
                self.hincndition = " AND TSML.JANCD LIKE '" + self.cnditiondct['hin'].translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})) + "%'"
            else:
                # 数値以外の場合
                self.hincndition = " AND HM.HINNM LIKE '%" + str(self.cnditiondct['hin']) + "%'"
        
        # 店舗
        if (self.cnditiondct['ktn'] == '99999') or (self.cnditiondct['ktn'] == ''):
            # 初期表示 or 全店表示
            self.ktncndition = ""
        else:
            self.ktncndition = " AND TSML.STORE_CD = " + self.cnditiondct['ktn']

        # 日付範囲 FROM,TO日付を設定
        self.datecondition = "(TSML.DEAL_DATE BETWEEN '" + str(self.cnditiondct['dtf']) + "' AND '" + (self.cnditiondct['dtt']) + "')"

        # 曜日条件を設定
        self.yobicondition = " AND TSML.YOBI IN ("
        for row in self.cnditiondct['ybckl'].split(','):
            self.yobicondition += str(row) + ","

        # 末尾のカンマを削除して、かっこを閉じる
        self.yobicondition = self.yobicondition.strip(',') + ")"

        # 使用するﾃｰﾌﾞﾙを定義
        if self.ktncndition == "":
            self.TSMLTB = "TIMESALESMEILOG"
        else:
            self.TSMLTB = "TIMESALESMEILOG_" + self.cnditiondct['ktn']


    def querycreate(self):

        self.sql = (
            "SELECT " +\
            "TSML.JANCD,HM.HINNM,TSML.SALES_ITM,TSML.SALES_AMT," +\
            "TSML.SELTMZNCD,HM.SYOKBN,HM.LINECD,HM.CLASSCD " +\
            "FROM " + self.TSMLTB  + " TSML " +\
            "JOIN HINMST HM ON HM.JANCD = TSML.JANCD " +\
            "WHERE " + self.datecondition + self.yobicondition + self.ktncndition  +\
            " AND HM.CKMCD = " + self.cnditiondct['ckm'] +\
            " AND HM.BMNCD = " + self.cnditiondct['bmn'] +\
            self.hincndition + ";"
        )


class Instruct_Query(MainSql):
    def __init__(self,cdt):
        self.cnditiondct = cdt
        
        # 店舗
        if (self.cnditiondct['ktn'] == '99999') or (self.cnditiondct['ktn'] == ''):
            # 初期表示 or 全店表示
            self.ktncndition = " WP.CKMCD = '" + self.cnditiondct['ckm'] + "'"
        else:
            self.ktncndition = " WP.KTNCD = '" + self.cnditiondct['ktn'] + "' AND WP.CKMCD = '" + self.cnditiondct['ckm'] + "'"

        # カテゴリーコード
        if self.cnditiondct['ctg'] == '':
            self.ctgcondition = ""
        else:
            self.ctgcondition = " AND WP.CATCD = '" + self.cnditiondct['ctg'] + "'"


        # 日付
        self.datecondition = " AND WP.SIZDATE = '" + self.cnditiondct['date'] + "'"

        # 使用するﾃｰﾌﾞﾙを定義
        self.TSMLTB = "WORKPLAN"
            
    def querycreate(self):
        # JANコード1、JANコード2、商品名、売上点数、売上金額、値引き金額、小区分
        self.sql = (
            "SELECT" +\
            " WP.ID,WP.SSKCD,WP.KTNCD,WP.CKMCD,WP.CATCD,WP.HINCD," +\
            " WP.HINNM,WP.CALLCD,WP.SIZE,WP.TRAY,WP.BAITNK,WP.GOZEN," +\
            " WP.HRADD,WP.GGADD,WP.TSADD" +\
            " FROM " + self.TSMLTB  + " WP" +\
            " WHERE" + self.ktncndition +\
            self.ctgcondition +\
            self.datecondition +\
            ";"
        )