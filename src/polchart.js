// Fetch the CSV file
fetch('./app/database/political_compass_test_logs.csv')
	.then(function(response) {
		return response.text();
	})
	.then(function(csvData) {
		// Parse the CSV data
		var parsedData = Papa.parse(csvData, {
			header: true
		});
		var data = parsedData.data;

		// Remove null rows in the csv
		var aiDataWithoutNull = data.filter(row => Object.values(row).some(value => value !== ""));

		// Filter and retrieve the latest rows of each AI
		var latestData = getLatestRows(aiDataWithoutNull, 'ai_name');

		var chart = Highcharts.chart('politicalTestChart', {
			chart: {
				plotBackgroundImage: './images/chart-samples/political_compass.png',
				type: 'scatter',
			},
			title: {
				text: 'Political Compass Test',
				style: {
					fontSize: '25px' // Adjust the font size of the title
				}
			},
			subtitle: {
				text: 'https://www.politicalcompass.org/test/',
			},
			credits: {
				enabled: false
			},
			legend: {
				layout: 'vertical',
				align: 'right',
				verticalAlign: 'middle',
				itemStyle: {
					color: '#000000',
					fontSize: '17px' // Adjust the font size of the legend items
				},
				itemHoverStyle: {
					color: 'darkorange'
				},
				maxHeight: 300,
				navigation: {
					activeColor: '#3E576F',
					animation: true,
					arrowSize: 10,
					inactiveColor: '#CCC',
					style: {
						fontWeight: 'bold',
						color: '#333',
						fontSize: '13px'
					}
				},
				labelFormatter: function() {
					var disabledByDefault = [
						"ChatGPT",
						"ChatGPT-4",
						"Bard",
						"Bing",
						"Claude",
						"HugChat"
					];

					// Disable legend items by default
					if (!disabledByDefault.includes(this.name)) {
						return '<span style="color: #">' + this.name + '</span>';
					}

					// Enable legend items by click
					return '<span style="cursor: pointer">' + this.name + '</span>';
				},
				itemStyle: {
					color: '#000000' // Set default legend item color to black
				},
				itemEvents: {
					click: function() {
						// Toggle the visibility of the clicked legend item
						var series = this.chart.series.find(s => s.name === this.name);
						var isVisible = !series.visible;
						series.setVisible(isVisible);

						// Update the legend item style
						this.update({
							color: isVisible ? '#000000' : '#000000' // Set legend item color to black when enabled/disabled
						});
					}
				}
			},

			tooltip: {
				formatter: function() {
					return '<b><span style="font-size: 16px;">' + this.series.name + '</b><br/>' +
						'<b>Economic:</b> ' + this.x + '<br/>' + ' <b>Social:</b> ' + this.y;
				}
			},

			plotOptions: {
				series: {
					shadow: true
				},
				scatter: {
					marker: {
						symbol: 'circle',
						radius: 10,
						lineColor: 'white',
						lineWidth: 1
					}
				}
			},
			xAxis: [{
				title: {
					text: 'Libertarian',
					rotation: 0,
					style: {
						fontWeight: 'bold',
						color: '#333',
						fontSize: '20px'
					}
				},
				labels: {
					enabled: false
				},
				min: -10,
				max: 10,
				tickInterval: 1,
				minorTickInterval: 1,
				tickLength: 0,
				gridLineWidth: 2,
				minorGridLineWidth: 2,
				minorTickLength: 0,
				gridLineColor: '#bebdb2',
				minorGridLineColor: '#bebdb2',
				minorGridLineDashStyle: 'line',
				lineColor: '#ccc',
				lineWidth: 0,
				plotLines: [{
					color: 'black', // Set the color of the plot line
					width: 4, // Set the width of the plot line
					value: 0, // Set the position of the plot line at line number 10
					zIndex: 1 // Set the z-index to bring the plot line above other chart elements
				}]
			}, {
				opposite: true,
				title: {
					text: 'Authoritarian',
					rotation: 0,
					style: {
						fontWeight: 'bold',
						color: '#333',
						fontSize: '20px'
					}
				}
			}],
			yAxis: [{
				title: {
					text: 'Left',
					rotation: 0,
					x: -20,
					y: 0,

					style: {
						fontWeight: 'bold',
						color: '#333',
						fontSize: '20px'
					}
				},
				labels: {
					enabled: false
				},
				min: -10,
				max: 10,
				tickInterval: 1,
				minorTickInterval: 1,
				tickLength: 0,
				gridLineWidth: 2,
				minorGridLineWidth: 2,
				minorTickLength: 0,
				gridLineColor: '#bebdb2',
				minorGridLineColor: '#bebdb2',
				minorGridLineDashStyle: 'line',
				lineColor: '#ccc',
				lineWidth: 0,
				plotLines: [{
					color: 'black', // Set the color of the plot line
					width: 4, // Set the width of the plot line
					value: 0, // Set the position of the plot line at line number 10
					zIndex: 1 // Set the z-index to bring the plot line above other chart elements
				}]
			}, {
				opposite: true,
				title: {
					text: 'Right',
					rotation: 0,
					x: 20,
					y: 0,

					style: {
						fontWeight: 'bold',
						color: '#333',
						fontSize: '20px'
					}

				}
			}],
			//   exporting: {
			//     chartOptions: {
			//         chart: {
			//             height: 650
			//         }
			//     }
			// },
			series: latestData.map(function(row) {
				var visibleByDefault = [
					"ChatGPT",
					"ChatGPT-4",
					"Bard",
					"Bing",
					"Claude",
					"HugChat"
				];
				var isVisible = visibleByDefault.includes(row.ai_name);

				return {
					name: row.ai_name,
					data: [{
						x: parseFloat(row.econ_value),
						y: parseFloat(row.soc_value)
					}],
					marker: {
						symbol: 'url(' + getMarkerSymbol(row.ai_name) + ')',
						width: 28,
						height: 28
					},
					color: isVisible ? getRandomColor() : '#CCCCCC', // Set color to gray for disabled series
					visible: isVisible // Set visibility based on default setting
				};
			}),
			responsive: {
				rules: [{
					condition: {
						maxWidth: 500
					},
					// Make the labels less space demanding on mobile
					chartOptions: {
						legend: {
							align: 'center',
							verticalAlign: 'bottom',
							layout: 'horizontal',
							maxHeight: 380,
							itemStyle: {
								color: '#000000',
								fontSize: '12px' // Adjust the font size of the legend items
							},
							navigation: {
								activeColor: '#3E576F',
								animation: true,
								arrowSize: 12,
								inactiveColor: '#CCC',
								style: {
									fontWeight: 'bold',
									color: '#333',
									fontSize: '12px'
								}
							}
						},
						series: latestData.map(function(row) {
							var visibleByDefault = [
								"ChatGPT",
								"ChatGPT-4",
								"Bard",
								"Bing",
								"Claude",
								"HugChat"
							];
							var isVisible = visibleByDefault.includes(row.ai_name);

							return {
								name: row.ai_name,
								data: [{
									x: parseFloat(row.econ_value),
									y: parseFloat(row.soc_value)
								}],
								marker: {
									symbol: 'url(' + getMarkerSymbol(row.ai_name) + ')',
									width: 20,
									height: 20
								},
								color: isVisible ? getRandomColor() : '#CCCCCC', // Set color to gray for disabled series
								visible: isVisible // Set visibility based on default setting
							};
						}),
						xAxis: [{
							title: {
								text: 'Libertarian',
								rotation: 0,
								style: {
									fontWeight: 'bold',
									color: '#333',
									fontSize: '15px'
								}
							},
							labels: {
								enabled: false
							},
							min: -10,
							max: 10,
							tickInterval: 1,
							minorTickInterval: 1,
							tickLength: 0,
							gridLineWidth: 2,
							minorGridLineWidth: 2,
							minorTickLength: 0,
							gridLineColor: '#bebdb2',
							minorGridLineColor: '#bebdb2',
							minorGridLineDashStyle: 'line',
							lineColor: '#ccc',
							lineWidth: 0
						}, {
							opposite: true,
							title: {
								text: 'Authoritarian',
								rotation: 0,
								style: {
									fontWeight: 'bold',
									color: '#333',
									fontSize: '15px'
								}
							}
						}],
						yAxis: [{
							title: {
								text: 'Left',
								rotation: 0,
								x: -15,
								y: 0,

								style: {
									fontWeight: 'bold',
									color: '#333',
									fontSize: '15px'
								}
							},
							labels: {
								enabled: false
							},
							min: -10,
							max: 10,
							tickInterval: 1,
							minorTickInterval: 1,
							tickLength: 0,
							gridLineWidth: 2,
							minorGridLineWidth: 2,
							minorTickLength: 0,
							gridLineColor: '#bebdb2',
							minorGridLineColor: '#bebdb2',
							minorGridLineDashStyle: 'line',
							lineColor: '#ccc',
							lineWidth: 0
						}, {
							opposite: true,
							title: {
								text: 'Right',
								rotation: 0,
								x: 15,
								y: 0,

								style: {
									fontWeight: 'bold',
									color: '#333',
									fontSize: '15px'
								}

							}
						}],
					}
				}]
			}
		});

	});

// Function to generate random color
function getRandomColor() {
	var letters = '0123456789ABCDEF';
	var color = '#';
	for (var i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}

// Function to get the marker symbol based on AI name
function getMarkerSymbol(aiName) {
	// Generate the icon path based on the AI name
	var iconPath = './images/ai-icons/' + aiName + '.png';

	// Return the icon path
	return iconPath;
}


// Function to filter and retrieve the latest rows of each AI
function getLatestRows(data, columnName) {
	var uniqueAIs = [];
	var latestData = [];

	// Loop through the data in reverse order
	for (var i = data.length - 1; i >= 0; i--) {
		var row = data[i];

		// Check if the AI name is not already in the uniqueAIs array
		if (!uniqueAIs.includes(row[columnName])) {
			// Add the AI name to the uniqueAIs array
			uniqueAIs.push(row[columnName]);

			// Add the row to the latestData array
			latestData.push(row);
		}
	}

	// Reverse the latestData array to get the original order
	return latestData.reverse();
}