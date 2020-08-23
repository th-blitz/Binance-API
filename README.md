Binance API 

Main file -> HeyBinance.py

How to use HeyBinance.py? 

-> HeyBinance.GetServerStatus() will get you the server status if active or under maintainence.
-> HeyBinance.GetPriceTicker(ListOfCoins) must be passed as a list eg: ListOfCoins=['BTCUSDT','ETHUSDT',....] OR ['BNBBTC'] and so on.
-> HeyBinance.GetCandleStickData(ListOfCoins,ListOfIntervals,fromwhen,tillwhen) will get you candlestick data in raw form , 
    listofcoin must be passed as a list eg: ListOfCoins=['BTCUSDT','ETHUSDT',....]. 
    listofintervals must be passed as a list eg:['1h'] Or ['1h','1m','4h',..] etc.
    fromwhen and tillwhen are starttime and endtime which must be passed as strings in the following format eg: 'June 4, 2020' OR "11 hours ago UTC" OR 'now utc' etc
-> HeyBinance.GetAccountSnapshot(AccountType,ApiKey,SecretKey) 
    accounttype='SPOT' OR 'MARGIN' etc
    apikey='0xhfkasl***************************lakfsajh'
    secretkey='kslhafkja*************************jhalsghas'
-> HeyBinance.PlaceNewMarketOrder(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,BUY_or_SELL,quantity_Of_BTC_or_BNB_or_ETH_etc,Set_Any_Unique_Order_ID_in_string_format,ApiKey,SecretKey)
    eg: (LTCBNB , BUY, 32.456 ,'34th_order',apikey,sceretkey)
-> HeyBinance.PlaceNewLimitOrder(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,BUY_or_SELL,quantity_Of_BTC_or_BNB_or_ETH_etc,Price,timeinforce_GTC_or_IOK_or_FOK,
                                    Set_Any_Unique_Order_ID_in_string_format,ApiKey,SecretKey)
    eg: (LTCBNB , BUY, 32.456 ,41.75,'IOK','89th_order',apikey,sceretkey
-> HeyBinance.CancelaOrder(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,Your_Unique_Order_ID,ApiKey,SecretKey)
    canceling a order by previously assigned unique ID
-> HeyBinance.CancelAllOrders(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,ApiKey,SecretKey)
    cancels all active order for a specified symbol like BTCUSDT OR XRPBNB etc
-> HeyBinance.CheckOrderStatus(BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,Your_Unique_Order_ID,ApiKey,SecretKey)
    checks for order status of assigned unique id for a perticular symbol.
-> HeyBinance.CheckForCurrentOpenOrders(ALL_BTCUSDT_or_BNBUSDT_or_BTCBNB_etc,ApiKey,SecretKey)
    checks for all open orders for a perticular symbol
-> HeyBinance.GetAccountInfo(ApiKey,SecretKey)
    returns a short description of your account
-> HeyBinance.GetCandleStickDataOHLCV(ListOfCoins,ListOfIntervals,fromwhen,tillwhen)
    same as the above function for candlestick data but returns pandas data base with TIME,OPEN,HIGH,LOW,CLOSE,VOLUME columns for all the coins and its intervals present in the list.

--->>> I MAY BE UPDATING THIS REPOSITORY WITH MORE EXCHANGES (BOTH CRYPTO AND STOCK) AND ALSO WITH MORE FEATURES IN THE FUTURE <<<--- 

