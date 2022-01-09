   // 時間帯番号
   // 1	   8:00 ～  9:00
   // 2	   9:00 ～ 10:00
   // 3	  10:00 ～ 11:00
   // 4	  11:00 ～ 12:00
   // 5	  12:00 ～ 13:00
   // 6	  13:00 ～ 14:00
   // 7	  14:00 ～ 15:00
   // 8	  15:00 ～ 16:00
   // 9	  16:00 ～ 17:00
   // 10	17:00 ～ 18:00
   // 11	18:00 ～ 19:00
   // 12	19:00 ～ 20:00
   // 13	20:00 ～ 21:00
   // 14	21:00 ～ 22:00
   // 15	22:00 ～ 23:00
   // 16	23:00 ～  0:00
   // 17	 0:00 ～  1:00
   // 18	 1:00 ～  2:00

let result;
jQuery(document).ready(function()
{
  jQuery("#salesRid").addClass("btnslectcolor");

  // GETパラメータの取得

  // 曜日の色を変更
  yobicolor("sledtstrlabel")

  // 初期表示
  data_load(Getparamset());
});

function Getparamset(){
    // 店舗
    var Ktnval = $("#Select_ktnId").val()

    // 調達方法
    var CkmVal = $("#Select_ckmId").val();

    // 商品
    var HinVal = $("#Hin_dtId").val();

    // 日付
    var DateVal = $("#sledtlabel").val()

    // 過去1～4週
    var KakowVal = $("#kako4_Id").val()

    // 曜日チェックボックス
    const yobicklst = [];
    yobicklst.length = 0;
    $(':checkbox[name="weekckbx"]:checked').each(function () {
      yobicklst.push($(this).val());
    });

    const params = { // 渡したいパラメータをJSON形式で書く
      ktn: Ktnval ,
      ckm: CkmVal ,
      hin: HinVal ,
      date: DateVal,
      kk4w: KakowVal,
      ybckl: yobicklst
    };

    const query_params = new URLSearchParams(params);

    return query_params
}

$(function() {

  // 日付ラベルid
  var ymdlabelid = "sledtlabel"
  // 曜日ラベルid
  var yobilabelid = "sledtstrlabel"
  // 曜日チェックボックスidの前方
  var idparents = 'id_weekckbx_';

  // 前月ボタンクリック時
  $('#sleltmnth').on('click', function() {
    var dtnum = $("#sleltmnth").val()
    dtcalc(dtnum,ymdlabelid,yobilabelid)
    valueChangeEvent()
  });
  // 前週ボタンクリック時
  $('#sleltweek').on('click', function() {
    var dtnum = $("#sleltweek").val()
    dtcalc(dtnum,ymdlabelid,yobilabelid)
    valueChangeEvent()
  });

  // 前日ボタンクリック時
  $('#sleltday').on('click', function() {
    var dtnum = $("#sleltday").val()
    dtcalc(dtnum,ymdlabelid,yobilabelid)
    valueChangeEvent()
  });

  // 今日ボタンクリック時
  $('#sletdday').on('click', function() {
    var dtnum = $("#sletdday").val()
    dtcalc(dtnum,ymdlabelid,yobilabelid)
    valueChangeEvent()
  });

  // 翌日ボタンクリック時
  $('#slenxtday').on('click', function() {
    var dtnum = $("#slenxtday").val()
    dtcalc(dtnum,ymdlabelid,yobilabelid)
    valueChangeEvent()
  });

  // 翌週ボタンクリック時
  $('#slenxtweek').on('click', function() {
    var dtnum = $("#slenxtweek").val()
    dtcalc(dtnum,ymdlabelid,yobilabelid)
    valueChangeEvent()
  });

  // 翌月ボタンクリック時
  $('#slenxtmnth').on('click', function() {
    var dtnum = $("#slenxtmnth").val()
    dtcalc(dtnum,ymdlabelid,yobilabelid)
    valueChangeEvent()
  });

  // カレンダー変更時
  $("#sledtlabel").change(function() {

    var date = new window.Date($("#" + ymdlabelid).val());
    var dayOfWeek = date.getDay() ;

    // 曜日更新
    yobiupdate(dayOfWeek,yobilabelid)
    
    // 曜日の色を変更
    yobicolor(yobilabelid)

    valueChangeEvent()
  });

  // 商品検索ボックス変更時
  $("#Hin_dtId").change(function() {
    valueChangeEvent()
  });

  // セレクトボックス変更時
  $("select").change(function() {
    valueChangeEvent()
  });

  // 全選択ボタン押下時
  $('#slezenselectid').on('click', function() {
    yobi_allcheckd(idparents)
    valueChangeEvent()
  });

  // 同曜日ボタン押下時
  $('#slesameyobiid').on('click', function() {
    yoni_singlecheckd(idparents,yobilabelid)
    valueChangeEvent()
  });

  // チェックボックスの値変更時
  $('input[id^=' + idparents + ']').change(function() {
    if (yobicheckbox_check(idparents,this)){
      valueChangeEvent()
    }
  });

  function valueChangeEvent(){

    $("#list").GridUnload(); // 表を削除
    data_load(Getparamset());

  }

});


