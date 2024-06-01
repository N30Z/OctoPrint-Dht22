$(function() {
    function fetchArduinoData() {
        $.ajax({
            url: API_BASEURL + "plugin/dht22",
            type: "POST",
            dataType: "json",
            data: JSON.stringify({
                command: "fetch_data",
            }),
            contentType: "application/json; charset=UTF-8",
            success: function(response) {
                updateNavbarValues(response);
                $("#dht22_log").html(response);
            },
            error: function(xhr, status, error) {
                addLogMessage("Failed to fetch data from Arduino.");
                console.error("Failed to fetch data from Arduino:", error);
            }
        });
    }

    function updateNavbarValues(data) {
        var tempMatch = data.match(/Temperatur: ([\d.]+) °C/);
        var humidityMatch = data.match(/Luftfeuchtigkeit: ([\d.]+) %/);

        if (tempMatch && humidityMatch) {
            var temperature = parseFloat(tempMatch[1]);
            var humidity = parseFloat(humidityMatch[1]);

            $("#navbar_temperature").text(temperature.toFixed(2));
            $("#navbar_humidity").text(humidity.toFixed(2));
            addLogMessage("Data fetched successfully from API.");
            addLogMessage("Temperature: " + temperature + "°C, Humidity: " + humidity + "%");
        } else {
            $("#navbar_temperature").text("--");
            $("#navbar_humidity").text("--");
            addLogMessage("Failed to parse data from API.");
        }
    }

    function addLogMessage(message) {
    var iframe = document.getElementById("dht22_tab").querySelector("iframe");
    if (!iframe) {
        console.error("Iframe not found");
        return;
    }

    iframe.onload = function() {
        var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        if (!iframeDoc) {
            console.error("Iframe document not found");
            return;
        }

        var logElement = iframeDoc.getElementById("dht22_log2");
        if (!logElement) {
            console.error("Log element not found in iframe");
            return;
        }

        var currentTime = new Date().toLocaleTimeString();
        logElement.innerHTML += "<div>[" + currentTime + "] " + message + "</div>";
        logElement.scrollTop = logElement.scrollHeight;
    };
}


    fetchArduinoData();
    setInterval(fetchArduinoData, 10000); // Default refresh rate of 10 seconds
});
