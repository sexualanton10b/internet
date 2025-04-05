function send_data(device, valueId, powerId) {
    var data = {};
    // Для сигнальной лампы не передаем значение
    if (device !== 'signallamp') {
        data.value = document.getElementById(valueId).value;
    }

    $.ajax({
        type: 'GET',
        url: `/connect_${device}`,
        dataType: 'json',
        contentType: 'application/json',
        data: data,  // данные для других устройств
        success: function (response) {
            if (response.power) {
                document.getElementById(powerId).value = response.power;
            }
            if (response.value !== undefined) {
                document.getElementById(valueId).value = response.value;
            }
            if (response.alert_message) {
                alert(response.alert_message);  // Показать сообщение об аварийной ситуации
            }
            if (device === 'signallamp') {
                // Меняем цвет поля сигнальной лампы
                var signallampField = document.getElementById('signallamp_power');
                if (response.power === 'On') {
                    signallampField.style.backgroundColor = 'red';  // Красный цвет для аварийной ситуации
                } else {
                    signallampField.style.backgroundColor = '';  // Сбросить цвет
                }
            }
            if (response.error) {
                alert(response.error);  // Показать сообщение об ошибке
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
    send_data('signallamp', 'signallamp_value', 'signallamp_power');  // Для сигнальной лампы запрос без value
    send_data('terminal', 'terminal_value', 'terminal_power');
}
