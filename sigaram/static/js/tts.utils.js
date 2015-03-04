window.TTS = window.TTS || {};
TTS.utils = TTS.utils || {}
TTS.utils.serilaizeJson =  function (form){
    var unindexed_array = $(form).serializeArray();
    unindexed_array = unindexed_array.concat(
    $(form+' input[type=checkbox]').map(function() {
        return {"name": this.name, "value": ($(this).prop("checked") ? 1 : 0 ) }
        }).get());
    var indexed_array = {};
    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });
    $.map($(".summernote"), function(n, i){
        indexed_array[n['name']] = $(n).code();
    })
    return JSON.stringify(indexed_array);
};

TTS.utils.guid = (function() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
               .toString(16)
               .substring(1);
  }
  return function() {
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
           s4() + '-' + s4() + s4() + s4();
  };
})();

TTS.utils.getSelectionHtml =  function () {
    var html = "";
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection();
        if (sel.rangeCount) {
            var container = document.createElement("div");
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                container.appendChild(sel.getRangeAt(i).cloneContents());
            }
            html = container.innerHTML;
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            html = document.selection.createRange().htmlText;
        }
    }
    return html;
}

TTS.utils.getUrlParameter =  function (sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}

TTS.utils.ajaxloaderstart =  function (sParam) {
    //console.log('Testing ...')
    if (sParam) {
        $("#top-notification>span").html("<i class='fa fa-spinner fa-spin'></i> "+sParam);
    } else {
        $("#top-notification>span").html("<i class='fa fa-spinner fa-spin'></i> Retreiving data from server. Please wait");
    }
    $("#top-notification").css('visibility','visible');
}

TTS.utils.ajaxloaderstop =  function (sParam) {
    $("#top-notification").css('visibility','hidden');
}

TTS.utils.datetime_to_timestamp =  function (datetime){
    dateParts = datetime.split(' ');
    timeParts = dateParts[1].split(':'); 
    date = '';
    dateParts = dateParts[0].split('-');
    date = new Date(dateParts[2], parseInt(dateParts[1], 10) - 1, dateParts[0], timeParts[0], timeParts[1], timeParts[2]);
    //console.log(date.getTime()); //1379426880000
    //console.log(date); //Tue Sep 17 2013 10:08:00 GMT-0400
    return date.getTime();
}

function addZero(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

TTS.utils.timestamp_to_datetime =  function (timestamp) {
    var d = new Date(parseInt(timestamp));
    var x = addZero(d.getDate());
    var y = addZero(d.getMonth() + 1);
    var z = addZero(d.getYear() + 1900);
    var h = addZero(d.getHours());
    var m = addZero(d.getMinutes());
    var s = addZero(d.getSeconds());
    var datetime = z+"-"+y+"-"+x+" "+h+":"+m+":"+s;
        return datetime;
}


TTS.utils.dateConv =  function (str) {
        date = new Date(str);
        return date.getDate()+
            '-'+date.getMonth()+1+
            '-'+date.getFullYear();
}

TTS.utils.datetimeConv = function(dtstring){
    //2015-02-05T13:34:26Z
    var t = dtstring.split('T');
    var d = t[0].split('-')
    return d[2] +'-'+ d[1] +'-'+d[0]+
           ' '+t[1].replace('Z',''); 

};

TTS.utils.datetimeConvDate = function(dtstring){
    //2015-02-05T13:34:26Z
    var t = dtstring.split('T');
    var d = t[0].split('-')
    return d[2] +'-'+ d[1] +'-'+d[0];
};

TTS.utils.summer_encode = function (str) {
    str = str.replace("/&nbsp;/g","");
    //console.log(str);
    return str.replace(/&/g, "*")
              .replace(/:/g, "~")
              .replace(/=/g, '#')
              .replace(/;/g, '^');
}

TTS.utils.getCookie = function(name)  {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

TTS.utils.datatable_ta = {
    "emptyTable":     "அட்டவணையில் பதிவுகள் எதுவும் இல்லை",
    "info":           "_START_ இலிருந்து _END_ வரை (மொத்தம் _TOTAL_)",
    "infoEmpty":      "அட்டவணையில் பதிவுகள் எதுவும் இல்லை",
    "infoFiltered":   "(_MAX_ பதிவுகளிலிருந்து வடிகட்டப்பட்டது)",
    "infoPostFix":    "",
    "thousands":      ",",
    "lengthMenu":     "காண்க _MENU_ பதிவுகள்",
    "loadingRecords": "ஏற்றுகிறது...",
    "processing":     "செயலாக்குகிறது...",
    "search":         "தேடு:",
    "zeroRecords":    "தேடும் பதிவுகள் இல்லை",
    "paginate": {
        "first":      "முதல்",
        "last":       "கடைசி",
        "next":       "அடுத்து",
        "previous":   "முன்"
    },
    "aria": {
        "sortAscending":  ": activate to sort column ascending",
        "sortDescending": ": activate to sort column descending"
    
    }
}