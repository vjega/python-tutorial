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