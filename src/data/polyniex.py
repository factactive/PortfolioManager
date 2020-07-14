import json
import time
import sys
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from src.config.config import *


minute = 60
hour = minute*60
day = hour*24
week = day*7
month = day*30
year = day*365

# Possible Commands
p = EndPoints
PUBLIC_COMMANDS = [p.returnTicker.name, p.return24Volume.name, p.returnOrderBook.name, p.returnTradeHistory.name, p.returnChartData.name , p.returnCurrencies.name, p.returnLoanOrders.name]

class Poloniex:
    def __init__(self, APIKey='', Secret=''):
        self.APIKey = APIKey.encode()
        self.Secret = Secret.encode()
        self.EndPointsAPI = EndPoints
        # Conversions
        self.timestamp_str = lambda timestamp=time.time(), format="%Y-%m-%d %H:%M:%S": datetime.fromtimestamp(timestamp).strftime(format)
        self.str_timestamp = lambda datestr=self.timestamp_str(), format="%Y-%m-%d %H:%M:%S": int(time.mktime(time.strptime(datestr, format)))
        self.float_roundPercent = lambda floatN, decimalP=2: str(round(float(floatN) * 100, decimalP))+"%"

        # PUBLIC COMMANDS
        self.marketTicker = lambda x=0: self.api(self.EndPointsAPI.returnTicker.name)
        self.marketVolume = lambda x=0: self.api(self.EndPointsAPI.return24Volume.name)
        self.marketStatus = lambda x=0: self.api(self.EndPointsAPI.returnCurrencies.name)
        self.marketLoans = lambda coin: self.api(self.EndPointsAPI.returnLoanOrders.name,{'currency':coin})
        self.marketOrders = lambda pair='all', depth=10:\
            self.api(self.EndPointsAPI.returnOrderBook.name, {'currencyPair':pair, 'depth':depth})
        self.marketChart = lambda pair, period=day, start=time.time()-(week*1), end=time.time(): self.api(self.EndPointsAPI.returnChartData.name, {'currencyPair':pair, 'period':period, 'start':start, 'end':end})
        self.marketTradeHist = lambda pair: self.api(self.EndPointsAPI.returnTradeHistory.name,{'currencyPair':pair}) # NEEDS TO BE FIXED ON Poloniex

    #####################
    # Main Api Function #
    #####################
    def api(self, command, args={}):
        """
        returns 'False' if invalid command or if no APIKey or Secret is specified (if command is "private")
        returns {"error":"<error message>"} if API error
        """
        if command in PUBLIC_COMMANDS:
            url = 'https://poloniex.com/public?'
            args['command'] = command
            ret = urlopen(Request(url + urlencode(args)))
            return json.loads(ret.read().decode(encoding='UTF-8'))
        else:
            return False
