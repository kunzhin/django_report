//Функция запроса всех остатков по городу
$(document).ready(function (){
    $('button.remains_sidebar').click(function (event){
        event.preventDefault();
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const city = this.value;
        $('#block_content').hide();
        $("#loading").removeClass('d-none');
        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            type:'POST',
            url: '/remains/',
            data:{'city': city, 'id': this.id},
            success: function (answer) {
                $("#loading").addClass('d-none');
                $('title.base_title').text('Остатки ' + city);
                $('#block_content').html(answer).fadeIn(500);
            },
            error: function (error){
                $("#loading").addClass('d-none');
                alert('error; ' + eval(error));
            }
        })
    })

    $('input[type=radio][name="ind_sidebar"]').change(function (event){
        event.preventDefault();
        $('input[type=radio][name="ind_sidebar"]').prop('checked', false);
        $(this).prop('checked', true)

        let path = window.location.pathname

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $('#block_content').hide();
        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            type: 'GET',
            data: {'kpi': this.id},
            url: path + 'sidebar_filter/',
            success: function (answer) {
                $('#block_sidebar_filter').html(answer).fadeIn(500);
            },
            error: function (error){
                $("#loading").addClass('d-none');
                alert('error; ' + eval(error));
            }
        })
    })
})
