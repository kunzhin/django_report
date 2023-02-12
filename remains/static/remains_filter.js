//Функция запроса всех остатков по городу и категории продукта
$(document).ready(function (){
   $('.remains_filter').click(function (event){
       event.preventDefault();
       const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
       $('#div_table').hide()
       $("#animation_table").removeClass('d-none');
       $.ajax({
           headers: {'X-CSRFToken': csrftoken},
           type: 'POST',
           url: '/remains/',
           data: {'code_category' : this.id, 'city_name': $('.city_header').attr('id')},
           success: function (answer){
               $("#animation_table").addClass('d-none');
               $('#div_table').html(answer).fadeIn(500);
           },
           error: function (error){
                $("#animation_table").addClass('d-none');
                alert('error; ' + eval(error));
            }
       })
    })
})
