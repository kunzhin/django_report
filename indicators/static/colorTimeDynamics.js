$(
    function (){
        // Получаем значение текущей динамики времени, переводим в float формат
        let dTime = parseFloat($('.progress-bar').text().replace('%',''))
        const array = ['TOTAL', 'ИТОГО']
        let fChild;

       $('td').each(function (){
           // Проверяем id таблицы, если объем, берем на проверку значение 2го столбца, иначе 1й
           if ($(this).parent().parent().parent().attr('id') === 'volume_table'){
                fChild = $(this).parent().children().eq(1).text();
           } else {
                fChild = $(this).parent().children().eq(0).text();
           }
            // Проверяем ячейки на вхождение "%", является ли строка со значением ТОТАЛ и длина менее 8ми символов
            if (($(this).text().indexOf('%') !== -1) && ($.inArray(fChild, array) === -1 ) && ($(this).text().length < 8)){
                // Преобразуем значение ячейки в float, убимраем пробелы(на случай выполнения более 1000%)
                let numFloat = parseFloat($(this).text().replace('%', '').replace(/\s+/g, ''))
                if (numFloat >= dTime){
                    $(this).addClass('td_in_time')
                }
                else {
                    $(this).addClass('td_not_in_time')
                }
            }
       })
    }
)