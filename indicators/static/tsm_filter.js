$(function (){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $('button[name="btn_tsm_filter"]').click(function (event){
        event.preventDefault();
        
        $('#esr_block').hide();
        $.ajax({
            header: {'X-CSRFToken': csrftoken},
            type: 'GET',
            url: 'terr_filter/',
            data: {'tsm': this.id},
            success: function (answer){
                $('#esr_block').html(answer).fadeIn(500);
            },
            error: function (error){
                $("#loading").addClass('d-none');
                alert('error; ' + eval(error));
            }
        })
    })
    $('button[name="btn_tsm"]').click(function(event){
        event.preventDefault();

        $('#esr_block').hide();

        $("#loading").removeClass('d-none');
        var start_day = $('#start_date').val()
        var end_day = $('#end_date').val()
        let url = $('input[type=radio][name="ind_sidebar"]:checked').val();

        if (!!!url) {
            url = 'data'
        }

        let path = window.location.pathname
        $.ajax({
            header: {'X-CSRFToken': csrftoken},
            type: 'GET',
            url: path + url + '/',
            data: {'tsm': this.value, 'start_day': start_day, 'end_day': end_day},
            success: function (answer){
                $("#loading").addClass('d-none');
                if (answer.message){
                    alert(answer.message)
                }  else {
                    $('#block_content').html(answer).fadeIn(500);
                }
            },
            error: function (error){
                $("#loading").addClass('d-none');
                alert('error; ' + eval(error));
            }
        })
    })
})