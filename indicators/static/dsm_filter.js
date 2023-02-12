$(function (){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $('button[name="btn_dsm_filter"]').click(function (event){
        event.preventDefault();
        
        $('#tsm_block').hide();
        $('#esr_block').hide();
        $.ajax({
            header: {'X-CSRFToken': csrftoken},
            type: 'GET',
            url: 'terr_filter/',
            data: {'dsm': this.id},
            success: function (answer){
                $('#tsm_block').html(answer).fadeIn(500);
            },
            error: function (error){
                $("#loading").addClass('d-none');
                alert('error; ' + eval(error));
            }
        })
    })

    $('button[name="btn_dsm"]').click(function(event){
        event.preventDefault();

        $('#tsm_block').hide();
        $('#esr_block').hide();

        $("#loading").removeClass('d-none');
        var start_day = $('#start_date').val()
        var end_day = $('#end_date').val()
        let url = $('input[type=radio][name="ind_sidebar"]:checked').val();

        if (!!!url) {
            url = 'data'
        }
        if (url === 'info_tt'){
            let data = 'dsm=' + this.value;
            let request = new XMLHttpRequest();
            request.open('POST', url + '/', true);
            request.setRequestHeader('X-CSRFToken', csrftoken)
            request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
            request.responseType = 'blob';

            request.onload = function (e) {
                if (this.status === 200) {
                    let filename = "";
                    let disposition = request.getResponseHeader('Content-Disposition');
                    // check if filename is given
                    if (disposition && disposition.indexOf('attachment') !== -1) {
                        let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                        let matches = filenameRegex.exec(disposition);
                        if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
                    }
                    let blob = this.response;
                    if (window.navigator.msSaveOrOpenBlob) {
                        window.navigator.msSaveBlob(blob, filename);
                    }
                    else {
                        let downloadLink = window.document.createElement('a');
                        let contentTypeHeader = request.getResponseHeader("Content-Type");
                        downloadLink.href = window.URL.createObjectURL(new Blob([blob], {type: contentTypeHeader}));
                        downloadLink.download = filename;
                        $("#loading").addClass('d-none');
                        document.body.appendChild(downloadLink);
                        downloadLink.click();
                        document.body.removeChild(downloadLink);
                    }
                } else {
                    $("#loading").addClass('d-none');
                    alert('Download failed.')
                }
            };

            request.send(data);
        }
        else{
            let path = window.location.pathname
            $.ajax({
                header: {'X-CSRFToken': csrftoken},
                type: 'GET',
                url: path + url + '/',
                data: {'dsm': this.value, 'start_day': start_day, 'end_day': end_day},
                success: function (answer){
                        $("#loading").addClass('d-none');
                        $('#block_content').html(answer).fadeIn(500);
                },
                error: function (error){
                    $("#loading").addClass('d-none');
                    alert('error; ' + eval(error));
                }
            })
        }
    })
})