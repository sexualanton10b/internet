function get_data(device, elementId) {
    $.ajax({
        type: 'GET',
        url: `/connect_${device}`,
        dataType: 'json',
        success: function (response) {
            document.getElementById(elementId).value = response.value;
        },
        error: function (xhr, status, error) {
            console.error(`Ошибка при запросе данных от ${device}:`, error);
        }
    });
}

// Обновляем данные каждую секунду
setInterval(function() {
    get_data('robot1', 'robot1_value');
    get_data('robot2', 'robot2_value');
    get_data('smartcam', 'smartcam_value');
    get_data('signallamp', 'signallamp_value');
    get_data('terminal', 'terminal_value');
}, 1000);