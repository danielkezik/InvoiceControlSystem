function dateIconInit(due_date) {
    //Get date
    var date = new Date(due_date);
    var mm = (date.getMonth()),
        dd = ("0" + date.getDate()).slice(-2),
        day = date.getDay(),
        year = date.getFullYear();

    //Set icon text with the date data
    $('strong').html(monthToStr(mm) + ' ' + year);
    $('span').html(dd);
    $('em').html(dayToStr(day));

    //Get month as a string
    function monthToStr(data) {
        var month = new Array();
        month[0] = "January";
        month[1] = "February";
        month[2] = "March";
        month[3] = "April";
        month[4] = "May";
        month[5] = "June";
        month[6] = "July";
        month[7] = "August";
        month[8] = "September";
        month[9] = "October";
        month[10] = "November";
        month[11] = "December";
        return month[data];
    }

    //Get day as a string
    function dayToStr(data) {
        var day = new Array();
        day[0] = "Sunday";
        day[1] = "Monday";
        day[2] = "Tuesday";
        day[3] = "Wednesday";
        day[4] = "Thursday";
        day[5] = "Friday";
        day[6] = "Saturday";
        return day[data];
    }
}