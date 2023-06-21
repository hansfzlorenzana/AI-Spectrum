

function loadCSV() {
    Papa.parse("./app/database/8values_political_test_logs.csv", {
      download: true,
      header: true,
      complete: function(results) {
        createChart(results.data);
      }
    });
  }

  function createChart(data) {


    // Define the axis names
    var axisNames = ['Economic Axis:', 'Diplomatic Axis:', 'Civil Axis:', 'Societal Axis:'];

    // Get the unique AI names
    var aiNames = [...new Set(data.map(row => row.ai_name))];

    // Iterate through each AI and extract the latest data
    aiNames.forEach((aiName, index) => {
      var aiData = data.filter(row => row.ai_name === aiName);
      var aiDataWithoutNull = aiData.filter(row => Object.values(row).some(value => value !== ""));
      var latestData = aiDataWithoutNull[aiDataWithoutNull.length - 1]; // Get the latest data for the AI

      // Extract the axis values and calculate percentages
      var equality = Number(latestData.equality);
      var wealth = Number(latestData.wealth);
      var peace = Number(latestData.peace);
      var might = Number(latestData.might);
      var liberty = Number(latestData.liberty);
      var authority = Number(latestData.authority);
      var progress = Number(latestData.progress);
      var tradition = Number(latestData.tradition);

      var totalEqualityWealth = equality + wealth;
      var totalPeaceMight = peace + might;
      var totalLibertyAuthority = liberty + authority;
      var totalProgressTradition = progress + tradition;

      var equalityPercentage = (equality / totalEqualityWealth) * 100;
      var wealthPercentage = (wealth / totalEqualityWealth) * 100;
      var peacePercentage = (peace / totalPeaceMight) * 100;
      var mightPercentage = (might / totalPeaceMight) * 100;
      var libertyPercentage = (liberty / totalLibertyAuthority) * 100;
      var authorityPercentage = (authority / totalLibertyAuthority) * 100;
      var progressPercentage = (progress / totalProgressTradition) * 100;
      var traditionPercentage = (tradition / totalProgressTradition) * 100;

      var chartContainer = document.createElement('div');
      chartContainer.id = `chartContainer-${aiName}`;
      chartContainer.style.overflow = 'visible'; // Set overflow to 'visible'
      document.body.appendChild(chartContainer);


    // Get Label Results for each Political Axis
    econArray = ["Communist", "Socialist", "Social", "Centrist", "Market", "Capitalist", "Laissez-Faire"]
    diplArray = ["Cosmopolitan", "Internationalist", "Peaceful", "Balanced", "Patriotic", "Nationalist", "Chauvinist"]
    govtArray = ["Anarchist", "Libertarian", "Liberal", "Moderate", "Statist", "Authoritarian", "Totalitarian"]
    sctyArray = ["Revolutionary", "Very Progressive", "Progressive", "Neutral", "Traditional", "Very Traditional", "Reactionary"]

    function setLabel(val,ary) {
        if (val > 100) { return "" } else
        if (val > 90) { return ary[0] } else
        if (val > 75) { return ary[1] } else
        if (val > 60) { return ary[2] } else
        if (val >= 40) { return ary[3] } else
        if (val >= 25) { return ary[4] } else
        if (val >= 10) { return ary[5] } else
        if (val >= 0) { return ary[6] } else
            {return ""}
    }

    economicAxis = setLabel(equality, econArray)
    diplomaticAxis = setLabel(peace, diplArray)
    civilAxis = setLabel(liberty, govtArray)
    societalAxis = setLabel(progress, sctyArray)

    // Get Closest Match Results

    ideology = ""
    ideodist = Infinity
    for (var i = 0; i < ideologies.length; i++) {
        dist = 0
        dist += Math.pow(Math.abs(ideologies[i].stats.econ - equality), 2)
        dist += Math.pow(Math.abs(ideologies[i].stats.govt - liberty), 2)
        dist += Math.pow(Math.abs(ideologies[i].stats.dipl - peace), 1.73856063)
        dist += Math.pow(Math.abs(ideologies[i].stats.scty - progress), 1.73856063)
        if (dist < ideodist) {
            ideology = ideologies[i].name
            ideodist = dist
        }
    }
    ideology = ideology


        Highcharts.chart(chartContainer.id, {
          chart: {
            type: "bar",
            marginLeft: 100,
            marginBottom: 40,
            marginRight: 100, // Increase the left margin to create more space
            spacingLeft: 0, // Reduce the space on the left side of the chart
            spacingRight: 0, // Reduce the space on the right side of the chart
            events: {
              load: function() {
                // Get the chart reference
                var chart = this;
                var axis1 = 110;
                var axis2 = 75

                // Add the annotations dynamically
                chart.renderer.text("Economic Axis: ", axis1, axis2)
                  .css({
                    fontSize: '14px',
                    fontWeight: 'bold'
                  })
                  .add();

                  chart.renderer.text(economicAxis, axis1 + 110, axis2)
                  .css({
                    fontSize: '14px'
                  })
                  .add();

                chart.renderer.text("Diplomatic Axis: ", axis1, axis2*2.0)
                  .css({
                    fontSize: '14px',
                    fontWeight: 'bold'
                  })
                  .add();

                  chart.renderer.text(diplomaticAxis, axis1 + 115, axis2*2.0)
                  .css({
                    fontSize: '14px'
                  })
                  .add();

                chart.renderer.text("Civil Axis: ", axis1, axis2*3.0)
                  .css({
                    fontSize: '14px',
                    fontWeight: 'bold'
                  })
                  .add();

                  chart.renderer.text(civilAxis, axis1 + 70, axis2*3.0)
                  .css({
                    fontSize: '14px'
                  })
                  .add();

                chart.renderer.text("Societal Axis: ", axis1, axis2*4.0)
                  .css({
                    fontSize: '14px',
                    fontWeight: 'bold'
                  })
                  .add();

                  chart.renderer.text(societalAxis, axis1 + 95, axis2*4.0)
                  .css({
                    fontSize: '14px'
                  })
                  .add();

                chart.renderer.text("Closest Match: ", axis1, axis2*5.0)
                  .css({
                    fontSize: '15px',
                    fontWeight: 'bold',
                    color: 'red'
                  })
                  .add();

                chart.renderer.text(ideology, axis1 + 110, axis2*5.0)
                .css({
                  fontSize: '13px'
                })
                .add();
              }
            }
          },
          title: {
            text: `${aiName}: ${ideology}`
          },
          subtitle: {
            text: '8Values Poltiical Test'
          },
          xAxis: [{
            lineWidth: 0,
            tickWidth: 0,
            categories: ['EQUALITY', 'NATION', 'LIBERTY', 'TRADITION'],
            labels: {
              enabled: true,
              align: 'left',
              x: -70, // Adjust the x position of the labels
              style: {
                fontSize: '14px',
              },
              useHTML: true,
              formatter: function() {
                var imagePath = "./images/value_images/";
                var imageName = "";

                if (this.value === "EQUALITY") {
                  imageName = "equality.svg";
                } else if (this.value === "NATION") {
                  imageName = "nation.svg";
                } else if (this.value === "LIBERTY") {
                  imageName = "liberty.svg";
                } else if (this.value === "TRADITION") {
                  imageName = "tradition.svg";
                }

                return `<img src="${imagePath}${imageName}" style="height: 70px; width: 70px;">`;
              }
            },
            gridLineWidth: 0,
          }, {
            lineWidth: 0,
            tickWidth: 0,
            opposite: true,
            linkedTo: 0,
            categories: ['MARKETS', 'GLOBE', 'AUTHORITY', 'PROGRESS'],
            labels: {
              enabled: true,
              align: 'right',
              x: 70,
              style: {
                fontSize: '14px',
              },
              useHTML: true,
              formatter: function() {
                var imagePath = "./images/value_images/";
                var imageName = "";

                if (this.value === "MARKETS") {
                  imageName = "markets.svg";
                } else if (this.value === "GLOBE") {
                  imageName = "globe.svg";
                } else if (this.value === "AUTHORITY") {
                  imageName = "authority.svg";
                } else if (this.value === "PROGRESS") {
                  imageName = "progress.svg";
                }

                return `<img src="${imagePath}${imageName}" style="height: 70px; width: 70px;">`;
              }
            },
          }],
          
          yAxis: {
            title: {
              text: null
            },
            labels: {
              enabled: false,
              formatter: function() {
                return this.value + '%'; // Add '%' symbol to the labels on the y-axis
              }
            },
            gridLineWidth: 0,
            max: 100
          },
          plotOptions: {
            series: {
              stacking: 'normal',
              dataLabels: {
                enabled: true,
                formatter: function() {
                  if (this.y !== 0) {
                    return this.y.toFixed(1) + '%'; // Show data label only for non-zero values
                  }
                  return null; // Hide data label for zero values
                },
                style: {
                  fontSize: '25px',
                  color: 'black'
                }
              },
              pointPadding: 0, // Remove space between bars
              groupPadding: 0.25, // Add space between groups of bars

            }
          },
          tooltip: {
            formatter: function() {
              if (this.y !== 0) {
                return `<b>${aiName}</b><br>${this.series.name}: ${this.y.toFixed(1)}%`; // Show tooltip only for non-zero values
              }
              return null; // Hide tooltip for zero values
            }
          },
          series: [{
            name: 'Wealth',
            data: [{
              y: wealthPercentage,
              color: '#00897b',
              borderColor: 'black',
              borderWidth: 4 // Add border to the left side of the bar
            }, {
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }] // Swap the data values for Economic Axis
          }, {
            name: 'Equality',
            data: [{
              y: equalityPercentage,
              color: '#f44336',
              borderColor: 'black',
              borderWidth: 4 // Add border to the right side of the bar
            }, {
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }] // Swap the data values for Economic Axis
          }, {
            name: 'Peace',
            data: [{
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: peacePercentage,
              color: '#03a9f4',
              borderColor: 'black',
              borderWidth: 4 // Add border to the left side of the bar
            }] // Add 0 for the first category (Economic Axis)
          }, {
            name: 'Might',
            data: [{
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: mightPercentage,
              color: '#ff9800',
              borderColor: 'black',
              borderWidth: 4 // Add border to the right side of the bar
            }] // Add 0 for the first category (Economic Axis)
          }, {
            name: 'Authority',
            data: [{
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: authorityPercentage,
              color: '#3f51b5',
              borderColor: 'black',
              borderWidth: 4 // Add border to the left side of the bar
            }] // Add 0 for the first two categories (Economic Axis, Diplomatic Axis)
          }, {
            name: 'Liberty',
            data: [{
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: libertyPercentage,
              color: '#ffeb3b',
              borderColor: 'black',
              borderWidth: 4 // Add border to the right side of the bar
            }] // Add 0 for the first two categories (Economic Axis, Diplomatic Axis)
          }, {
            name: 'Progress',
            data: [{
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: progressPercentage,
              color: '#9c27b0',
              borderColor: 'black',
              borderWidth: 4 // Add border to the left side of the bar
            }] // Add 0 for the first two categories (Economic Axis, Diplomatic Axis)
          }, {
            name: 'Tradition',
            data: [{
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: 0,
              color: 'transparent',
              borderWidth: 0,
              borderColor: 'transparent'
            }, {
              y: traditionPercentage,
              color: '#8bc34a',
              borderColor: 'black',
              borderWidth: 4 // Add border to the right side of the bar
            }] // Add 0 for the first two categories (Economic Axis, Diplomatic Axis)
          }],
          legend: {
            enabled: false // Disable the legend
          },
          credits: {
            enabled: false
          },
          exporting: {
            enabled: true
          }
          
        });
      });
    }

    loadCSV();

    var ideologies = [
        {
            "name": "Anarcho-Communism",
            "stats": {
                "econ": 100,
                "dipl": 50,
                "govt": 100,
                "scty": 90
            }
        },
        {
            "name": "Libertarian Communism",
            "stats": {
                "econ": 100,
                "dipl": 70,
                "govt": 80,
                "scty": 80
            }
        },
        {
            "name": "Trotskyism",
            "stats": {
                "econ": 100,
                "dipl": 100,
                "govt": 60,
                "scty": 80
            }
        },
        {
            "name": "Marxism",
            "stats": {
                "econ": 100,
                "dipl": 70,
                "govt": 40,
                "scty": 80
            }
        },
        {
            "name": "De Leonism",
            "stats": {
                "econ": 100,
                "dipl": 30,
                "govt": 30,
                "scty": 80
            }
        },
        {
            "name": "Leninism",
            "stats": {
                "econ": 100,
                "dipl": 40,
                "govt": 20,
                "scty": 70
            }
        },
        {
            "name": "Stalinism/Maoism",
            "stats": {
                "econ": 100,
                "dipl": 20,
                "govt": 0,
                "scty": 60
            }
        },
        {
            "name": "Religious Communism",
            "stats": {
                "econ": 100,
                "dipl": 50,
                "govt": 30,
                "scty": 30
            }
        },
        {
            "name": "State Socialism",
            "stats": {
                "econ": 80,
                "dipl": 30,
                "govt": 30,
                "scty": 70
            }
        },
        {
            "name": "Theocratic Socialism",
            "stats": {
                "econ": 80,
                "dipl": 50,
                "govt": 30,
                "scty": 20
            }
        },
        {
            "name": "Religious Socialism",
            "stats": {
                "econ": 80,
                "dipl": 50,
                "govt": 70,
                "scty": 20
            }
        },
        {
            "name": "Democratic Socialism",
            "stats": {
                "econ": 80,
                "dipl": 50,
                "govt": 50,
                "scty": 80
            }
        },
        {
            "name": "Revolutionary Socialism",
            "stats": {
                "econ": 80,
                "dipl": 20,
                "govt": 50,
                "scty": 70
            }
        },
        {
            "name": "Libertarian Socialism",
            "stats": {
                "econ": 80,
                "dipl": 80,
                "govt": 80,
                "scty": 80
            }
        },
        {
            "name": "Anarcho-Syndicalism",
            "stats": {
                "econ": 80,
                "dipl": 50,
                "govt": 100,
                "scty": 80
            }
        },
        {
            "name": "Left-Wing Populism",
            "stats": {
                "econ": 60,
                "dipl": 40,
                "govt": 30,
                "scty": 70
            }
        },
        {
            "name": "Theocratic Distributism",
            "stats": {
                "econ": 60,
                "dipl": 40,
                "govt": 30,
                "scty": 20
            }
        },
        {
            "name": "Distributism",
            "stats": {
                "econ": 60,
                "dipl": 50,
                "govt": 50,
                "scty": 20
            }
        },
        {
            "name": "Social Liberalism",
            "stats": {
                "econ": 60,
                "dipl": 60,
                "govt": 60,
                "scty": 80
            }
        },
        {
            "name": "Christian Democracy",
            "stats": {
                "econ": 60,
                "dipl": 60,
                "govt": 50,
                "scty": 30
            }
        },
        {
            "name": "Social Democracy",
            "stats": {
                "econ": 60,
                "dipl": 70,
                "govt": 60,
                "scty": 80
            }
        },
        {
            "name": "Progressivism",
            "stats": {
                "econ": 60,
                "dipl": 80,
                "govt": 60,
                "scty": 100
            }
        },
        {
            "name": "Anarcho-Mutualism",
            "stats": {
                "econ": 60,
                "dipl": 50,
                "govt": 100,
                "scty": 70
            }
        },
        {
            "name": "National Totalitarianism",
            "stats": {
                "econ": 50,
                "dipl": 20,
                "govt": 0,
                "scty": 50
            }
        },
        {
            "name": "Global Totalitarianism",
            "stats": {
                "econ": 50,
                "dipl": 80,
                "govt": 0,
                "scty": 50
            }
        },
        {
            "name": "Technocracy",
            "stats": {
                "econ": 60,
                "dipl": 60,
                "govt": 20,
                "scty": 70
            }
        },
        {
            "name": "Centrist",
            "stats": {
                "econ": 50,
                "dipl": 50,
                "govt": 50,
                "scty": 50
            }
        },
        {
            "name": "Liberalism",
            "stats": {
                "econ": 50,
                "dipl": 60,
                "govt": 60,
                "scty": 60
            }
        },
        {
            "name": "Religious Anarchism",
            "stats": {
                "econ": 50,
                "dipl": 50,
                "govt": 100,
                "scty": 20
            }
        },
        {
            "name": "Right-Wing Populism",
            "stats": {
                "econ": 40,
                "dipl": 30,
                "govt": 30,
                "scty": 30
            }
        },
        {
            "name": "Moderate Conservatism",
            "stats": {
                "econ": 40,
                "dipl": 40,
                "govt": 50,
                "scty": 30
            }
        },
        {
            "name": "Reactionary",
            "stats": {
                "econ": 40,
                "dipl": 40,
                "govt": 40,
                "scty": 10
            }
        },
        {
            "name": "Social Libertarianism",
            "stats": {
                "econ": 60,
                "dipl": 70,
                "govt": 80,
                "scty": 70
            }
        },
        {
            "name": "Libertarianism",
            "stats": {
                "econ": 40,
                "dipl": 60,
                "govt": 80,
                "scty": 60
            }
        },
        {
            "name": "Anarcho-Egoism",
            "stats": {
                "econ": 40,
                "dipl": 50,
                "govt": 100,
                "scty": 50
            }
        },
        {
            "name": "Nazism",
            "stats": {
                "econ": 40,
                "dipl": 0,
                "govt": 0,
                "scty": 5
            }
        },
        {
            "name": "Autocracy",
            "stats": {
                "econ": 50,
                "dipl": 20,
                "govt": 20,
                "scty": 50
            }
        },
        {
            "name": "Fascism",
            "stats": {
                "econ": 40,
                "dipl": 20,
                "govt": 20,
                "scty": 20
            }
        },
        {
            "name": "Capitalist Fascism",
            "stats": {
                "econ": 20,
                "dipl": 20,
                "govt": 20,
                "scty": 20
            }
        },
        {
            "name": "Conservatism",
            "stats": {
                "econ": 30,
                "dipl": 40,
                "govt": 40,
                "scty": 20
            }
        },
        {
            "name": "Neo-Liberalism",
            "stats": {
                "econ": 30,
                "dipl": 30,
                "govt": 50,
                "scty": 60
            }
        },
        {
            "name": "Classical Liberalism",
            "stats": {
                "econ": 30,
                "dipl": 60,
                "govt": 60,
                "scty": 80
            }
        },
        {
            "name": "Authoritarian Capitalism",
            "stats": {
                "econ": 20,
                "dipl": 30,
                "govt": 20,
                "scty": 40
            }
        },
        {
            "name": "State Capitalism",
            "stats": {
                "econ": 20,
                "dipl": 50,
                "govt": 30,
                "scty": 50
            }
        },
        {
            "name": "Neo-Conservatism",
            "stats": {
                "econ": 20,
                "dipl": 20,
                "govt": 40,
                "scty": 20
            }
        },
        {
            "name": "Fundamentalism",
            "stats": {
                "econ": 20,
                "dipl": 30,
                "govt": 30,
                "scty": 5
            }
        },
        {
            "name": "Libertarian Capitalism",
            "stats": {
                "econ": 20,
                "dipl": 50,
                "govt": 80,
                "scty": 60
            }
        },
        {
            "name": "Market Anarchism",
            "stats": {
                "econ": 20,
                "dipl": 50,
                "govt": 100,
                "scty": 50
            }
        },
        {
            "name": "Objectivism",
            "stats": {
                "econ": 10,
                "dipl": 50,
                "govt": 90,
                "scty": 40
            }
        },
        {
            "name": "Totalitarian Capitalism",
            "stats": {
                "econ": 0,
                "dipl": 30,
                "govt": 0,
                "scty": 50
            }
        },
        {
            "name": "Ultra-Capitalism",
            "stats": {
                "econ": 0,
                "dipl": 40,
                "govt": 50,
                "scty": 50
            }
        },
        {
            "name": "Anarcho-Capitalism",
            "stats": {
                "econ": 0,
                "dipl": 50,
                "govt": 100,
                "scty": 50
            }
        }
    ];
    