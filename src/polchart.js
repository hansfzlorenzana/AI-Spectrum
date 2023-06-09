// Fetch the CSV file
fetch('./database/political_compass_test_logs.csv')
  .then(function(response) {
    return response.text();
  })
  .then(function(csvData) {
    // Parse the CSV data
    var parsedData = Papa.parse(csvData, { header: true });
    var data = parsedData.data;

    // Filter and retrieve the latest rows of each AI
    var latestData = getLatestRows(data, 'ai_name');

    Highcharts.chart('politicalTestChartContainer', {
      chart: {
        plotBackgroundImage: './images/chart-samples/political_compass.png',
        type: 'scatter',
        borderWidth: 1,
        borderColor: '#ccc',
        marginLeft: 100,
        marginRight: 200,
        marginBottom: 100,
        marginTop: 200,
        width: 700,
        height: 700,
        events: {
          render: function() {
            var chart = this,
                xAxis = chart.xAxis[0],
                yAxis = chart.yAxis[0],
                labelStyle = {
                  color: '#333',
                  fontWeight: 'bold',
                  fontSize: '12px'
                };

            // Add label on top of the chart
            chart.renderer.text('Authoritarian', chart.plotLeft + (chart.plotWidth / 2), chart.plotTop - 20)
              .attr({
                align: 'center'
              })
              .css(labelStyle)
              .css({
                fontSize: '20px' // Adjust the font size of the label
              })
              .add();

            // Add label on right side of the chart
            chart.renderer.text('Right', chart.plotLeft + chart.plotWidth + 50, chart.plotTop + (chart.plotHeight / 2))
              .attr({
                align: 'center',
                rotation: 0
              })
              .css(labelStyle)
              .css({
                fontSize: '20px' // Adjust the font size of the label
              })
              .add();

            // Add label on bottom of the chart
            chart.renderer.text('Libertarian', chart.plotLeft + (chart.plotWidth / 2), chart.plotTop + chart.plotHeight + 40)
              .attr({
                align: 'center'
              })
              .css(labelStyle)
              .css({
                fontSize: '20px' // Adjust the font size of the label
              })
              .add();

            // Add label on left side of the chart
            chart.renderer.text('Left', chart.plotLeft - 50, chart.plotTop + (chart.plotHeight / 2))
              .attr({
                align: 'center',
                rotation: 0,
              })
              .css(labelStyle)
              .css({
                fontSize: '20px' // Adjust the font size of the label
              })
              .add();
          }
        }
      },
      title: {
        text: 'Political Compass Test',
        margin: 50,
        y: 80,
        x: -50,
        style: {
          fontSize: '40px' // Adjust the font size of the title
        }
      },
      credits: {
        enabled: false
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: 10,
        y: 200,
        itemMarginBottom: 10,
        itemStyle: {
            color: '#000000',
            fontSize: '16px' // Adjust the font size of the legend items
        },
        itemHoverStyle: {
            color: 'darkorange'
        },
        itemMarginLeft: 500,
        maxHeight: 380,
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
      
      
      tooltip: {
        formatter: function() {
          return '<b><span style="font-size: 16px;">'+ this.series.name +'</b><br/>'+
              '<b>Economic:</b> '+ this.x + '<br/>'+ ' <b>Social:</b> '+ this.y;
        }
      },
      plotOptions: {
        series: {
          shadow: true
        },
        scatter: {
          marker: {
            symbol: 'circle',
            radius: 8,
            lineColor: 'white',
            lineWidth: 1
          }
        }
      },
      xAxis: {
        title: {
          text: '',
          align: 'high',
          rotation: 0,
          offset: 0,
          x: 30,
          y: -20,
          style: {
            fontWeight: 'bold'
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
        showLastLabel: false,
        showFirstLabel: false,
        lineColor: '#ccc',
        lineWidth: 0
      },
      yAxis: {
        title: {
          text: '',
          align: 'high',
          rotation: 0,
          offset: 0,
          x: 60,
          y: -10,
          style: {
            fontWeight: 'bold'
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
      },
      exporting: {
        chartOptions: {
            chart: {
                height: 650
            }
        }
    },
    series: latestData.map(function(row) {
      return {
        name: row.ai_name,
        data: [{
          x: parseFloat(row.econ_value),
          y: parseFloat(row.soc_value)
        }],
        marker: {
          symbol: 'url(' + getMarkerSymbol(row.ai_name) + ')',
          width: 32,
          height: 32
        },
        color: getRandomColor()
      };
    })
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
