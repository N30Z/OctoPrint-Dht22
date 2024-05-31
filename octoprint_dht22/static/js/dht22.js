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
                addLogMessage("Failed to parse data from Arduino.");
            }
        }).fail(function() {
            addLogMessage("Failed to fetch data from Arduino.");
        });
    }

    function addLogMessage(message) {
        var logElement = $("#dht22_log");
        var currentTime = new Date().toLocaleTimeString();
        logElement.append("<div>[" + currentTime + "] " + message + "</div>");
        logElement.scrollTop(logElement.prop("scrollHeight"));
    }

    fetchArduinoData();
    setInterval(fetchArduinoData, 10000); // Default refresh rate of 10 seconds
});

//    OCTOPRINT_VIEWMODELS.push({
//        construct: Dht22ViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
//        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_dht22, #tab_plugin_dht22, ...
//        elements: [ /* ... */ ]
//    });
//});
