/*
 Highcharts JS v10.0.0 (2022-03-07)

 (c) 2009-2021 Torstein Honsi

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/themes/dark-unica",["highcharts"],function(b){a(b);a.Highcharts=b;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function b(a,c,b,d){a.hasOwnProperty(c)||(a[c]=d.apply(null,b),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:c,module:a[c]}})))}a=a?a._modules:{};b(a,
    "Extensions/Themes/DarkUnica.js",[a["Core/DefaultOptions.js"],a["Core/Utilities.js"]],function(a,c){var b=a.setOptions,d=c.createElement,e;(function(a){a.options={colors:"#2b908f #90ee7e #f45b5b #7798BF #aaeeee #ff0066 #eeaaee #55BF3B #DF5353 #7798BF #aaeeee".split(" "),chart:{backgroundColor:{linearGradient:{x1:0,y1:0,x2:1,y2:1},stops:[[0,"#2a2a2b"],[1,"#3e3e40"]]},style:{fontFamily:"'Unica One', sans-serif"},plotBorderColor:"#606063"},title:{style:{color:"#E0E0E3",textTransform:"uppercase",fontSize:"20px"}},
    subtitle:{style:{color:"#E0E0E3",textTransform:"uppercase"}},xAxis:{gridLineColor:"#707073",labels:{style:{color:"#E0E0E3"}},lineColor:"#707073",minorGridLineColor:"#505053",tickColor:"#707073",title:{style:{color:"#A0A0A3"}}},yAxis:{gridLineColor:"#707073",labels:{style:{color:"#E0E0E3"}},lineColor:"#707073",minorGridLineColor:"#505053",tickColor:"#707073",tickWidth:1,title:{style:{color:"#A0A0A3"}}},tooltip:{backgroundColor:"rgba(0, 0, 0, 0.85)",style:{color:"#F0F0F0"}},plotOptions:{series:{dataLabels:{color:"#F0F0F3",
    style:{fontSize:"13px"}},marker:{lineColor:"#333"}},boxplot:{fillColor:"#505053"},candlestick:{lineColor:"white"},errorbar:{color:"white"}},legend:{backgroundColor:"rgba(0, 0, 0, 0.5)",itemStyle:{color:"#E0E0E3"},itemHoverStyle:{color:"#FFF"},itemHiddenStyle:{color:"#606063"},title:{style:{color:"#C0C0C0"}}},credits:{style:{color:"#666"}},labels:{style:{color:"#707073"}},drilldown:{activeAxisLabelStyle:{color:"#F0F0F3"},activeDataLabelStyle:{color:"#F0F0F3"}},navigation:{buttonOptions:{symbolStroke:"#DDDDDD",
    theme:{fill:"#505053"}}},rangeSelector:{buttonTheme:{fill:"#505053",stroke:"#000000",style:{color:"#CCC"},states:{hover:{fill:"#707073",stroke:"#000000",style:{color:"white"}},select:{fill:"#000003",stroke:"#000000",style:{color:"white"}}}},inputBoxBorderColor:"#505053",inputStyle:{backgroundColor:"#333",color:"silver"},labelStyle:{color:"silver"}},navigator:{handles:{backgroundColor:"#666",borderColor:"#AAA"},outlineColor:"#CCC",maskFill:"rgba(255,255,255,0.1)",series:{color:"#7798BF",lineColor:"#A6C7ED"},
    xAxis:{gridLineColor:"#505053"}},scrollbar:{barBackgroundColor:"#808083",barBorderColor:"#808083",buttonArrowColor:"#CCC",buttonBackgroundColor:"#606063",buttonBorderColor:"#606063",rifleColor:"#FFF",trackBackgroundColor:"#404043",trackBorderColor:"#404043"}};a.apply=function(){d("link",{href:"https://fonts.googleapis.com/css?family=Unica+One",rel:"stylesheet",type:"text/css"},null,document.getElementsByTagName("head")[0]);b(a.options)}})(e||(e={}));return e});b(a,"masters/themes/dark-unica.src.js",
    [a["Core/Globals.js"],a["Extensions/Themes/DarkUnica.js"]],function(a,b){a.theme=b.options;b.apply()})});
    //# sourceMappingURL=dark-unica.js.map