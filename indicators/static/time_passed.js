function tableColorCss(tableIdValue) {
    var table = document.getElementById(tableIdValue);

    var cells = table.getElementsByTagName('td');

    var timePassed = document.getElementsByClassName('progress-bar bg-success').innerHTML;

    timePassed = timePassed.replace('%','');

    timePassed = parseInt(timePassed, 10);

    for (var i = 0; i < cells.length; i++) {
        var value = cells[i].innerHTML;
        if (value === 'TOTAL') {
            var row = cells[i].parentNode;
            for (var k=0, td = row.children ; k < td.length; k++) {
                td[k].setAttribute('class', 'td_total');
            }
        }
        if ((value.indexOf('%') !== -1) || (value.indexOf('% Эффект') !== -1) || (value.indexOf('% Общее') !== -1) ) {
            value = value.replace('%','');
            var valueInt = parseInt(value, 10);
            if (valueInt < timePassed) {
                cells[i].setAttribute('class', 'td_not_in_time');
            }
            if (valueInt > timePassed) {
                cells[i].setAttribute('class', 'td_in_time')
            }
        }
    }
}