from django.shortcuts import render
from django.views import View
from . import common
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class DiscountView(View):
    @method_decorator(login_required)
    def get(self, request):
    
        # セッション情報の定義
        sessionkeylst = ['s_kyoten','s_ckm','s_hintb','s_salesdatefrom','s_salesdateto']

        # フォーム生成クラスのインスタンス作成
        fgclass = common.FormGenerater(request,sessionkeylst)

        # セッション情報の取得
        for row in sessionkeylst:
            fgclass.session_check(row)

        # 日付クラスのインスタンス作成
        dtcmn = common.DateCalccmn('')
        # 初期日付計算
        dtcmn.datekeisan(-1)

        if fgclass.sessiondict["s_salesdatefrom"] == '' or fgclass.sessiondict["s_salesdateto"] == '':
            # from,to日付が入っていない場合設定する
            fgclass.sessiondict.update({"s_salesdatefrom": dtcmn.dateformcnv1()})
            fgclass.sessiondict.update({"s_salesdateto": dtcmn.dateformcnv1()})

        # FROM曜日
        yobifrom = dtcmn.inputdt_yobiget(fgclass.sessiondict["s_salesdatefrom"])
        # TO曜日
        yobito = dtcmn.inputdt_yobiget(fgclass.sessiondict["s_salesdateto"])

        #　共通フォーム１の設定
        fgclass.common1_formset()
        #　共通フォーム２の設定
        fgclass.common2_formset()

        context = {
            'kyotenvalue': fgclass.cform_kyoten,
            'ckmvalue' : fgclass.cform_ckm,
            'hinvalue' : fgclass.cform_hintb,
            'yobivalefrom': yobifrom,
            'yobivaleto': yobito,
            'clndrfrom':fgclass.cform_clndrfrom,
            'clndrto':fgclass.cform_clndrto
        }

        return render(request,'discount.html',context)

def szi_disC(request):
    
    DiscountView.as_view()
