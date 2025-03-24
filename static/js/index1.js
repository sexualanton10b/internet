function send_data(device, elementId) {
    $.ajax({
        type: 'GET',
        url: `/connect_${device}`,
        dataType: 'json',
        contentType: 'application/json',
        data: {
            "value": document.getElementById(elementId).value,
        },
        success: function (response) {
            document.getElementById("command").value = response["power"]
        }
    });
}
function sendAllData() {
    send_data('robot1', 'robot1_value');
    send_data('robot2', 'robot2_value');
    send_data('smartcam', 'smartcam_value');
    send_data('signallamp', 'signallamp_value');
    send_data('terminal', 'terminal_value');
}
