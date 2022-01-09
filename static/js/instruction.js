let result;
jQuery(document).ready(function()
{
  jQuery("#instRid").addClass("btnslectcolor");

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

  // カテゴリー
  var CatVal = $("#Select_catId").val();

  // 日付
  var DateVal = $("#sledtlabel").val()

  const params = { // 渡したいパラメータをJSON形式で書く
    ktn: Ktnval ,
    ckm: CkmVal ,
    hincat: CatVal ,
    date: DateVal
  };

  const query_params = new URLSearchParams(params);

  return query_params
}

$(function() {
  // 日付の取得
  $("#sledtlabel").change(function() {
    var date = new window.Date($("#sledtlabel").val());
    // 曜日更新
    yobiupdate(date.getDay(),"sledtstrlabel")
    // 曜日の色を変更
    yobicolor("sledtstrlabel")
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

  fetch("/menu/instruction/data/load?" + query_params)
    .then((response) => {
        return response.json()　// ここでサーバからJSONを取得
    })
    .then((data) => {

      var colModelset =[
        {name:'key',editable:true},
        {name:'callhin',align:"center",editable:false},
        {name:'hincd',align:"left",editable:false, width:500, formatter:hinjan_cellvalue},
        {name:'hincd',align:"left",hidden: true , editable: true,editrules: {edithidden:true}},
        {name:'hinnm',align:"left",hidden: true , editable: true,editrules: {edithidden:true} },
        {name:'spec',align:"center",editable:true,width:100},
        {name:'baik',align:"right",editable:true,width:100,sorttype: 'int'},
        {name:'tray',align:"left",editable:true},
        {name:'prod1',align:"center",editable:true,width:100,sorttype: 'int',cellattr: EditcellColor},
        {name:'prod2',align:"center",editable:true,width:100,sorttype: 'int',cellattr: EditcellColor},
        {name:'prod3',align:"center",editable:true,width:100,sorttype: 'int',cellattr: EditcellColor},
        {name:'prod4',align:"center",editable:true,width:100,sorttype: 'int',cellattr: EditcellColor},
        {name:'gokei',align:"center",width:100,sorttype: 'int'},
        {name:'sum',align:"center",width:100,sorttype: 'int'},
      ];
    jQuery("#list").jqGrid({
      data: data,
      datatype: "local",
      colNames:['','品番','商品','商品コード','商品名','規格', '本体価格','トレー' ,'朝一', '朝二', '午後一', '午後二','合計','金額'],
      colModel:colModelset,
      cellEdit: false,
      multiselect: false,
      rowNum : 20,
      rowList : [10,20, 50, 100],
      pager : 'pager1',
      regional : 'ja',
      viewrecords: true,
      ondblClickRow: function(rowid) {jQuery(this).jqGrid('editGridRow', rowid,
              {
              closeOnEscape:true,reloadAfterSubmit:false,
              height:'auto',
              modal:true,                             // モーダル表示にします。
              editCaption:"編集",                     // フォームのキャプションを設定
              bSubmit:"更新",                         // フォーム内に表示する確定ボタンのキャプション
              bCancel:"キャンセル",                   // フォーム内に表示する取消ボタンのキャプション
              reloadAfterSubmit:false,                // cellsubmit: 'clientArray'なのでサブミット後データを再読み込みしない
              beforeShowForm:function(formid) {

                  // inputのオプション追加1
                  // 商品コード、商品名、売価
                  // readonly に変更
                  // 色を変更
                  const ReadonlyArr = ['hincd', 'hinnm', 'baik','spec'];
                  ReadonlyArr.forEach(function(elem, index) {
                    $('#' + elem ,formid).attr('readonly','readonly');
                    $('#' + elem ,formid).addClass("readonlycolor")
                    $('#tr_' + elem ,formid).addClass("readonlycolor")
                  });

                  // inputのオプション追加2
                  // 午前前、昼前追加、午後追加、調整追加
                  // type:number
                  // マイナス入力不可
                  const NumberArr = ['prod1', 'prod2', 'prod3', 'prod4'];
                  NumberArr.forEach(function(elem, index) {
                    $('#' + elem ,formid).get(0).type = 'number';
                    $('#' + elem ,formid).attr('min','0');
                  });
              },
              beforeSubmit:function(postdata, formid) {
                  // 行ID
                  var rowkey = postdata['list_id'];

                  // 更新時赤色にする
                  $('#' + rowkey).addClass("upcolor")
                  // 合計数量、合計金額にクラスを追加（点滅用）
                  
                  // ポストデータの取得
                  // キー
                  var key = postdata['key'];
                  // 午前前追加
                  var prod1 = postdata['prod1'];
                  // 午前追加
                  var prod2 = postdata['prod2'];
                  // 午後追加
                  var prod3 = postdata['prod3'];
                  // 調整追加
                  var prod4 = postdata['prod4'];
                  //売価
                  var baik = postdata['baik'];

  
                  // 合計数量
                  gksu = Number(prod1) + Number(prod2) + Number(prod3) + Number(prod4)
                  // 合計金額
                  sm = Number(baik) * gksu
  
                  //編集行を更新
                  var updt = $('#list').setRowData(rowkey, {gokei : gksu, sum:sm});
                  
                  const params = { // 渡したいパラメータをJSON形式で書く
                    key: key ,
                    prod1: prod1 ,
                    prod2: prod2 ,
                    prod3: prod3 ,
                    prod4: prod4
                  };

                  const query_params = new URLSearchParams(params);
                  
                  // 更新
                  fetch('/menu/instruction/data/update?' + query_params)
                  .then(response => response.json())
                  .then(response => {
                    console.log('Success:', response);
                  });
                  
              },
              afterComplete:function(response, postdata, formid) {
                  // 編集が完了した時のイベント処理

                  // 更新時の色変更終了
                  $('#' + postdata['id']).removeClass("upcolor");
                  // 合計数量、合計金額のクラスを削除（点滅用）
                  ;
              }
            }
          );
      }
    });

    //リサイズ時イベント
    $(window).bind('resize', function(){
      // 画面全体 - メニューエリア - 50
      $('#list').setGridWidth($(window).width() - document.getElementById('menuariaid').clientWidth - 50);

      // 画面高さ - ヘッダー高さ - 条件ヘッダー高さ - 100
      $('#list').setGridHeight($(window).height() - document.getElementById('headerid').clientHeight - document.getElementById('intrdc_headid').clientHeight - 100);
    }).trigger('resize');

    $('#list').hideCol('key');
    // fillter
    //jQuery("#list").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, defaultSearch: "cn" });
  })
  .catch((e) => {
      console.log(e)  // エラーをキャッチし表示     
  })
}

$(function() {
    // エクセル出力
    $("#exellout_instruct").click(function() { 
      loadingstart()
      // 表示データの取得
      var gridoutdict = $("#list").jqGrid("getRowData")

      // 店舗をJson形式で取得
      var tenjson = {ten: $('#Select_ktnId option:selected').text()}
      // 調達方法をJson形式で取得
      var ckmjson = {ckm: $('#Select_ckmId option:selected').text()}
      // カテゴリをJson形式で取得
      var catjson = {cat: $('#Select_catId option:selected').text()}
      // 日付をJson形式で取得
      var datejson = {date: $('#sledtlabel').val()}

      // 店舗、調達方法、カテゴリ、日付を先頭に追加
      var array = [tenjson, ckmjson,catjson,datejson];
      for (var value of array) {
        gridoutdict.unshift(value) 
      }
      
      // サーバーへPOST
      const method = "POST";
      const body = JSON.stringify(gridoutdict);
      const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
      };
      fetch("./data/excelout/", {method, headers, body}).then(response => response.blob()) //blobで読み込む
      .then(blob => {
          // ファイル名に使用する日付
          let today = new Date();  
          let year = today.getFullYear();
          let month = today.getMonth() + 1;
          let date = today.getDate();
          let hour = today.getHours();
          let minute = today.getMinutes();
          let second = today.getSeconds();
        
          console.log(year + '-' + month + '-' + date + ' ' + hour + minute + second);
          //DOMでダウンロードファイルを添付したアンカー要素を生成
          let anchor = document.createElement("a");
          anchor.download = '作業計画書_' + year + month + date + '_' + hour + minute + second + '.xlsx'
          anchor.href = window.URL.createObjectURL(blob);
          //アンカーを発火
          anchor.click();
          loadingstop()
      })
      .catch(function(err) {
          console.log("err=" + err);
          loadingstop()
      });
    });
    
  });


// 色指定
function EditcellColor(rowId, value, rawObject, cm, rdata){
  return "style='background-color: #ff000012'";
}

// 商品名、JANコード
function hinjan_cellvalue(rowId, value, rawObject, cm, rdata){

  var hincd = rawObject["hincd"]
  var hinnm = rawObject["hinnm"]
  return hincd + "<br/>" + hinnm;
}
