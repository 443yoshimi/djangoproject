let result;
jQuery(document).ready(function()
{
  jQuery("#disCid").addClass("btnslectcolor");

  // 表示データ
  // nesagekng: 値下げ金額合計,値下げ金額合計最大値
  // hin: 商品名,JANコード,小中大
  // nesageritu: 値下げ率
  //var dt = [
  //  {nesagekng:"1002,1002",hin:"たこ焼き,021546800000,大",nesageritu:10}
  //];

  // 曜日の色を変更
  yobicolor("discdtstrlabel-from")
  yobicolor("discdtstrlabel-to")
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

  // 日付from
  var DateValFrom = $("#discdtlabel-from").val()

  // 日付to
  var DateValTo = $("#discdtlabel-to").val()

  const params = { // 渡したいパラメータをJSON形式で書く
    ktn: Ktnval ,
    ckm: CkmVal ,
    hin: HinVal ,
    datef: DateValFrom,
    datet: DateValTo
  };

  const query_params = new URLSearchParams(params);

  return query_params
}

$(function() {

  // 日付ラベルid - from
  var ymdlabelidfrom = "discdtlabel-from"
  // 曜日ラベルid - from
  var yobilabelidfrom = "discdtstrlabel-from"
  // 日付ラベルid - from
  var ymdlabelidto = "discdtlabel-to"
  // 曜日ラベルid - from
  var yobilabelidto = "discdtstrlabel-to"

  // 前月ボタンクリック時
  $('#discltmnth').on('click', function() {
    var dtnum = $("#discltmnth").val()
    dtcalc(dtnum,ymdlabelidfrom,yobilabelidfrom)
    dtcalc(dtnum,ymdlabelidto,yobilabelidto)
    valueChangeEvent()
  });
  // 前週ボタンクリック時
  $('#discltweek').on('click', function() {
    var dtnum = $("#discltweek").val()
    dtcalc(dtnum,ymdlabelidfrom,yobilabelidfrom)
    dtcalc(dtnum,ymdlabelidto,yobilabelidto)
    valueChangeEvent()
  });

  // 前日ボタンクリック時
  $('#discltday').on('click', function() {
    var dtnum = $("#discltday").val()
    dtcalc(dtnum,ymdlabelidfrom,yobilabelidfrom)
    dtcalc(dtnum,ymdlabelidto,yobilabelidto)
    valueChangeEvent()
  });

  // 今日ボタンクリック時 from
  $('#disctdday-from').on('click', function() {
    var dtnum = $("#disctdday-from").val()
    dtcalc(dtnum,ymdlabelidfrom,yobilabelidfrom)
    valueChangeEvent()
  });

  // 今日ボタンクリック時 to
  $('#disctdday-to').on('click', function() {
    var dtnum = $("#disctdday-to").val()
    dtcalc(dtnum,ymdlabelidto,yobilabelidto)
    valueChangeEvent()
  });

  // 翌日ボタンクリック時
  $('#discnxtday').on('click', function() {
    var dtnum = $("#discnxtday").val()
    dtcalc(dtnum,ymdlabelidto,yobilabelidto)
    dtcalc(dtnum,ymdlabelidfrom,yobilabelidfrom)
    valueChangeEvent()
  });

  // 翌週ボタンクリック時
  $('#discnxtweek').on('click', function() {
    var dtnum = $("#discnxtweek").val()
    dtcalc(dtnum,ymdlabelidto,yobilabelidto)
    dtcalc(dtnum,ymdlabelidfrom,yobilabelidfrom)
    valueChangeEvent()
  });

  // 翌月ボタンクリック時
  $('#discnxtmnth').on('click', function() {
    var dtnum = $("#discnxtmnth").val()
    dtcalc(dtnum,ymdlabelidto,yobilabelidto)
    dtcalc(dtnum,ymdlabelidfrom,yobilabelidfrom)
    valueChangeEvent()
  });

  // カレンダー変更時
  $("#discdtlabel-from").change(function() {
    var date = new window.Date($("#" + ymdlabelidfrom).val());
    var dayOfWeek = date.getDay() ;

    // 曜日更新
    yobiupdate(dayOfWeek,yobilabelidfrom)
    
    // 曜日の色を変更
    yobicolor(yobilabelidfrom)

    valueChangeEvent()
  });

  // カレンダー変更時
  $("#discdtlabel-to").change(function() {
    var date = new window.Date($("#" + ymdlabelidto).val());
    var dayOfWeek = date.getDay() ;

    // 曜日更新
    yobiupdate(dayOfWeek,yobilabelidto)
    
    // 曜日の色を変更
    yobicolor(yobilabelidto)

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



  function valueChangeEvent(){

    $("#list").GridUnload(); // 表を削除
    data_load(Getparamset());
  }
});

function data_load(query_params){
  fetch("/menu/discount/data/load?" + query_params)
  .then((response) => {
      return response.json()　// ここでサーバからJSONを取得
  })
  .then((data) => {
  //表示設定
    $("#list").jqGrid({
      data: data,
      datatype: 'local',
      colNames:['値下額（合計）', '商品名<br/>JANコード','値下率（平均）'],
      colModel:[
        {index:'nesagekng', name:'nesagekng', width:'100px',title: false ,align:'center', sorttype: 'int',formatter:nsg_kng_graph}  //値下げ金額
        ,{index:'hin', name:'hin', width:'200px',title: false , align:'left', sorttype: 'int',
        sorttype: function(cell) {
          var str = cell;
          // JANコード取り出し
          str = str.split(',')[1];
          return str},
          formatter:hinjan_cellvalue} // 商品名
        ,{index:'nesageritu', name:'nesageritu', width:'100px', align:'center',title: false , sorttype: 'int',formatter:nsg_ritu_graph} // 値下げ率
      ],
      rowNum : 20,
      rowList : [10,20, 50, 100],
      height : 500,
      pager : 'pager1'
    });

      //リサイズ時イベント
    $(window).bind('resize', function(){
      // 画面全体 - メニューエリア - 50
      $('#list').setGridWidth($(window).width() - document.getElementById('menuariaid').clientWidth - 50);
      // 画面高さ - ヘッダー高さ - 条件ヘッダー高さ - 100
      $('#list').setGridHeight($(window).height() - document.getElementById('headerid').clientHeight - document.getElementById('discnt_headid').clientHeight - 100);
    }).trigger('resize');
  });
}
 
 // 値下げ額グラフ
function nsg_kng_graph(cval, opt, rdt){
  var percentage = cval.split(',');
  
  // グラフ金額
  graphper = Number(percentage[0])
  graphpermax = Number(percentage[1])
  
  // パーセンテージの算出
  per1 = Number((graphper / graphpermax) * 100)
  per2 = 100 - per1
  
  str = "<div class=\"padl5r5 bunkatu1\"><div class=\"container grpltmr grprgtmr\">\
  <div class=\"white\" style=\"width:" + per2 + "%\">\
  <span class=\"item_label\"></span>\
  </div>"
  
  str = str + "\
  <div class=\"orange2 ctnsdw\" style=\"width:" + per1 + "%\">\
  <span class=\"item_label\"></span>\
  </div></div></div>"

  str = str + "<div class=\"bunkatu2\">" + new Intl.NumberFormat('ja', {
    style: 'currency',
    currency: 'JPY',
    currencyDisplay: 'name'}).format(graphper) + "</div>"
  
  return str;
}


// 商品名、JANコード、分類
function hinjan_cellvalue(rowId, value, rawObject, cm, rdata){

  var hinnm = rawObject["hin"].split(',')[0];
  var jan = rawObject["hin"].split(',')[1];
  var bunrui = rawObject["hin"].split(',')[2];
  
  str = "<div class=\"bunkatu1\">" +  hinnm + "<br/>" + jan + "</div>\
         <div class=\"bunkatu2\">" + bunrui + "</div>"
         
  return str;
}



 // 値下げ率グラフ
function nsg_ritu_graph(cval, opt, rdt){
  var per1 = cval;
  var per2 = 100 - per1
 
  var str = "<div class=\"bunkatu2\">" + parseFloat(per1).toFixed(1) + "%</div>"
  
  str = str + "<div class=\"padl5r5 bunkatu1\"><div class=\"container grpltmr grprgtmr\">\
  <div class=\"yellow2 ctnsdw_2\" style=\"width:" + per1 + "%\">\
  <span class=\"item_label\"></span>\
  </div>"
  
  str = str + "\
  <div class=\"white\" style=\"width:" + per2 + "%\">\
  <span class=\"item_label\"></span>\
  </div></div></div>"
      
  return str;

}