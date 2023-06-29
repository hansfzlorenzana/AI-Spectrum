google.charts.load('current', {
    'packages': ['corechart', 'controls']
  });
  google.charts.setOnLoadCallback(drawChart);
  
  function drawChart() {
    var queryOptions = {
        csvColumns: ['datetime', 'number', 'number', 'string', 'string'],
        csvHasHeader: true
    };
  
    var query = new google.visualization.Query('./app/database/political_compass_test_logs.csv', queryOptions);
    query.send(handleQueryResponse);
  
  }
  
  function handleQueryResponse(response) {
    if (response.isError()) {
        alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
        return;
    }
  
    var data = response.getDataTable();
  
    // Convert the data types of columns as needed
    data.setColumnLabel(0, 'Datetime');
    data.setColumnLabel(1, 'Economic Value');
    data.setColumnLabel(2, 'Social Value');
    data.setColumnLabel(3, 'Test');
    data.setColumnLabel(4, 'AI Name');
  
    // Convert column 0 (Datetime) to 'datetime' data type
    data.setColumnProperty(0, 'type', 'datetime');
  
    // Convert column 1 (Economic Value) and column 2 (Social Value) to 'number' data type
    data.setColumnProperty(1, 'type', 'number');
    data.setColumnProperty(2, 'type', 'number');
  
    var chart = new google.visualization.ChartWrapper({
        chartType: 'LineChart',
        containerId: 'chart_div',
        dataTable: data,
        options: {
            width: '100%', // 700
            height: 600, //600
            backgroundColor: '#FFFFFF',
            // curveType: 'function',
            colors: ['#FF8C00', '#000000'],
            legend: {
                position: 'top',
                alignment: 'end',
                textStyle: {
                    color: 'black',
                    bold: true
                }
            },
            tooltip: { 
                textStyle: { 
                    fontSize: 13 
                },
                content: {
                    
                }
            },
            title: 'Political Compass Test Coordinates Over Time',
            titleTextStyle: {
                fontSize: 20,
                bold: true
            },
            chartArea: {
                width: '80%',
                height: '75%'
            },
            hAxis: {
                gridLines: {
                    color: '#CCCCCC'
                },
                textStyle: {
                    color: '#666666',
                    fontSize: 11,
                    bold: true
                  }
            },
            vAxis: {
                title: 'Value',
                gridLines: {
                    color: '#CCCCCC'
                },
                textStyle: {
                    color: '#666666',
                    fontSize: 11,
                    bold: true
                },
                minValue: 0
            },
            responsive: true
        }
    });
  
    var control = new google.visualization.ControlWrapper({
        controlType: 'ChartRangeFilter',
        containerId: 'control_div',
        dataTable: data,
        options: {
            filterColumnIndex: 0,
            ui: {
                chartType: 'LineChart',
                chartOptions: {
                    width: '100%', //700
                    height: 120, // 100
                    backgroundColor: '#FFFFFF',
                    colors: ['darkOrange', 'black'],
                    lineWidth: 1,
                    chartArea: {
                        width: '80%',
                        top: 0,
                        bottom: 50,
                        left: 60,
                        right: 60
                    },
                    hAxis: {
                        textStyle: {
                            color: 'grey'
                        }
                    },
                    responsive: true
                },
            },
        },
    });
  
    var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));
    dashboard.bind(control, chart);
    dashboard.draw(data);

      // Set default chart filter to "ChatGPT"
    var defaultFilter = 'ChatGPT';

  
    function filterChart(filterValue) {
        var filterSelect = document.getElementById('filter-select');
  
        filterSelect.addEventListener('change', function() {
            var filterValue = filterSelect.value;
            filterChart(filterValue);
        });
  
        var chartTitle = filterValue === 'Reset' ? 'Political Compass Test Coordinates Over Time' : 'Political Compass Test Coordinates Over Time (' + filterValue + ')';
  
        if (filterValue === 'Reset' || data.getFilteredRows([{
                column: 4,
                value: filterValue
            }]).length > 0) {
            var view = new google.visualization.DataView(data);
            view.setColumns([0, 1, 2]);
            if (filterValue !== 'Reset') {
                view.setRows(data.getFilteredRows([{
                    column: 4,
                    value: filterValue
                }]));
            }
  
            chart.setOption('title', chartTitle);
            chart.setDataTable(view);
            chart.draw();
            control.setDataTable(view);
            control.draw();
        } else {
            // Reset the select element to the default option
            filterSelect.value = 'Reset';
  
            chart.setOption('title', 'Political Compass Test Coordinates Over Time');
            chart.setDataTable(data);
            chart.draw();
            control.setDataTable(data);
            control.draw();
        }
  
        if (filterValue === 'ChatGPT') {
            // Reset the select element to the default option
            filterSelect.value = 'ChatGPT';
  
            control.setState({}); // Reset the zoom state
            control.draw();
        }

    }
  
  
    function zoomLastDay() {
        var range = data.getColumnRange(0);
        control.setState({
            range: {
                start: new Date(range.max.getFullYear(), range.max.getMonth(), range.max.getDate() - 1),
                end: range.max
            }
        });
        control.draw();
    }
  
  
    function zoomLastWeek() {
        var range = data.getColumnRange(0);
        control.setState({
            range: {
                start: new Date(range.max.getFullYear(), range.max.getMonth(), range.max.getDate() - 7),
                end: range.max
            }
        });
        control.draw();
    }
  
    function zoomLastMonth() {
        var today = new Date();
        var lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
        control.setState({
            range: {
                start: lastMonth,
                end: today
            }
        });
        control.draw();
    }
  
    function zoomMax() {
        var range = data.getColumnRange(0);
        var startDate = range.min;
        var endDate = range.max;
  
        // Calculate the range for one year
        var oneYearAgo = new Date(endDate.getFullYear() - 1, endDate.getMonth(), endDate.getDate());
  
        // Adjust the start date if it's earlier than one year ago
        if (startDate < oneYearAgo) {
            startDate = oneYearAgo;
        }
  
        control.setState({
            range: {
                start: startDate,
                end: endDate
            }
        });
        control.draw();
    }
  
    var zoomMaxButton = document.getElementById('zoom-max');
    zoomMaxButton.addEventListener('click', zoomMax);
  
    var lastDayButton = document.getElementById('zoom-last-day');
    lastDayButton.addEventListener('click', zoomLastDay);
  
    var lastWeekButton = document.getElementById('zoom-last-week');
    lastWeekButton.addEventListener('click', zoomLastWeek);
  
    var lastMonthButton = document.getElementById('zoom-last-month');
    lastMonthButton.addEventListener('click', zoomLastMonth);
  
    var filterButtons = document.getElementsByClassName('filter-button');
    for (var i = 0; i < filterButtons.length; i++) {
        filterButtons[i].addEventListener('click', function() {
            var filterValue = this.textContent;
            filterChart(filterValue);
        });
        filterButtons[i].classList.add('ui-button');
    }
  
    var filterResetButton = document.getElementById('filter-reset');
    filterResetButton.addEventListener('click', function() {
        filterChart(defaultFilter);
    });
  
    filterChart(defaultFilter);
    
    // Make Chart Responsive to any screen
    function resizeHandler () {
        filterChart(defaultFilter);
    
    }
    if (window.addEventListener) {
        window.addEventListener('resize', resizeHandler, false);
    }
    else if (window.attachEvent) {
        window.attachEvent('onresize', resizeHandler);
    }

  }



