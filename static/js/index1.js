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
        data: data,
        success: function (response) {
            // Обновление состояния устройства
            if (response.power) {
                document.getElementById(powerId).value = response.power;
            }
            if (response.value !== undefined) {
                document.getElementById(valueId).value = response.value;
            }

            // Обработка аварийных сообщений
            if (response.alert_message) {
                alert(response.alert_message);
            }

            // Специальная обработка для сигнальной лампы
            if (device === 'signallamp') {
                var signallampField = document.getElementById('signallamp_power');
                if (response.power === 'On') {
                    signallampField.style.backgroundColor = 'red';
                } else {
                    signallampField.style.backgroundColor = '';
                }
            }

            // Обработка ошибок
            if (response.error) {
                alert(response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
}

function updateStats(robot, avgId, maxId) {
    $.ajax({
        type: 'GET',
        url: `/stats_${robot}`,
        dataType: 'json',
        success: function (response) {
            document.getElementById(avgId).value = response.average.toFixed(2);
            document.getElementById(maxId).value = response.max;
        },
        error: function (xhr, status, error) {
            console.error(`Ошибка при запросе статистики для ${robot}:`, error);
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

// Обновление статистики каждые 5 секунд
setInterval(function() {
    updateStats('robot1', 'robot1_avg', 'robot1_max');
    updateStats('robot2', 'robot2_avg', 'robot2_max');
}, 5000);

// Инициализация статистики при загрузке страницы
$(document).ready(function() {
    updateStats('robot1', 'robot1_avg', 'robot1_max');
    updateStats('robot2', 'robot2_avg', 'robot2_max');
});