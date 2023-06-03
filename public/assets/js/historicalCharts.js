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

		let charts = [waitChart,queueChart,validatorChart,stakedChart,aprChart];
		charts.forEach((chart) => {
			chart.options.plugins.legend.labels.color = legend_color;
			chart.options.scales.x.ticks.color = ticks_color;
			chart.options.scales.y.ticks.color = ticks_color;
			if (chart.options.scales.y1) {
				chart.options.scales.y1.ticks.color = ticks_color;
			}
			chart.options.scales.x.grid.color = grid_color;
			chart.options.scales.y.grid.color = grid_color;
			chart.update();
		});
	}
	document.getElementById("darkModeToggle").addEventListener("click", updateChartColor);

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
	var fill = false;

	var queueChart = new Chart(document.getElementById('queueChart'), {
		type: 'line',  
		data: {
			labels: historical_data.map(row => row.date),
	        datasets: [
				{
		            label: 'Entry',
		            data: historical_data.map(row => Math.round(row.entry_queue)),
					fill: fill,
					pointStyle: false
				},
				{
		            label: 'Exit',
		            data: historical_data.map(row => Math.round(row.exit_queue)),
					fill: fill,
					pointStyle: false
				}
	        ]
		},
		options: {
			scales: {
				x: scales_x,
				y: {
					// min: 0,
	                ticks: {
	                    callback: function(value) {
	                        return (value === 0) ? value : `${Math.round(value/100)/10}k`;
	                    }
	                }
	            }
			},
			interaction: {
				intersect: false,
			}
		}
	});

	var waitChart = new Chart(document.getElementById('waitChart'), {
		type: 'line',  
		data: {
			labels: historical_data.filter(row => row.entry_wait || row.exit_wait).map(row => row.date),
	        datasets: [
				{
		            label: 'Entry',
		            data: historical_data.filter(row => row.entry_wait).map(row => row.entry_wait),
					fill: fill,
					pointStyle: false
				},
				{
		            label: 'Exit',
		            data: historical_data.filter(row => row.exit_wait).map(row => row.exit_wait),
					fill: fill,
					pointStyle: false
				}
	        ]
		},
		options: {
			scales: {
				x: scales_x,
			},
			interaction: {
				intersect: false,
			}
		}
	});

	
	var validatorChart = new Chart(document.getElementById('validatorChart'), {
		type: 'line',  
		data: {
			labels: historical_data.map(row => row.date),
	        datasets: [
				{
		            label: 'Active validators',
		            data: historical_data.map(row => Math.round(row.validators)),
					fill: fill,
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

	var stakedChart = new Chart(document.getElementById('stakedChart'), {
		type: 'line',  
		data: {
			labels: historical_data.map(row => row.date),
	        datasets: [
				{
		            label: 'Total ETH Staked',
		            data: historical_data.map(row => Math.round(row.staked_amount)),
		            yAxisID: 'y',
					fill: fill,
					pointStyle: false
				},
				{
		            label: '% Supply Staked',
		            data: historical_data.map(row => row.staked_percent),
		            yAxisID: 'y1',
					fill: fill,
					pointStyle: false
				}
	        ]
		},
		options: {
			scales: {
				x: scales_x,
				y: {
					position: 'left',
	                ticks: {
	                    callback: function(value) {
	                        return `${value}`;
	                    }
	                }
	            },
	            y1: {
	            	position: 'right',
	            	grid: {
						drawOnChartArea: false, // only want the grid lines for one axis to show up
			        },
	                ticks: {
	                    callback: function(value) {
	                        return `${value}`;
	                    }
	                }
	            }
			},
			interaction: {
				intersect: false,
			}
		}
	});

	var aprChart = new Chart(document.getElementById('aprChart'), {
		type: 'line',  
		data: {
			labels: historical_data.filter(row => row.apr !== null).map(row => row.date),
	        datasets: [
				{
		            label: 'Staking APR (%)',
		            data: historical_data.filter(row => row.apr !== null).map(row => Math.round(row.apr)),
					fill: fill,
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
	                        return `${value}%`;
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
