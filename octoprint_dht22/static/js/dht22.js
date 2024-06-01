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
        } else {
            $("#navbar_temperature").text("--");
            $("#navbar_humidity").text("--");
        }
    }

    fetchArduinoData();
    setInterval(fetchArduinoData, 10000); // Default refresh rate of 10 seconds
});
