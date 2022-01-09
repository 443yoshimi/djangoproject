
import datetime
from .forms import CookingMethodForm,KyotenForm,HinSerchTextform
from .forms import Kako4ChoiceForm,WeekcheckboxForm,AddCalenderForm2
from .forms import AddCalenderForm3,AddCalenderForm4,HinCategoryForm,KyotenFormDisable,CookingMethodFormDisable

class Convertcmn:
    def __init__(self):
        pass
    
    # 曜日コード変換
    def yobicdcvt(self,yobicd):
        # 月：0　火：1　水：2　木：3　金：4　土：5　日：6
        yobilst = ["月","火","水","木","金","土","日"]        

        return yobilst[yobicd]

    # None変換
    def nonecvt(self,a,b):
        if a is None:
            # Noneの時、変更
            value = b
        else:
            value = a

        return value


class DateCalccmn:
    def __init__(self,day):
        # 基準日
        self.kijundate = day

        # 本日
        self.today = datetime.date.today()

        if self.kijundate == '':
            # POST、GET、保存されたデータがある場合
            self.getdate = self.today
        else:
            # 初期表示
            self.getdate = datetime.datetime.strptime(self.kijundate, '%Y-%m-%d')
    
    def datekeisan(self,value):
        # 日付を計算
        self.getdate = self.getdate + datetime.timedelta(days=value)

    def datecalck(self,date1,num):
        return date1 + datetime.timedelta(days=num)

    def dateformcnv1(self):
        # 日付型から文字列(yyyy-mm-dd)
        return self.getdate.strftime('%Y-%m-%d')

    def dateformcnv2(self,dt):
        # 日付型から文字列(yyyy-mm-dd)
        return dt.strftime('%Y-%m-%d')

    def yobiget(self):
        # 曜日番号から文字列曜日
        w_list = ['月', '火', '水', '木', '金', '土', '日']

        return w_list[self.getdate.weekday()]

    def inputdt_yobiget(self,dt):
        # 曜日番号から文字列曜日
        w_list = ['月', '火', '水', '木', '金', '土', '日']
        dt1 = datetime.datetime.strptime(dt, '%Y-%m-%d')
        
        return w_list[dt1.weekday()]

    def yobinumget(self,num = 0):
        # 曜日番号を返却
        targetday = self.getdate + datetime.timedelta(days=num)
        return targetday.weekday()

    def yobidate_sa(self,yobickbnum,postyobinum,kk4cnt):
        # 曜日から日付差を算出
        if yobickbnum > postyobinum:
            # 7 - (曜日checkboxの曜日番号 - POST日付の曜日番号)
            sa = (7- (abs(yobickbnum - postyobinum))) + (7*kk4cnt)
        else:
            # 曜日checkboxの曜日番号 - POST日付の曜日番号
            sa = abs(yobickbnum - postyobinum) + (7*kk4cnt)
        return sa

    def fromdate_timedelta(self,week):
        # fromdate = 基準日 - 週 +1
        # 例）2021年11月2日の過去1週の場合
        #  2021年10月27日（水）　～  2021年11月2日 にしたい
        dt1 = self.getdate - datetime.timedelta(weeks=int(week))
        dt2 = dt1 + datetime.timedelta(days=1)
        return dt2

def syokbnstr_hantei(syokbn,genk):
    # 大、中、小を区別
    # 小区分
    bunruistr = ''
    mid = ''
    lg = ''

    # 小区分が入っている場合
    if (syokbn != '') and (syokbn != '0') and (syokbn != ''):
        # ～中
        # 1～4桁かつ0以外の場合
        mid = syokbn[-4:]

        # ～大
        # 小区分が5～8桁の場合、8桁目から左に4桁取得
        # 小区分が5～8桁ではない場合、10000を設定()
        lg = syokbn[-8:-4] if ((len(syokbn)) > 4 and (len(syokbn) < 9)) else ""

        if lg == '':
            if genk <= int(mid):
                bunruistr = '小'
            else:
                bunruistr = '中'
        else:
            # 大中小の判定
            if genk <= int(mid):
                bunruistr = '小'
            elif genk <= int(lg):
                bunruistr = '中'
            else:
                bunruistr = '大'
    
    return bunruistr


class SessionManage:
    def __init__(self):
        pass

    def session_check(self,keyword):
        sessionv = self.request.session.get(keyword)
        if sessionv is not None:
            self.sessiondict.update({keyword: sessionv})


class FormGenerater(SessionManage):
    def __init__(self,s_request,sessionkey):
        # コンストラクタ
        # POST情報
        self.request = s_request

        self.user_ten = self.request.user.first_name

        self.sessiondict = {}
        # セッションキーの初期化
        for row in sessionkey:
            self.sessiondict[row] = ''

    def common1_formset(self):
        # cform → common form
        # 店舗ドロップダウン
        if self.sessiondict["s_kyoten"] == '':
            # セッションが空の場合
            if self.user_ten == '100':
                kyoten = ''
            else:
                # 前ゼロを消して文字列にする
                kyoten = str(int(self.user_ten))
        else:
            kyoten = self.sessiondict["s_kyoten"]

        self.cform_kyoten = KyotenForm(initial={'name': kyoten})
        # 調達方法ドロップダウン
        self.cform_ckm = CookingMethodForm(initial={'name': self.sessiondict["s_ckm"]})
        # 商品検索ボックス
        self.cform_hintb = HinSerchTextform(initial={'name': self.sessiondict["s_hintb"] })

    def common2_formset(self):
        # cform → common form
        # カレンダーフォームfrom
        self.cform_clndrfrom = AddCalenderForm3(initial={'name': self.sessiondict["s_salesdatefrom"]})
        # カレンダーフォームto
        self.cform_clndrto = AddCalenderForm4(initial={'name': self.sessiondict["s_salesdateto"]})

    def saler_formset(self):
        # cform → common form
        # 過去4週セレクトボックス
        self.srform_kako4 = Kako4ChoiceForm(initial={'name': self.sessiondict["s_srkako4"]})
        # 曜日チェックボックス
        self.srform_wckb = WeekcheckboxForm(initial={'weekckbx': self.sessiondict["s_sryobinum"]})
        # カレンダーフォーム
        self.srform_clndr = AddCalenderForm2(initial={'name': self.sessiondict["s_srsalesdate"]})

    def selesjb_fromset(self):
        self.sjbform_wckb = WeekcheckboxForm(initial={'weekckbx': self.sessiondict["s_sjbyobinum"]})


    def instruct_fromset(self):
        # cform → common form
        # 店舗ドロップダウン
        if self.sessiondict["s_instkyoten"] == '':
            # セッションが空の場合
            if self.user_ten == '100':
                kyoten = ''
            else:
                # 前ゼロを消して文字列にする
                kyoten = str(int(self.user_ten))
        else:
            kyoten = self.sessiondict["s_instkyoten"]

        if self.user_ten == '100':
            self.cform_kyoten = KyotenForm(initial={'name': kyoten})
        else:
            self.cform_kyoten = KyotenFormDisable(initial={'name': kyoten})

        # 調達方法ドロップダウン
        self.cform_ckm = CookingMethodFormDisable(initial={'name': self.sessiondict["s_instckm"]})
        # カテゴリドロップダウン
        self.cform_hincat = HinCategoryForm(initial={'name': self.sessiondict["s_insthincat"]})
        # カレンダーフォーム
        self.srform_clndr = AddCalenderForm2(initial={'name': self.sessiondict["s_instcalender"]})
