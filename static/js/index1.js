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

function create_chart(robot, chartID) {
    // 1. Получаем элемент canvas
    const ctxElement = document.querySelector(chartID);
    if (!ctxElement) {
        console.error(`Element ${chartID} not found`);
        return;
    }

    // 2. Уничтожаем предыдущий график
    if (ctxElement.chart) {
        ctxElement.chart.destroy();
    }

    // 3. Показываем индикатор загрузки (с проверкой наличия container)
    const container = ctxElement.closest('.chart-container');
    if (container) container.classList.add('loading');

    $.ajax({
        type: 'GET',
        url: `/get_chart_${robot}?_=${new Date().getTime()}`, // Добавляем timestamp против кэширования
        dataType: 'json',
        success: function(response) {
            // 4. Скрываем индикатор загрузки
            if (container) container.classList.remove('loading');

            // 5. Проверяем полученные данные
            if (!response || !response.time_data || !response.robot_data) {
                console.error('Invalid data format received', response);
                return;
            }

            // 6. Определяем заголовок графика
            const chartLabel = robot === 'robot1' ? 'Значения Робота 1' : 'Значения Робота 2';

            // 7. Создаем график (исправленная версия без дублирования)
            ctxElement.chart = new Chart(ctxElement.getContext('2d'), {
                type: 'line',
                data: {
                    labels: response.time_data,
                    datasets: [{
                        label: chartLabel,
                        data: response.robot_data,
                        cubicInterpolationMode: 'monotone',
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        borderWidth: 3,
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#3498db',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        tension: 0.2,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                font: {
                                    size: 14,
                                    family: "'Arial', sans-serif"
                                },
                                padding: 20,
                                usePointStyle: true,
                                pointStyle: 'circle'
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: {
                                size: 16,
                                weight: 'bold'
                            },
                            bodyFont: {
                                size: 14
                            },
                            footerFont: {
                                size: 12
                            },
                            padding: 12,
                            cornerRadius: 8,
                            displayColors: true,
                            borderColor: 'rgba(255, 255, 255, 0.1)',
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: true,
                                color: 'rgba(0, 0, 0, 0.05)',
                                drawBorder: false
                            },
                            ticks: {
                                font: {
                                    size: 12
                                },
                                color: '#7f8c8d'
                            }
                        },
                        y: {
                            grid: {
                                display: true,
                                color: 'rgba(0, 0, 0, 0.05)',
                                drawBorder: false
                            },
                            ticks: {
                                font: {
                                    size: 12
                                },
                                color: '#7f8c8d'
                            },
                            beginAtZero: false
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    },
                    animation: {
                        duration: 1000,
                        easing: 'easeOutQuart'
                    }
                }
            });
        },
        error: function(xhr, status, error) {
            if (container) container.classList.remove('loading');
            console.error(`Error loading chart data for ${robot}:`, error);
        }
    });
}
// Функция для скачивания графика
function downloadChart(chartID) {
    const canvas = document.querySelector(chartID);
    const link = document.createElement('a');
    link.download = 'graph-' + new Date().toISOString().slice(0, 10) + '.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
}
function refreshCharts() {
    create_chart('robot1', '.chart1');
    create_chart('robot2', '.chart2');
}
function sendAllData() {
    send_data('robot1', 'robot1_value', 'robot1_power');
    send_data('robot2', 'robot2_value', 'robot2_power');
    send_data('smartcam', 'smartcam_value', 'smartcam_power');
    send_data('signallamp', 'signallamp_value', 'signallamp_power');
    send_data('terminal', 'terminal_value', 'terminal_power');
    refreshCharts()
}

// Обновление статистики и графиков каждые 5 секунд
setInterval(function() {
    updateStats('robot1', 'robot1_avg', 'robot1_max');
    updateStats('robot2', 'robot2_avg', 'robot2_max');
}, 5000);

// Инициализация статистики при загрузке страницы
$(document).ready(function() {
    updateStats('robot1', 'robot1_avg', 'robot1_max');
    updateStats('robot2', 'robot2_avg', 'robot2_max');
});