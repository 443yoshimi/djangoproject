from django.urls import path
from .views import menu,salesResult,discount,instruction,provisionPlan
from .views import salesResult_jikanbetu,instruct_async,salesresult_async,discount_async,salesresult_jikanbetu_async

pp_name= 'Sziapp'

urlpatterns = [
    path('menu/',menu.szi_menu,name='szi_menu'),
    path('menu/instruction/',instruction.HinCategoryView.as_view(),name='szi_instR'),
    path('menu/provisionPlan/',provisionPlan.szi_provisionP,name='szi_provisionP'),
    path('menu/salesResultjikanbetu/',salesResult_jikanbetu.SalesResultjbView.as_view(),name='szi_salesJB'),
    path('menu/salesResultjikanbetu/data/load/',salesresult_jikanbetu_async.salesresultjikanbetu_load,name='salesresultjikanbetu_load'),
    path('menu/instruction/data/load/',instruct_async.instruct_load,name='instruct_load'),
    path('menu/instruction/data/update/',instruct_async.instruct_update,name='instruct_update'),
    path('menu/instruction/data/excelout/',instruct_async.instruct_excellout,name='instruct_excellout'),
    path('menu/salesResult/',salesResult.SalesResultView.as_view(),name='szi_salesR'),
    path('menu/salesResult/data/load/',salesresult_async.salesresult_load,name='salesresult_load'),
    path('menu/discount/',discount.DiscountView.as_view(),name='szi_disC'),
    path('menu/discount/data/load/',discount_async.instruct_load,name='instruct_load'),
]
