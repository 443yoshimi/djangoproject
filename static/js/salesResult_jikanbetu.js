let result;
jQuery(document).ready(function()
{
  jQuery("#salesJBid").addClass("btnslectcolor");

  // GETパラメータの取得

  // 曜日の色を変更
  yobicolor("discdtstrlabel-from")
  yobicolor("discdtstrlabel-to")
  // 初期表示
  data_load(Getparamset());
});

$(function() {

  // 日付ラベルid - from
  var ymdlabelidfrom = "discdtlabel-from"
  // 曜日ラベルid - from
  var yobilabelidfrom = "discdtstrlabel-from"
  // 日付ラベルid - to
  var ymdlabelidto = "discdtlabel-to"
  // 曜日ラベルid - to
  var yobilabelidto = "discdtstrlabel-to"

  // 曜日チェックボックスidの前方
  var idparents = 'id_weekckbx_';

  // 全選択id
  var yobilabelid = "sledtstrlabel"

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

  // 全選択ボタン押下時
  $('#slezenselectid').on('click', function() {
    yobi_allcheckd(idparents)
    valueChangeEvent()
  });

  // 同曜日ボタン押下時
  $('#slesameyobiid').on('click', function() {
    yoni_singlecheckd(idparents,yobilabelidto)
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
    datef: DateValFrom,
    datet: DateValTo,
    ybckl: yobicklst
  };

  const query_params = new URLSearchParams(params);

  return query_params
}

function data_load(query_params){

   // 表示データ
   var dt = [
    {hinnm:"りんご,0215456555551", bunrui:"大", saleskng:"24510",salessu:"15", 
    time3:2,time4:3, time5:0, time6:0, time7:0, time8:0, time9:0,
    time10:0, time11:0, time12:0, time13:0, time14:0, time15:0, time16:1, brgkrng:"200,500" },
    {hinnm:"りんご,0215456555531", bunrui:"大", saleskng:"24210",salessu:"13", 
    time3:2,time4:3, time5:0, time6:0, time7:0, time8:0, time9:0,
    time10:0, time11:0, time12:0, time13:0, time14:0, time15:0, time16:1,brgkrng:"200,0" }
  ];

  fetch("/menu/salesResultjikanbetu/data/load?" + query_params)
  .then((response) => {
      return response.json()　// ここでサーバからJSONを取得
  })
  .then((data) => {
    //表示設定
    $("#list").jqGrid({
      data: data,
      datatype: 'local',
      colNames:['JANコード<br/>商品名','分類','販売金額','販売点数','～ 11', '12'
      , '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '0 ～'],
      colModel:[
        {index:'hinnm', name:'hinnm', width:'200px', align:'left',sorttype: 'int',
        sorttype: function(cell) {
          var str = cell;
          // JANコード取り出し
          str = str.split(',')[1];
          return str
          },formatter:hinjan_cellvalue
        }
        ,{index:'bunrui', name:'bunrui', width:'40px', align:'center',formatter:bunrui_cellvalue}
        ,{index:'saleskng', name:'saleskng', width:'60px', align:'right',sorttype: 'int',formatter:hanbaikng_cellvalue}
        ,{index:'salessu', name:'salessu', width:'60px', align:'right',sorttype: 'int',formatter:hanbaisu_cellvalue}
        ,{name:'time3', width:'40px', align:'center', sorttype: 'int',formatter:gozenmax_color}
        ,{name:'time4', width:'40px', align:'center', sorttype: 'int',formatter:gozenmax_color}
        ,{name:'time5', width:'40px', align:'center', sorttype: 'int',formatter:gozenmax_color}
        ,{name:'time6', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time7', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time8', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time9', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time10', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time11', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time12', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time13', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time14', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time15', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
        ,{name:'time16', width:'40px', align:'center', sorttype: 'int',formatter:gogomax_color}
      ],
      rowNum : 20,
      rowList : [10,20, 50, 100],
      height : 500,
      pager : 'pager1'
    });

      //タイトル結合設定
      $("#list").jqGrid('setGroupHeaders',{
        useColSpanStyle: true
      ,groupHeaders:[
          {startColumnName: 'time3', numberOfColumns: 14, titleText: '時間帯別販売数'}
        ]
      });

      //リサイズ時イベント
      $(window).bind('resize', function(){
        // 画面全体 - メニューエリア - 50
        $('#list').setGridWidth($(window).width() - document.getElementById('menuariaid').clientWidth - 50);
        $('#list').setGridHeight($(window).height() - document.getElementById('headerid').clientHeight - document.getElementById('salesr_headid').clientHeight - 100);
      }).trigger('resize');
  })
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

// ～14時までの一番多い販売数を色付ける
function gozenmax_color(cellvalue, value, rawObject, cm, rdata){  
  var items = [rawObject["time3"],rawObject["time4"],rawObject["time5"]];
  // 最大値取得
  var max = Math.max(...items);
  if (max == cellvalue){
    return "<span class=\"font-red\">" + String(cellvalue) + "<\/span>"
  }else{
    return cellvalue;
  }
}
// 14時～の一番多い販売数を色付ける
function gogomax_color(cellvalue, value, rawObject, cm, rdata){  
  var items = [rawObject["time6"],rawObject["time7"],rawObject["time8"],
  rawObject["time9"],rawObject["time10"],rawObject["time11"],rawObject["time12"],
  rawObject["time13"],rawObject["time14"],rawObject["time15"],rawObject["time16"]
];
  // 最大値取得
  var max = Math.max(...items);
  if (max == cellvalue){
    return "<span class=\"font-red\">" + String(cellvalue) + "<\/span>"
  }else{
    return cellvalue;
  }
}

// 商品名、JANコード
function hinjan_cellvalue(rowId, value, rawObject, cm, rdata){

  var hinnm = rawObject["hinnm"].split(',')[0];
  var jan = rawObject["hinnm"].split(',')[1];
  // return jan + "<br/>" + hinnm;
  return jan + "<br/>" + hinnm;
}

// 販売金額
function hanbaikng_cellvalue(rowId, value, rawObject, cm, rdata){
  return new Intl.NumberFormat('ja', {
    style: 'currency',
    currency: 'JPY',
    currencyDisplay: 'name'}).format(rawObject["saleskng"]);
}

// 販売点数
function hanbaisu_cellvalue(rowId, value, rawObject, cm, rdata){
  return rawObject["salessu"] + "点";
}
