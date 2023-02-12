/* Функция преобразования даты для поля ввода даты */
function get_date(date){
    let month = (date.getMonth() + 1)
    let day = date.getDate();
    if (month < 10)
        month = "0" + month
    if (day < 10)
        day = "0" + day
    const curr_date = date.getFullYear() + '-' + month + '-' + day;
    return curr_date
}