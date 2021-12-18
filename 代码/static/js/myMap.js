(function() {
  // 1. 实例化对象
  var myChart = echarts.init(document.querySelector(".map .chart"));
  // 2. 指定配置和数据
  // 2. 指定配置和数据
  window.dataList = [
    {name: "澳门", value: 0},
    {name: "香港", value: 0},
    {name: "台湾", value: 0},
    {name: "新疆", value: 0},
    {name: "宁夏", value: 0},
    {name: "青海", value: 0},
    {name: "甘肃", value: 0},
    {name: "陕西", value: 0},
    {name: "西藏", value: 0},
    {name: "云南", value: 0},
    {name: "贵州", value: 0},
    {name: "四川", value: 0},
    {name: "重庆", value: 0},
    {name: "海南", value: 0},
    {name: "广西", value: 374},
    {name: "广东", value: 420},
    {name: "湖南", value: 410},
    {name: "湖北", value: 373},
    {name: "河南", value: 0},
    {name: "山东", value: 389},
    {name: "江西", value: 385},
    {name: "福建", value: 410},
    {name: "安徽", value: 0},
    {name: "浙江", value: 0},
    {name: "江苏", value: 0},
    {name: "上海", value: 0},
    {name: "黑龙江", value: 0},
    {name: "吉林", value: 0},
    {name: "辽宁", value: 0},
    {name: "内蒙古", value: 0},
    {name: "山西", value: 0},
    {name: "河北", value: 0},
    {name: "天津", value: 0},
    {name: "北京", value: 0}
];
option = {
    tooltip: {
        triggerOn: "click",
        formatter: function(e, t, n) {
            return '.5' == e.value ? e.name + "：有疑似病例" : e.seriesName + "<br />" + e.name + "：" + e.value
        }
    }, 
    toolbox: {//右边那三个图标
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                dataView: {readOnly: false,title:'hello',textColor:"#777"},
                restore: {},
                saveAsImage: {}
            }
        }, // 提供下载工具
    visualMap: {//左边的图标
        min: 0,
        max: 100000,
        left: 26,
        bottom: 30,
        showLabel: !0,
        text: ["高", "低"],
        pieces: [{
            gt: 415,
            label: "> 415人",
            color: "#7f1100"
        }, {
            gte: 390,
            lte: 415,
            label: "390 - 415人",
            color: "#ff5428"
        }, {
            gte: 380,
            lt: 390,
            label: "380-390人",
            color: "#ff8c71"
        }, {
            gt: 370,
            lt: 380,
            label: "370 - 380人",
            color: "#ffd768"
        }, {
            value: 0,
            color: "#0025B3"
        }],
        show: !0
    },
    grid: [{
                right: '5%',
                top: '20%',
                bottom: '10%',
                width: '20%'
            },
        
        ],
    
    geo: {
        map: "china",
        // right:'25%',
        // left:'18%',
        center: [105.97, 30.71],
        roam: !1,
        scaleLimit: {//通过鼠标控制的缩放
            min: 1,
            max: 2
        },
        zoom: 1.1,//当前缩放比例
        top: 120,//组件离容器上方的距离
        label: {
            normal: {
                show: !0,
                fontSize: "14",
                color: "rgba(0,0,0,0.7)"
            }
        },
//         regions: [{
//     name: '青海',
//     label: {
//         normal: {
            
//         }
//     }
// }],
        itemStyle: {
            normal: {
                //shadowBlur: 50,
                //shadowColor: 'rgba(0, 0, 0, 0.2)',
                borderColor: "rgba(0, 0, 0, 0.5)"
            },
            emphasis: {
                areaColor: "#f2d5ad",//鼠标放上去的颜色
                shadowOffsetX: 0,
                shadowOffsetY: 0,
                borderWidth: 0
            }
        }
    },
    series: [{
        name: "僵尸企业数量",
        type: "map",
        geoIndex: 0,
        data: window.dataList}]
    // },
    // {
    //         name: '哈喽喽',
    //         type: 'scatter',
    //         itemStyle: itemStyle,
    //         data: window.dataList
    //     }
    // ]
};
  myChart.setOption(option);
  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();
