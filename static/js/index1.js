function send_data(device, valueId, powerId) {
    $.ajax({
        type: 'GET',
        url: `/connect_${device}`,
        dataType: 'json',
        contentType: 'application/json',
        data: {
            "value": document.getElementById(valueId).value,
        },
        success: function (response) {
            if (response.power) {
                document.getElementById(powerId).value = response.power;
            }
            if (response.value !== undefined) {
                document.getElementById(valueId).value = response.value;
            }
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
}

function sendAllData() {
    send_data('robot1', 'robot1_value', 'robot1_power');
    send_data('robot2', 'robot2_value', 'robot2_power');
    send_data('smartcam', 'smartcam_value', 'smartcam_power');
    send_data('signallamp', 'signallamp_value', 'signallamp_power');
    send_data('terminal', 'terminal_value', 'terminal_power');
}