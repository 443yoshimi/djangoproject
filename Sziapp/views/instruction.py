from django.shortcuts import render
from django.views import View
from . import common
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class HinCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):

        # セッション情報の定義
        sessionkeylst = ['s_instkyoten','s_instckm','s_insthincat','s_instcalender']
        

        # フォーム生成クラスのインスタンス作成
        fgclass = common.FormGenerater(request,sessionkeylst)


        # セッション情報の取得
        for row in sessionkeylst:
            fgclass.session_check(row)

        # 日付クラスのインスタンス作成
        dtcmn = common.DateCalccmn(fgclass.sessiondict["s_instcalender"])
        # 曜日
        yobi = dtcmn.yobiget()
        
        if fgclass.sessiondict["s_instcalender"] == '':
            # 日付が入っていない場合設定する
            fgclass.sessiondict.update({"s_instcalender": dtcmn.dateformcnv1()})

        # 作業計画書専用フォームの設定
        fgclass.instruct_fromset()

        context = {
            'kyoten': fgclass.cform_kyoten,
            'ckmethtod' : fgclass.cform_ckm,
            'hincat': fgclass.cform_hincat,
            'calender' : fgclass.srform_clndr,
            'yobivale': yobi
        }

        return render(request, 'instruction.html', context)



#製造指図書
def szi_instR(request):

    sample_choice_view = HinCategoryView.as_view()
    
