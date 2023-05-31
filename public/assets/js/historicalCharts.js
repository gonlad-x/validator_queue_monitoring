(async function() {
	// update chart colors according to user's theme
	function updateChartColor() {
		let theme = document.querySelector("html").getAttribute('data-bs-theme');
		let legend_color;
		let ticks_color;
		let grid_color;

		if (theme == "light") {
			legend_color = '#212529';
			ticks_color = '#212529';
			grid_color = 'rgba(33, 37, 41, 0.1)';
		} else if (theme == "dark") {
			legend_color = '#adb5bd';
			ticks_color = '#adb5bd';
			grid_color = 'rgba(173, 181, 189, 0.2)';
		}

		waitChart.options.plugins.legend.labels.color = legend_color;
		waitChart.options.scales.x.ticks.color = ticks_color;
		waitChart.options.scales.y.ticks.color = ticks_color;
		waitChart.options.scales.x.grid.color = grid_color;
		waitChart.options.scales.y.grid.color = grid_color;

		queueChart.options.plugins.legend.labels.color = legend_color;
		queueChart.options.scales.x.ticks.color = ticks_color;
		queueChart.options.scales.y.ticks.color = ticks_color;
		queueChart.options.scales.x.grid.color = grid_color;
		queueChart.options.scales.y.grid.color = grid_color;

		validatorChart.options.plugins.legend.labels.color = legend_color;
		validatorChart.options.scales.x.ticks.color = ticks_color;
		validatorChart.options.scales.y.ticks.color = ticks_color;
		validatorChart.options.scales.x.grid.color = grid_color;
		validatorChart.options.scales.y.grid.color = grid_color;

		waitChart.update();
		queueChart.update();
		validatorChart.update();
	}
	document.getElementById("darkModeToggle").addEventListener("click", updateChartColor);

	var labels_x = historical_data.map(row => row.date);
	var scales_x = {
		    type: 'time',
		    time: {
				unit: 'day',
				displayFormats: {
					'day': 'MMM DD',
					'month': "MMM 'YY",
					'year': 'MMM YYYY'
				},
				tooltipFormat: 'MMM DD, YYYY'
			}
		};

	var waitChart = new Chart(document.getElementById('waitChart'), {
		type: 'line',  
		data: {
			labels: labels_x,
	        datasets: [
				{
		            label: 'Entry',
		            data: historical_data.map(row => row.entry_wait),
					fill: true,
					pointStyle: false
				},
				{
		            label: 'Exit',
		            data: historical_data.map(row => row.exit_wait),
					fill: true,
					pointStyle: false
				}
	        ]
		},
		options: {
			scales: {
				x: scales_x
			},
			interaction: {
				intersect: false,
			}
		}
	});

	var queueChart = new Chart(document.getElementById('queueChart'), {
		type: 'line',  
		data: {
			labels: labels_x,
	        datasets: [
				{
		            label: 'Entry',
		            data: historical_data.map(row => Math.round(row.entry_queue)),
					fill: true,
					pointStyle: false
				},
				{
		            label: 'Exit',
		            data: historical_data.map(row => Math.round(row.exit_queue)),
					fill: true,
					pointStyle: false
				}
	        ]
		},
		options: {
			scales: {
				x: scales_x,
				y: {
	                ticks: {
	                    callback: function(value) {
	                        return `${Math.round(value/100)/10}k`;
	                    }
	                }
	            }
			},
			interaction: {
				intersect: false,
			}
		}
	});

	var validatorChart = new Chart(document.getElementById('validatorChart'), {
		type: 'line',  
		data: {
			labels: labels_x,
	        datasets: [
				{
		            label: 'Total validators',
		            data: historical_data.map(row => Math.round(row.validators)),
					fill: true,
					pointStyle: false
				}
	        ]
		},
		options: {
			scales: {
				x: scales_x,
				y: {
	                ticks: {
	                    callback: function(value) {
	                        return `${Math.round(value/100)/10}k`;
	                    }
	                }
	            }
			},
			interaction: {
				intersect: false,
			}
		}
	});

	updateChartColor();

})();
