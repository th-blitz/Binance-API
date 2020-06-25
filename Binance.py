import json
import pandas as pd
import urllib
import time
import requests
import datetime
import hmac
import hashlib
import dateparser
import pytz

keys={
    'apikey':'Ov83xBFDrXOq2AXw1RoTOm0kyqdJg1inU73vaYLyDD6F9IeioJGzyUuWxMjBHshj',
    'secretkey':'whX21dwM5JwsohZzbImlVEOpVaYkzQmkSoDHU2J330eoKTx6R7ivuhjPpEE9Tp1v'
}


def sign(message,encryptionstandard):
    if encryptionstandard=='SHA256':
        message=urllib.parse.urlencode(message)
        hashed = hmac.new(keys['secretkey'].encode(), message.encode(), digestmod=hashlib.sha256)
        signedmessage = hashed.hexdigest()
        return signedmessage

def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)

def exchangeendpoints(exchange):
    if exchange is 'binance':
        return('https://api.binance.com')
    else:
        print('Update this exchange in exchangeendpoints function')
        return('NULL')

def querystringsforinfo(exchange,userinput,label):
    if exchange is 'binance':
        headers = {"X-MBX-APIKEY": keys['apikey']}
        if userinput=='get data':
            querystring='/api/v3/klines'
            parameter=parametergenerator(userinput,label)
            endpointtype='get'
            headers='noheader'
            return(querystring,parameter,headers,endpointtype,userinput)
        elif userinput=='snap':
            querystring='/sapi/v1/accountSnapshot'
            parameter=parametergenerator(userinput,label)
            endpointtype='get'
            return(querystring,parameter,headers,endpointtype,userinput)
        elif userinput=='tick':
            querystring='/api/v3/ticker/price'
            parameter=parametergenerator(userinput,label)
            endpointtype='get'
            return(querystring,parameter,headers,endpointtype,userinput)

def parametergenerator(userinput,label):
    if userinput=='get data':
        print('enter the parameters')
        print('----NOTE ALL PARAMETERS ARE MANDATORY DUE TO CODING DIFFICULTY----')
        symbol = input('enter the symbol (mandatory) (ex:BTCUSDT):')
        interval = input('enter the interval (mandatory) (ex:1m,1h,1d,1w):')
        date_str=input('enter the start time in format (16 June, 2020 / 10 hours ago UTC / now UTC : ')
        starttime=date_to_milliseconds(date_str)
        date_str =input('endtime in the same format : ')
        endtime=date_to_milliseconds(date_str)
        limit = 1000
        plainparameter = {
            'symbol': symbol,
            'interval': interval,
            'startTime': starttime,
            'endTime': endtime,
            'limit': limit
        }
        return plainparameter
    elif userinput=='snap':
        print('enter the parameters')
        acctype=input('enter the account type in format "SPOT", "MARGIN", "FUTURES" : ')
        timestamp=date_to_milliseconds('now utc')
        plainparameter = {
            'type':acctype,
            'timestamp':timestamp
        }
        signature=sign(plainparameter,'SHA256')
        plainparameter.update({'signature':signature})
        return plainparameter
    elif userinput=='tick':
        plainparameter={
            'symbol':label
        }
        return plainparameter

def APIconnenction(exchangeendpoint,querystring,parameter,header,endpointtype,userinput):
    if userinput=='get data':
        intervalsinmilli = {'1m': 1 * 60 * 1000, '3m': 3 * 60 * 1000, '5m': 5 * 60 * 1000, '15m': 15 * 60 * 1000,
                            '30m': 30 * 60 * 1000, '1h': 1 * 60 * 60 * 1000, '2h': 2 * 60 * 60 * 1000,
                            '4h': 4 * 60 * 60 * 1000,
                            '6h': 6 * 60 * 60 * 1000, '8h': 8 * 60 * 60 * 1000, '12h': 12 * 60 * 60 * 1000,
                            '1d': 1 * 24 * 60 * 60 * 1000,
                            '3d': 3 * 24 * 60 * 60 * 1000, '1w': 1 * 7 * 24 * 60 * 60 * 1000
                            }
        inter=parameter['interval']
        intervals=(parameter['endTime'] - parameter['startTime']) / intervalsinmilli[f'{inter}']
        if intervals >=1000:
            if (intervals/1000) < (intervals%1000):
                order=(int(intervals/1000))+1
            else:
                order=int(intervals/1000)
            diff=parameter['endTime'] - parameter['startTime']
            addition=int(diff/order)
            data=[]
            end=parameter['endTime']
            parameter['endTime']=parameter['startTime']
            print(f'------>>> fetching about {int(intervals)} candelsticks data from binance ... ')
            for i in range(order):
                parameter['endTime']=parameter['endTime']+addition
                if(parameter['endTime']>end):
                    parameter['endTime']=end
                connect = requests.get(f'{exchangeendpoint}{querystring}', params=parameter)
                connect=json.loads(connect.text)
                for j in connect:
                    data.append(j)
                parameter['startTime']=parameter['endTime']
                time.sleep(0.06)
            return data
        else:
            connect = requests.get(f'{exchangeendpoint}{querystring}', params=parameter)
            return connect

    elif endpointtype is 'get':
        if header=='noheader':
            connect = requests.get(f'{exchangeendpoint}{querystring}', params=parameter)
            connect = json.loads(connect.text)
            return connect
        else:
            connect = requests.get(f'{exchangeendpoint}{querystring}', params=parameter,headers=header)
            connect = json.loads(connect.text)
            return connect

def datatopanda(rawdata,userinput,exchange):
    if exchange is 'binance':
        if userinput=='get data':
            open = []
            high = []
            low = []
            close = []
            volume = []
            datetimes = []

            for every in rawdata:
                datetimes.append(datetime.datetime.fromtimestamp(every[0]/1000.0))
                open.append(every[1])
                high.append(every[2])
                low.append(every[3])
                close.append(every[4])
                volume.append(every[5])

            df=pd.DataFrame(list(zip(datetimes,open,high,low,close,volume)), columns =['time','open', 'high','low','close','volume'])
            open.clear()
            close.clear()
            high.clear()
            low.clear()
            high.clear()
            datetimes.clear()
            volume.clear()
            rawdata.clear()
            print(df.head())
            print(df.tail())
            df.to_csv(r'E:\\Tradedata\\BTCUSDT\\4hHrCandleSticks.csv')
            return(df)
        elif userinput=='snap':
            balances=rawdata['snapshotVos'][0]['data']['balances']
            assets=[]
            free=[]
            locked=[]
            for i in balances:
                assets.append(i['asset'])
                free.append(i['free'])
                locked.append(i['locked'])
            df = pd.DataFrame(list(zip(assets,free,locked)),columns=['Coins', 'Available', 'Locked'])
            print(rawdata['snapshotVos'][0]['data']['totalAssetOfBtc'])
            print(df)
            return df

exchange='binance'
print('for account snapshot enter *snap*')
print('for account deposit history enter *deposit history*')
print('for account withdrawl history enter *withdraw history*')
print('for account trade info *acc info*')
# print('for price ticker *tick*')
print('for candlestick data *get data*')
userinput=input('enter the command my lord :')
label=None

exchangeendpoint=exchangeendpoints(exchange)
querystring,parameter,header,endpointtype,userinput=querystringsforinfo(exchange,userinput,label)
rawdata=APIconnenction(exchangeendpoint,querystring,parameter,header,endpointtype,userinput)
finaldata=datatopanda(rawdata,userinput,exchange)

