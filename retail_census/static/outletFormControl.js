function json_to_select(url, select_selector) {
    $.getJSON(url, function(data) {
        let opt = $(select_selector);
        opt.html('');
        $.each(data, function () {
            opt.append($('<option/>').attr('id', this.id).val(this.id).text(this.value));
        });
    });
}

$(function(){
    json_to_select('json/' + $(this).val(), '#id_esr')
})