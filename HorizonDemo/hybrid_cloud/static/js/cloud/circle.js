function circle() {
    //alert(arguments[0])
    $(arguments[0]).highcharts({

        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            height:200
        },
        credits: {
          enabled:false
        },
        colors:[
                        '#379BFF',
                        '#CACACA'
                      ],
        title: {
            text: arguments[2]
        },
        tooltip: {
    	    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'resource',
            data: arguments[1]
        }]
    });
}

