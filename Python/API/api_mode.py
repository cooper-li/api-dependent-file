#coding=utf-8

__author ='Ray'


import time
import hashlib
import requests
import requests.packages.urllib3.util.ssl_
import json
import ConfigParser

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

class API_Mode():
    def __init__(self):
        parser = ConfigParser.ConfigParser()
        parser.read("infor.conf")
        self.Secret = parser.get("key","Secret")
        self.ApiKey = parser.get("key","ApiKey")
        self.TradePw = parser.get("key","TradePw")
        self.URL = parser.get("key","URL")

    def httpsGet(self, url):
        response = requests.get(url)
        return response

    def httpsPost(self,url,params):
        response = requests.post(url=url,params=params)
        return response

    #签名
    def signature(self):
        iniSign = ''
        list = []
        for key in sorted(self.params.keys()):
            iniSign += key + '=' + str(self.params[key]) + '&'
            signs = iniSign[:-1]
            list.append(signs)
        sign = list[-1]
        data = sign + str(self.Secret)
        self.params['sign'] = hashlib.md5(data.encode("utf8")).hexdigest().lower()
        return self.params['sign']


    # 获取牌价
    def ticker(self,symbol):
        """
        :param symbol: eth_btc
        :return: {
                    "code": 0, //Status code
                    "msg": "Success", //Status
                    "data": {
                        "date": 1505472441,  //time stamp
                        "last": 0, New Price
                        "buy": "0.10000000",  //first buy price
                        "sell": 0,  //first sell pric
                        "high": 0,  //max price
                        "low": 0,  //min price
                        "vol": 0  //24 Volume
                    }
                }
        """
        __url = self.URL + "/Market/ticker?symbol=%s"%(symbol)
        __response = API_Mode().httpsGet(url=__url)
        return __response


    # 获取所有牌价数据
    def tickerall(self):
        """
        :return:
            {
                "code": 0, //Status code
                "msg": "Success", //Status
                "data": {
                    "ltc_btc": {
                     "date": 1506063078,  //time stamp
                     "last": "0.01297061", //  New Price
                     "buy": "0.01296937", //first buy price
                     "sell": "0.01297061", //first sell pric
                     "high": "0.01355093", //max price
                     "low": "0.01263860", //min price
                     "vol": "41417.9852" //24 Volume
                 },
                 "eth_btc": {
                      "date": 1506063078,
                      "last": "0.07262708",
                      "buy": "0.07262708",
                      "sell": "0.07265075",
                      "high": "0.07396673",
                      "low": "0.07064294",
                      "vol": "6088.3691"
                 },
               }
             }
        """
        __url = self.URL + "/Market/tickerall"
        __response = API_Mode().httpsGet(url=__url)
        return __response



    #获取深度数据
    def depth(self,symbol):
        """
        :param symbol: eth_btc
        :return: {
                    "code":0, // Status code
                    "msg":"Success", // Status
                    "data":{
                    "asks":[[0.00417,5000],[0.004,229.6829],[0.003,350]],//asks Trust Buy Order [Trust Order Price, Trust Order Number]
                    "bids":[[0.00024,2021.3688],[0.00023262,702.5492]],//bids Trust Sell Order[Trust Order Price, Trust Order Number]
                    "date":1506047161 //time stamp
                    }
                }
        """
        __url = self.URL + "/Market/depth?symbol=%s"%(symbol)
        __response = API_Mode().httpsGet(url=__url)
        return __response



    # 成交单
    def order(self,symbol):
        """
        :param symbol: bz_usdt
        :return:{
                  "code": 0,  // Status code
                  "msg": "Success", // Status
                  "data": {
                  "max": 0, // max price
                  "min": 0, // min price
                  "sum": 0, // Volume
                  "d": [{
                        "t": "00:00:00", // time
                        "p": 0, // order price
                        "n": 0, // order number
                        "s": "sell|buy" // order type
                          }]
                   }
                }

        """
        __url = self.URL + "/Market/order?symbol=%s" % (symbol)
        response = API_Mode().httpsGet(url=__url)
        return response



    #获取K线数据
    def kline(self,symbol,resolution,size,toTime=None):
        """
        :param symbol:eos_btc
        :param resolution: x min ,x hour , x day
        :param size: max 300
        :return:
            {
              "code": 0, // Status code
              "msg": "Success", //Status
              "data": {
                "des": "",
                "isSuc": true,
                "datas": {
                  "USDCNY": "**",
                  "contractUnit": "MZC",
                  "data": "[[1494235500000,1.00000000,1.00000000,1.00000000,1.00000000,1.0000],
                      [1494412200000,1.00000000,1.00000000,1.00000000,1.00000000,1.0000],
                      [1495869000000,0.00100000,0.00100000,0.00100000,0.00100000,100.0000],
                      [1495869900000,0.10000000,0.10000000,0.10000000,0.10000000,100.0000],
                      [1497255000000,0.00010000,0.00010000,0.00010000,0.00010000,10.0000]]",
                  "marketName": "",
                  "moneyType": "BTC",
                  "symbol": "mzc_btc",
                  "url": ""
                }
              }
            }
        #             """
        if toTime != None:
            __toTime = time.strptime(toTime, "%Y-%m-%d %H:%M:%S")
            toTimeStamp = int(time.mktime(__toTime)*1000)
            if size < 300:
                return "size max 300！"
            else:
                to = toTimeStamp
                __url = self.URL + "/Market/kline?symbol=%s&resolution=%s&size=%s&to=%s" % (symbol,resolution,size,to)
                response = API_Mode().httpsGet(url=__url)
                return  response
        else:
            if size < 300:
                return "size max 300！"
            else:
                __url = self.URL + "/Market/kline?symbol=%s&resolution=%s&size=%s" % (symbol,resolution,size)
                response = API_Mode().httpsGet(url=__url)
                return response


    #获取交易对信息
    def symbolList(self):
        """
        :return:
            {
                "code": 0, //Status code
                "msg": "Success", //Status
                "data": {
                    "bnty_btc": {
                              "currencyCoin": "btc",
                              "symbol": "bnty_btc",
                              "pricePrecision": 8,
                              "maxTrade": "500000000.000",
                              "minTrade": "50.000",
                              "coin": "bnty",
                              "numberPrecision": 4
               }
             }
                    """
        __url = self.URL + "/Market/symbolList"
        __response = API_Mode().httpsGet(url=__url)
        return __response



    #获取当前法币汇率信息
    def currencyRate(self):
        """
        :return:
                {
                "status": 200,
                "msg": "",
                "data": {
                    "cny_usdt": {
                        "coin": "cny",
                        "currencyCoin": "usdt",
                        "rate": "0.146471",
                        "rateTime": "2018-08-03 23:29:03",
                        "ratenm": "cny/usdt",
                        "flatform": "api.k780.com",
                        "created": 1533461732,
                        "timezone": "PRC"
                    },
                },
                "time": 1533462219,
                "microtime": "0.56846900 1533462219",
                "source": "api"
            }
        """
        __url = self.URL + "/Market/currencyRate"
        __response = API_Mode().httpsGet(url=__url)
        return __response



    #获取虚拟货币法币汇率信息
    def currencyCoinRate(self):
        """
        :return:
                {
                    "status": 200,
                    "msg": "",
                    "data": {
                        "btc": {
                            "usdt": "7392.98000000",
                            "dkkt": "47619.53224133",
                            "eth": "17.85045531",
                            "cny": "50474.01874773",
                            "jpy": "822173.04270462",
                            "usd": "7392.98000000",
                            "dkk": "47619.53224133",
                            "btc": "1"
                        },
                    },
                    "time": 1533382048,
                    "microtime": "0.65652200 1533382048",
                    "source": "api"
                }
        """
        __url = self.URL + "/Market/currencyCoinRate"
        __response = API_Mode().httpsGet(url=__url)
        return __response



    #获取币种对应汇率信息
    def coinRate(self):
        """
        :return:
                {
                "status": 200,
                "msg": "",
                "data": {
                    "777": {
                        "usdt": "0.01123732",
                        "dkkt": "0.07238168",
                        "eth": "0.00002713",
                        "cny": "0.07672050",
                        "jpy": "1.24970302",
                        "usd": "0.01123732",
                        "dkk": "0.07238168",
                        "btc": "0.00000152"
                    },
                },
                "time": 1533382189,
                "microtime": "0.96448500 1533382189",
                "source": "api"
            }
        """
        __url = self.URL + "/Market/currencyCoinRate"
        __response = API_Mode().httpsGet(url=__url)
        return __response




    #提交委托单
    def addEntrustSheet(self,_type,price,number,symbol):
        """
        :param _type: 1:buy  2:sell
        :param price: order price
        :param number: trust order number
        :param symbol: Trading of column
        :return:
        """

        self.params = {}
        self.params['apiKey'] = self.ApiKey
        self.params['timeStamp'] = str(int(time.time()))
        self.params['nonce'] = str(int(time.time() % 1000000))
        self.params['type'] = str(_type)
        self.params['price'] = str(price)
        self.params['number'] = str(number)
        self.params['symbol'] = str(symbol)
        self.params['tradePwd'] = self.TradePw
        self.signature()
        __url = self.URL + "/Trade/addEntrustSheet"
        __response = API_Mode().httpsPost(url=__url,params=self.params)
        return __response



    #撤销委托单
    def cancelEntrustSheet(self,entrustSheetId):
        """
        :param trustId: trust order id
        :return:
        """
        self.params = {}
        self.params['apiKey'] = self.ApiKey
        self.params['timeStamp'] = str(int(time.time()))
        self.params['nonce'] = str(int(time.time() % 1000000))
        self.params['entrustSheetId'] = str(entrustSheetId)
        self.signature()
        __url = self.URL + "/Trade/cancelEntrustSheet"
        __response = API_Mode().httpsPost(url=__url, params=self.params)
        return __response



    #批量撤销委托单
    def cancelAllEntrustSheet(self,trustAllId):
        """
        :param trustAllId: Trust order id
        :return:
        """
        self.params = {}
        self.params['apiKey'] = self.ApiKey
        self.params['timeStamp'] = str(int(time.time()))
        self.params['nonce'] = str(int(time.time() % 1000000))
        self.params['ids'] = str(trustAllId)
        self.signature()
        __url = self.URL + "/Trade/cancelAllEntrustSheet"
        __response = API_Mode().httpsPost(url=__url, params=self.params)
        return __response



    #获取个人历史委托单列表
    def getUserHistoryEntrustSheet(self,coinFrom,coinTo,page,pageSize,_type=None,startTime=None,endTime=None):

        """
        :param coinFrom: coin from
        :param coinTo: coin to
        :param _type: 1:buy 2:sell
        :param page:  current page number
        :param pageSize: a page show history entrust sheet
        :param startTime: Search start time
        :param endTime: Search end time
        :return:
        """

        self.params = {}
        self.params['apiKey'] = self.ApiKey
        self.params['timeStamp'] = str(int(time.time()))
        self.params['nonce'] = str(int(time.time() % 1000000))
        self.params['coinFrom'] = str(coinFrom)
        self.params['coinTo'] = str(coinTo)
        self.params['page'] = str(page)
        self.params['pageSize'] = pageSize
        if _type != None:
            self.params['type'] = str(_type)

        if startTime != None:
            starttimeArray= time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
            startTimeStamp = int(time.mktime(starttimeArray))
            self.params['startTime'] = startTimeStamp

        if endTime != None:
            endtimeArray = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
            endTimeStamp = str(time.mktime(endtimeArray))
            self.params['endTime'] = endTimeStamp

        self.signature()
        __url = self.URL + "/Trade/getUserHistoryEntrustSheet"
        __response = API_Mode().httpsPost(url=__url, params=self.params)
        return __response



    #获取当前委托
    def getUserNowEntrustSheet(self,coinFrom,coinTo,page,pageSize,startTime=None,endTime=None,_type=None):
        """
        :param coinFrom: coin from
        :param coinTo: coin to
        :param _type: 1:buy 2:sell
        :param page:  current page number
        :param pageSize: a page show entrust sheet
        :param startTime: Search start time   2017-06-08 12:00:00
        :param endTime: Search end time   2017-06-08 12:00:00
        :return:
        """
        self.params = {}
        self.params['apiKey'] = self.ApiKey
        self.params['timeStamp'] = str(int(time.time()))
        self.params['nonce'] = str(int(time.time() % 1000000))
        self.params['coinFrom'] = str(coinFrom)
        self.params['coinTo'] = str(coinTo)
        self.params['page'] = str(page)
        self.params['pageSize'] = str(pageSize)
        if _type != None:
            self.params['type'] = str(_type)
        if startTime != None:
            starttimeArray= time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
            startTimeStamp = int(time.mktime(starttimeArray))
            self.params['startTime'] = startTimeStamp
        if endTime != None:
            endtimeArray = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
            endTimeStamp = int(time.mktime(endtimeArray))
            self.params['endTime'] = endTimeStamp
        self.signature()
        __url = self.URL + "/Trade/getUserNowEntrustSheet"
        __response = API_Mode().httpsPost(url=__url, params=self.params)
        return __response



    #获取委托单详情
    def getEntrustSheetInfo(self,entrustSheetId):
        """
        :param entrustSheetId: trust id
        :param _type: 1:buy 2:sell
        :return:
        """
        self.params = {}
        self.params['apiKey'] = self.ApiKey
        self.params['timeStamp'] = str(int(time.time()))
        self.params['nonce'] = str(int(time.time() % 1000000))
        self.params['entrustSheetId'] = str(entrustSheetId)
        self.signature()
        __url = self.URL + "/Trade/getEntrustSheetInfo"
        __response = API_Mode().httpsPost(url=__url, params=self.params)
        return __response



    #获取用户所有资产
    def getUserAssets(self):
        """
        :return: {
            "status": 200,
                  "source": "api",
                  "microtime": "0.15746300 1532256821",
                  "time": 1532256821,
                  "msg": "",
                  "data": {
                    "info": [
                      {
                        "usd": "0.00000000",
                        "usd": "0.00000000",
                        "name": "btc",
                        "lock": "102.04000000",
                        "over": "897.96000000",
                        "cny": "0.00000000",
                        "num": "1000.00000000",
                        "btc": "0.00000000"
                      }
                    ]
                }
        """
        self.params = {}
        self.params['apiKey'] = self.ApiKey
        self.params['timeStamp'] = str(int(time.time()))
        self.params['nonce'] = str(int(time.time() % 1000000))
        self.params['secretKey'] = self.Secret
        self.signature()
        __url = self.URL + "/Assets/getUserAssets"
        __response = API_Mode().httpsPost(url=__url, params=self.params)
        return __response

