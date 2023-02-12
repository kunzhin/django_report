function json_to_select(url, select_selector) {
    $.getJSON(url, function(data) {
        let opt = $(select_selector);
        opt.html('');
        $.each(data, function () {
            opt.append($('<option/>').attr('id', this.id).val(this.id).text(this.value));
        });
    });
}

function json_to_select_esr_tt(url, select_selector) {
    $.getJSON(url, function(data) {
        let opt = $(select_selector);
        opt.html('');
        $.each(data, function () {
            opt.append($('<option/>').attr('id', this.id).val(this.value).text(this.value));
        });
    });
}


$(function(){
    console.log($(this).attr('id'))
    json_to_select('json/' + $(this).val(), '#id_esr');

    $('#id_esr').change(function(){
        $('#id_address option').remove()
        if ($(this).val() !== null ) {
            json_to_select_esr_tt('json/?id_esr=' + $(this).find('option:selected').attr('id'), '#id_tt');
        }
    });

    $('#id_tt').change(function(){
        if ($(this).val() !== null ) {
            json_to_select_esr_tt('json/?id_tt=' + $(this).find('option:selected').attr('id'), '#id_address');
        }
    });
});
