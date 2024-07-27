function printTime() {
    window.setInterval(function() {
        var date = new Date();
        var hours = date.getHours();
        var minute = date.getMinutes();
        var clock = hours + ':' + minute;
        document.getElementById('clock').innerHTML = clock;
    }
    );
}

printTime()