// 表示データ
// graph: 定価販売数量,値下30%未満販売数量,値下30%以上販売数量,廃棄数量
//var dt = [
// {graph:"100,0,0,0", hinnm:"りんご,0215456555551", bunrui:"大", saleskngsu:"24510,15", nebikiritu:"12.0", 
// time3:0,time4:0, time5:0, time6:0, time7:0, time8:0, time9:0,
//  time10:0, time11:0, time12:0, time13:0, time14:0, time15:0, time16:1 }
//];

function data_load(query_params){

  fetch("/menu/salesResult/data/load?" + query_params)
  .then((response) => {
      return response.json()　// ここでサーバからJSONを取得
  })
  .then((data) => {
    //表示設定
    $("#list").jqGrid({
      data: data,
      datatype: 'local',
      colNames:['内訳', 'JANコード<br/>商品名',"分類","販売金額<br/>販売点数",'値引率','~11', '12'
      , '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '0~'],
      colModel:[
        {index:'graph', name:'graph', width:'200px', align:'center', formatter:utiwakegraph}  //フォーマッタ―
        ,{index:'hinnm', name:'hinnm', width:'300px', align:'left', formatter:hinjan_cellvalue}
        ,{index:'bunrui', name:'bunrui', width:'50px', align:'center',formatter:bunrui_cellvalue}
        ,{index:'saleskngsu', name:'saleskngsu', width:'100px', align:'right', formatter:kngsu_cellvalue}
        ,{index:'nebikiritu', name:'nebikiritu', width:'80px', align:'right',  formatter:nsg_cellvalue}
        ,{name:'time3', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time4', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time5', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time6', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time7', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time8', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time9', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time10', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time11', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time12', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time13', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time14', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time15', width:'40px', align:'center', formatter:lastsales_cellvalue}
        ,{name:'time16', width:'40px', align:'center', formatter:lastsales_cellvalue}
      ],
      rowNum : 20,
      rowList : [10,20, 50, 100],
      height : 500,
      pager : 'pager1',
      cmTemplate: {sortable:false},
      loadComplete: function() {
        var rowIDs = jQuery("#list").getDataIDs(); 
        for (var i=0;i<rowIDs.length;i=i+1){ 
          rowData=jQuery("#list").getRowData(rowIDs[i]);
          var trElement = jQuery("#"+ rowIDs[i],jQuery('#list'));
          if (rowData["bunrui"] != "") { 
              trElement.addClass('font1');
          }
        }
      }
      });

    //タイトル結合設定
    $("#list").jqGrid('setGroupHeaders',{
      useColSpanStyle: true
    ,groupHeaders:[
        {startColumnName: 'time3', numberOfColumns: 14, titleText: '最終販売時間'}
      ]
    });

    //リサイズ時イベント
    $(window).bind('resize', function(){
      // 画面全体 - メニューエリア - 50
      $('#list').setGridWidth($(window).width() - document.getElementById('menuariaid').clientWidth - 50);
      $('#list').setGridHeight($(window).height() - document.getElementById('headerid').clientHeight - document.getElementById('salesr_headid').clientHeight - 100);
    }).trigger('resize');


  })
  .catch((e) => {
    console.log(e)  // エラーをキャッチし表示     
  })
}

 // 内訳グラフ
function utiwakegraph(cval, opt, rdt){
    var percentage = cval.split(',');
    // ある数 ÷ 全体 ×100
    //　全体数量
    var zensuryo = 0
    for (  var i = 0;  i < percentage.length;  i++  ) {
      zensuryo = zensuryo + Number(percentage[i])
    }
    
    // 定価販売数量パーセンテージ
    teikaper = Number(percentage[0]) / zensuryo * 100
    // 値下30%未満販売数量パーセンテージ
    mimanper = Number(percentage[1]) / zensuryo * 100
    // 値下30%以上販売数量パーセンテージ
    ijyouper = Number(percentage[2]) / zensuryo * 100
    // 廃棄数量パーセンテージ
    haikiper = Number(percentage[3]) / zensuryo * 100
    
    // 0％の場合
    if (isNaN(teikaper) && isNaN(mimanper) && isNaN(ijyouper) && isNaN(haikiper)){
      var str = "<div class=\"padl5r5\"><div class=\"container grpltmr grprgtmr\">"
    }else{
      var str = "<div class=\"padl5r5\"><div class=\"container ctnsdw grpltmr grprgtmr\">"
    }
    
    // 定価
    if(Number(teikaper) > 0){
      str = str + "\
      <div title=\"定価 " + percentage[0] + "\" class=\"item blue grpltmr\" style=\"width:" + teikaper + "%\">\
      <span class=\"item_label\"></span>\
      </div>"
    }

    // 値下げ30%未満
    if(Number(mimanper) > 0){
      str = str + "\
      <div title=\"値下げ30%未満 " + percentage[1] + "\" class=\"item yellow\" style=\"width:" + mimanper + "%\">\
      <span class=\"item_label\"></span>\
      </div>"
    }

    // 値下げ30%以上
    if(Number(ijyouper) > 0){
      str = str + "\
      <div title=\"値下げ30%以上 " + percentage[2] + "\" class=\"item orange\" style=\"width:" + ijyouper + "%\">\
      <span class=\"item_label\"></span>\
      </div>"
    }

    // 廃棄
    if(Number(haikiper) > 0){
      str = str + "\
      <div title=\"廃棄 " + percentage[3] + "\" class=\"item pink grprgtmr\" style=\"width:" + haikiper + "%\">\
      <span class=\"item_label\"></span>\
      </div>"
    }

    str = str + "</div></div>"

    return str;
 }
 
  // 値下げ金額
  function nsg_cellvalue(cellvalue){
    if (cellvalue == "0.0"){
      str = ""
    }else{
      str = cellvalue + "%"
    }
    return str   
  }

  // 分類
  function bunrui_cellvalue(cval, opt, rdt){
    
    if (cval == ""){
      str = ""
    }else{
      var mid = rdt["brgkrng"].split(',')[0];
      var lg = rdt["brgkrng"].split(',')[1];

      if (lg == '0'){
        str = "<span title=\"小： ～" + mid + "円&#10;中：" + String(Number(mid)+1) + "円～\">" + cval + "<\/span>"
      }else{
        str = "<span title=\"小： ～" + mid + "円&#10;中：" + String(Number(mid)+1) + "～" + lg + "円&#10;大：" + String(Number(lg)+1) + "円～\">" + cval + "<\/span>"
      }
      
    }
    return str
  }

 // 色指定
 function cellColor(rowId, value, rawObject, cm, rdata){
   return "style='background-color: #ff000012'";
 }


// 商品名、JANコード
function hinjan_cellvalue(rowId, value, rawObject, cm, rdata){

  var hinnm = rawObject["hinnm"].split(',')[0];
  var jan = rawObject["hinnm"].split(',')[1];
  // return jan + "<br/>" + hinnm;
  return jan + "<br/>" + hinnm;
}

// 販売金額、点数
function kngsu_cellvalue(rowId, value, rawObject, cm, rdata){

  var saleskng = rawObject["saleskngsu"].split(',')[0];
  var salessu = rawObject["saleskngsu"].split(',')[1];
  return new Intl.NumberFormat('ja', {
    style: 'currency',
    currency: 'JPY',
    currencyDisplay: 'name'}).format(saleskng) + "<br/>" + parseFloat(salessu).toFixed(1) + "点";
}

// 最終販売時刻
function lastsales_cellvalue(cellvalue, options, cellobject){
  // 1: ～30分
  // 2: 31分～
  if(cellvalue == 1){
    rtnval = "<div class=\"item_label pink w10h10_p\"><div class=\"markmidle\">〇</div></div>"
  }else{
    rtnval = ""
  }
  return rtnval;
}
