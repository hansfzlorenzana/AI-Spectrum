// Load the Charts and the corechart package.
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var queryOptions = {
        // Define the CSV data columns
        csvColumns: ['datetime', 'number','number','string','string'],
        // This should be false if your CSV file doesn't have a header 
        csvHasHeader: true
    }
        
    // Create the query giving the path and name of the CSV file
    var query = new google.visualization.Query('./database/coordinates_logs.csv', queryOptions);
    query.send(handleQueryResponse);
}

function handleQueryResponse(response) {
    if (response.isError()) {
        alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
        return;
    }

    var data = response.getDataTable();
    var chart = new google.visualization.ChartWrapper({
        chartType: 'LineChart',
        containerId: 'chart_div',
        dataTable: data,
        options:{
            width: 700, height: 600,
            backgroundColor: '#FFFFFF',
            lineWidth: 3,
            colors: ['darkOrange', 'black'],
            legend: 'right',
            title: 'Political Compass Test Coordinates Over Time',
            titleTextStyle : {color: 'grey', fontSize: 11},
            chartArea: {
                width: '73%',
                top: 40,
                bottom: 200,
                left: 40,
                // this should be the same as the ChartRangeFilter
            }
        }
    });
    var view = new google.visualization.DataView(data);
    var viewColumns = [0, 1, 2];
    view.setColumns(viewColumns);

    view.setRows(data.getFilteredRows([{column: 4, value: 'Bard'}]));
    var control = new google.visualization.ControlWrapper({
        controlType: 'ChartRangeFilter',
        containerId: 'control_div',
        options: {
        filterColumnIndex: 0,
        ui: {
            chartOptions: {
            height: 50,
            width: 700,
            colors: ['darkOrange', 'black'],
            backgroundColor: '#FFFFFF',
            // omit width, since we set this in CSS
            chartArea: {
                width: '73%',
                top: 0,
                left: 40,
                // this should be the same as the ChartRangeFilter
            }
            }
        }
        }
    });

    var dashboard = new google.visualization.Dashboard(document.querySelector('#dashboard_div'));
    dashboard.bind([control], [chart]);
    dashboard.draw(view);

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
        // zoom here sets the month back 1, which can have odd effects when the last month has more days than the previous month
        // eg: if the last day is March 31, then zooming last month will give a range of March 3 - March 31, as this sets the start date to February 31, which doesn't exist
        // you can tweak this to make it function differently if you want
        var range = data.getColumnRange(0);
        control.setState({
        range: {
            start: new Date(range.max.getFullYear(), range.max.getMonth() - 1, range.max.getDate()),
            end: range.max
        }
        });
        control.draw();
    }

    
    var runOnce = google.visualization.events.addListener(dashboard, 'ready', function() {
        google.visualization.events.removeListener(runOnce);
        if (document.addEventListener) {
        document.querySelector('#lastDay').addEventListener('click', zoomLastDay);
        document.querySelector('#lastWeek').addEventListener('click', zoomLastWeek);
        document.querySelector('#lastMonth').addEventListener('click', zoomLastMonth);
        } else if (document.attachEvent) {
        document.querySelector('#lastDay').attachEvent('onclick', zoomLastDay);
        document.querySelector('#lastWeek').attachEvent('onclick', zoomLastWeek);
        document.querySelector('#lastMonth').attachEvent('onclick', zoomLastMonth);
        } else {
        document.querySelector('#lastDay').onclick = zoomLastDay;
        document.querySelector('#lastWeek').onclick = zoomLastWeek;
        document.querySelector('#lastMonth').onclick = zoomLastMonth;
        }
    });
}

google.load('visualization', '1.1', {
    packages: ['controls'],
    callback: drawChart
});
    
//     chart.draw();
// }