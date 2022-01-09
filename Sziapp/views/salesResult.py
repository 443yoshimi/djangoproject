from django.shortcuts import render
from django.views import View
from . import common
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class SalesResultView(View):
    @method_decorator(login_required)
    def get(self, request):

        # セッション情報の定義
        sessionkeylst = ['s_kyoten','s_ckm','s_hintb','s_srkako4','s_sryobinum','s_srsalesdate']

        # フォーム生成クラスのインスタンス作成
        fgclass = common.FormGenerater(request,sessionkeylst)

        # セッション情報の取得
        for row in sessionkeylst:
            fgclass.session_check(row)

        # 日付クラスのインスタンス作成
        dtcmn = common.DateCalccmn(fgclass.sessiondict["s_srsalesdate"])
        # 曜日
        yobi = dtcmn.yobiget()

        # 曜日チェックボックス
        if fgclass.sessiondict["s_sryobinum"] == '':
            # セッションに値がない場合
            # 本日日付の曜日を設定
            fgclass.sessiondict.update({"s_sryobinum": str(dtcmn.yobinumget(-1))})
            # 本日日付を設定
            fgclass.sessiondict.update({"s_srsalesdate": dtcmn.dateformcnv1()})
        else:
            fgclass.sessiondict.update({"s_sryobinum": fgclass.sessiondict["s_sryobinum"].split(',')})
                
        # 日付チェック
        

        #　共通フォーム１の設定
        fgclass.common1_formset()
        # 販売実績専用フォームの設定
        fgclass.saler_formset()

        context = {}
        context = {
            'kyotenvalue': fgclass.cform_kyoten,
            'ckmvalue' : fgclass.cform_ckm,
            'hinvalue' : fgclass.cform_hintb,
            'yobivale': yobi,
            'kako4value':fgclass.srform_kako4,
            'checboxvalue':fgclass.srform_wckb,
            'clndr':fgclass.srform_clndr
        }

        return render(request, 'salesResult.html', context)

def szi_salesR(request):
    
    SalesResultView.as_view()

