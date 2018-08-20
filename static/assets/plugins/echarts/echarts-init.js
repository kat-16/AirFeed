
// ==============================================================
// Pie chart option
// ==============================================================
var pieChart = echarts.init(document.getElementById('chart'));

// specify chart configuration item and data
option = {

    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        x : 'center',
        y : 'bottom',
        data:['rose6','rose7','rose8']
    },
    toolbox: {
        show : true,
        feature : {

            dataView : {show: true, readOnly: false},
            magicType : {
                show: true,
                type: ['pie', 'funnel']
            },
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    color: ["#f62d51", "#dddddd","#ffbc34", "#7460ee","#009efb", "#2f3d4a","#90a4ae", "#55ce63"],
    calculable : true,
    series : [
        {
            name:'Radius mode',
            type:'pie',
            radius : [20, 110],
            center : ['50%', "50%"],
            roseType : 'radius',
            width: '40%',       // for funnel
            max: 40,            // for funnel
            itemStyle : {
                normal : {
                    label : {
                        show : true
                    },
                    labelLine : {
                        show : true
                    }
                },
                emphasis : {
                    label : {
                        show : true
                    },
                    labelLine : {
                        show : true
                    }
                }
            },
            data:[
                {value:35, name:'rose6'},
                {value:30, name:'rose7'},
                {value:40, name:'rose8'}
            ]
        },
    ]
};



// use configuration item and data specified to show chart
pieChart.setOption(option, true), $(function() {
            function resize() {
                setTimeout(function() {
                    pieChart.resize()
                }, 100)
            }
            $(window).on("resize", resize), $(".sidebartoggler").on("click", resize)
        });
