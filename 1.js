var webPage = require('webpage');
var page = webPage.create();
page.open('https://s.tradingview.com/cryptomktscreenerwidget/#{%22width%22:%22100%%22,%22height%22:%22100%%22,%22defaultColumn%22:%22moving_averages%22,%22screener_type%22:%22crypto_mkt%22,%22displayCurrency%22:%22USD%22,%22locale%22:%22zh_CN%22,%22market%22:%22crypto%22,%22enableScrolling%22:true,%22utm_source%22:%22www.knowsec.org%22,%22utm_medium%22:%22widget%22,%22utm_campaign%22:%22cryptomktscreener%22}', page.onLoadFinished=function (status) {
  var content = page.content;
  console.log('Content: ' + content);
  phantom.exit();
});
