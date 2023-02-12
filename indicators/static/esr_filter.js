$(function (){
    $('input[type=radio][name="btnradio_esr"]').click(function (event){
        event.preventDefault();

        $('input[type=radio][name="btnradio_tsm"]').attr('checked', false);
        $('input[type=radio][name="btnradio_esr"]').attr('checked', false);

        $(this).attr('checked', true)
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
            data: {'esr': this.value, 'start_day': start_day, 'end_day': end_day},
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