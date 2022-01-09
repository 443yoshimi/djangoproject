// 曜日チェックボックスを全選択
function yobi_allcheckd(parents){
    // 曜日チェックボックスを取得（id前方一致検索）
    $('input:checkbox[id^=' + parents + ']').prop('checked',true);
}

// 同曜日の曜日チェックボックス選択
function yoni_singlecheckd(parents,yobilabel){
    // 曜日チェックボックスを取得（id前方一致検索）
    var result = $('input[id^=' + parents + ']');
    // 曜日を取得
    var yobi = $("#" + yobilabel).text()

    // 0：月曜日　6：月曜日
    yobinum = yobi.replace('月', 0).replace('火', 1).replace('水', 2).replace('木', 3).replace('金', 4).replace('土', 5).replace('日', 6)

    // チェックボックス全外し
    $('input:checkbox[id^=' + parents + ']').prop('checked',false);

    // チェック
    $('[id=' + result[yobinum].id + ']').prop('checked', true)
}

// 曜日チェックボックスは必ずチェック
function yobicheckbox_check(parents,thisvalue){
  // 曜日チェックボックスの選択がなくなった場合
  if ($('input:checkbox[id^=' + parents + ']:checked').length == 0){
    // 今クリックしたチェックボックスをクリック
    jQuery(thisvalue).prop('checked',true)
    return false
  }
  return true
}


// 日付計算
function dtcalc(dtnum,dtlabel,dtstrlabel){
  if (dtnum == "0") {
    // 0 本日ボタンクリック時
    var date = new window.Date();
  }else{
    var date = new window.Date($("#" + dtlabel).val());

    if (dtnum == "1"){
      // 1 前日ボタンクリック時
      date = new window.Date(date.setDate(date.getDate() - 1));
    }else if (dtnum == "2"){
      // 2 前週ボタンクリック時
      date = new window.Date(date.setDate(date.getDate() - 7));
    }else if (dtnum == "3"){
      // 3 前月ボタンクリック時
      date = new window.Date(date.getFullYear(), date.getMonth()-1, date.getDate());
    }else if (dtnum == "4"){
      // 4 翌日ボタンクリック時
      date = new window.Date(date.setDate(date.getDate() + 1));
    }else if (dtnum == "5"){
      // 5 翌週ボタンクリック時
      date = new window.Date(date.setDate(date.getDate() + 7));
    }else if (dtnum == "6"){
      // 6 翌月ボタンクリック時
      date = new window.Date(date.getFullYear(), date.getMonth()+1, date.getDate());
    }
  }

  var Year = date.getFullYear();
  var Month = ("0"+(date.getMonth()+1)).slice(-2);
  var Date = ("0"+(date.getDate())).slice(-2);
  var dayOfWeek = date.getDay() ;

  // 日付更新
  dateupdate(dtlabel,Year,Month,Date)

  // 曜日更新
  yobiupdate(dayOfWeek,dtstrlabel)
  
  // 曜日の色を変更
  yobicolor(dtstrlabel)
}

// 日付更新
function dateupdate(dtlabel,Year,Month,Date){
  $("#" + dtlabel).val(Year + "-" + Month + "-" + Date);
}

function yobiupdate(dayOfWeek,dtstrlabel){

  var dayOfWeekStr = [ "日", "月", "火", "水", "木", "金", "土" ][dayOfWeek];
  
  $("#" + dtstrlabel).text(dayOfWeekStr);
}

function yobicolor(dtstrlabel){
  
  // 曜日の色変更

  // 曜日を取得
  var yobi = $("#" + dtstrlabel).text()
  $('#' + dtstrlabel).removeClass('font-blue').removeClass('font-red');
  if(yobi == "土"){
    $('#' + dtstrlabel).addClass('font-blue');
  }else if(yobi == "日"){
    $('#' + dtstrlabel).addClass('font-red');
  }
};


$(function() {
  let dateFormat = 'yy年mm月dd日';
  $( "#Calender_dtId" ).datepicker(
    {
      dateFormat: dateFormat,
      language:'ja'
    }
  );
});

$(function() {
  let dateFormat = 'yy-mm-dd';
  $( "#sledtlabel" ).datepicker(
    {
      language:'ja',
      dateFormat: dateFormat,    
    }
  );
});

$(function() {
  let dateFormat = 'yy-mm-dd';
  $( "#discdtlabel-from" ).datepicker(
    {
      language:'ja',
      dateFormat: dateFormat,    
    }
  );
});

$(function() {
  let dateFormat = 'yy-mm-dd';
  $( "#discdtlabel-to").datepicker(
    {
      language:'ja',
      dateFormat: dateFormat,    
    }
  );
});

// 処理中
function loadingstart(){
  var h = $('#v-pills-tabContent').height();
  $('#loader-bg').removeClass('disp-none');
  $('#gbox_list').addClass('disp-none');
  $('#loader-bg ,#loader').height(h).css('display','block');
  $('#loader-bg').css('position', 'absolute');
}

function loadingstop(){
  $('#loader-bg').addClass('disp-none');
  $('#gbox_list').removeClass('disp-none');
  $('#loader-bg').delay(900).fadeOut(800);
  $('#loader').delay(600).fadeOut(300);
}

$(function(){
  
  var rotation = function (){　/* 一定の速度（早く）で回転をし続ける */
    $("#img").rotate({
      angle:0,
      animateTo:360,
      callback: rotation,
      easing: function (x,t,b,c,d){        // t: current time, b: begInnIng value, c: change In value, d: duration
        return c*(t/d)+b;
      }
    });
  }
  rotation();
});
