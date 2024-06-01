$(function() {
    function fetchArduinoData() {
        $.get("/plugin/dht22_tab/arduino_data", function(data) {
            var tempMatch = data.match(/Temperatur: ([\d.]+) &deg;C/);
            var humidityMatch = data.match(/Luftfeuchtigkeit: ([\d.]+) %/);

            if (tempMatch && humidityMatch) {
                var temperature = parseFloat(tempMatch[1]);
                var humidity = parseFloat(humidityMatch[1]);

                $("#navbar_temperature").text(temperature);
                $("#navbar_humidity").text(humidity);

                addLogMessage("Data fetched successfully from Arduino.");
            } else {
                $("#navbar_temperature").text("--");
                $("#navbar_humidity").text("--");
                addLogMessage("Failed to parse data from Arduino.");
            }
        }).fail(function() {
            $("#navbar_temperature").text("--");
            $("#navbar_humidity").text("--");
            addLogMessage("Failed to fetch data from Arduino.");
        });
    }

    function addLogMessage(message) {
        var logElement = $("#dht22_log");
        var currentTime = new Date().toLocaleTimeString();
        logElement.append("<div>[" + currentTime + "] " + message + "</div>");
        logElement.scrollTop(logElement.prop("scrollHeight"));

        updateLogIframe(logElement.html());
    }

    function updateLogIframe(logContent) {
        var iframe = document.getElementById("dht22_log_iframe");
        if (iframe) {
            var doc = iframe.contentDocument || iframe.contentWindow.document;
            doc.open();
            doc.write("<html><body>" + logContent + "</body></html>");
            doc.close();
        }
    }

    fetchArduinoData();
    setInterval(fetchArduinoData, 10000); // Default refresh rate of 10 seconds
});
