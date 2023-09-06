#########################################################################################################################
###      This is me in 2020 trying to automate my crypto market activities. This code is not optimal and need more    ###
###      attention but is a good foundation for a strategy on fluctuating indices                                     ###
#########################################################################################################################

import time

import numpy as np
import pandas as pd
import talib as talib
import talib.abstract as tb
import smtplib                           
from binance.client import Client
import sqlite3

class Bot:

    min_amount_dict = {'ETHBTC': '0', 'LTCBTC': '0.01', 'NEOBTC': '0.01', 'GASBTC': '0', 'BCCBTC': '0',
                       'MCOBTC': '0', 'WTCBTC': '0', 'QTUMBTC': '0', 'OMGBTC': '0', 'ZRXBTC': '0', 'STRATBTC': '0',
                       'SNGLSBTC': '0', 'BQXBTC': '0', 'KNCBTC': '0', 'FUNBTC': '0', 'SNMBTC': '0', 'LINKBTC': '0',
                       'XVGBTC': '0', 'CTRBTC': '0', 'SALTBTC': '0', 'IOTABTC': '0', 'MDABTC': '0', 'MTLBTC': '0',
                       'SUBBTC': '0', 'EOSBTC': '0', 'SNTBTC': '0', 'ETCBTC': '0', 'MTHBTC': '0', 'ENGBTC': '0',
                       'DNTBTC': '0', 'BNTBTC': '0', 'ASTBTC': '0', 'DASHBTC': '3', 'ICNBTC': '0', 'OAXBTC': '0',
                       'BTGBTC': '0', 'EVXBTC': '0', 'REQBTC': '0', 'LRCBTC': '0', 'VIBBTC': '0', 'HSRBTC': '0',
                       'TRXBTC': '0', 'POWRBTC': '0', 'ARKBTC': '0', 'YOYOBTC': '0', 'XRPBTC': '0', 'MODBTC': '0',
                       'ENJBTC': '0', 'STORJBTC': '0', 'VENBTC': '0', 'KMDBTC': '0', 'RCNBTC': '0', 'NULSBTC': '0',
                       'RDNBTC': '0', 'XMRBTC': '0', 'DLTBTC': '0', 'AMBBTC': '0', 'BATBTC': '0', 'ZECBTC': '0',
                       'BCPTBTC': '0', 'ARNBTC': '0', 'GVTBTC': '0', 'CDTBTC': '0', 'GXSBTC': '0', 'POEBTC': '0',
                       'QSPBTC': '0', 'BTSBTC': '0', 'XZCBTC': '0', 'LSKBTC': '0', 'TNTBTC': '0', 'FUELBTC': '0',
                       'MANABTC': '0', 'BCDBTC': '0', 'DGDBTC': '0', 'ADXBTC': '0', 'ADABTC': '0', 'PPTBTC': '0',
                       'CMTBTC': '0', 'XLMBTC': '0', 'CNDBTC': '0', 'LENDBTC': '0', 'WABIBTC': '0', 'TNBBTC': '0',
                       'WAVESBTC': '0.01', 'ICXBTC': '0', 'GTOBTC': '0', 'OSTBTC': '0', 'ELFBTC': '0', 'AIONBTC': '0',
                       'NEBLBTC': '0', 'BRDBTC': '0', 'EDOBTC': '0', 'WINGSBTC': '0', 'NAVBTC': '0', 'LUNBTC': '0',
                       'TRIGBTC': '0', 'APPCBTC':'0','VIABTC':'0','ONTBTC':'0','XEMBTC':'0','RVNBTC':'0','DCRBTC':'0.001',
                       'SXPBTC':'0','FORBTC':'1','FTTBTC':'0.01','SANDBTC':'0','SRMBTC':'0'}
    now = time.ctime()
    maxSpendInBTC = 0.001
    maxNumberOfCurrencies = 15
#    interval = '15m'
    interval = ['15m','1h','4h']

    def __init__(self):

        f = open("account_info.txt", 'r')
        message = f.read().split("\n")
        
        f2 = open("coins", 'r')
        self.coins = f2.read().split("\n")
        self.coins = [x for x in self.coins if x != '']  # Remove the empty caracter
        
        print("Starting the Bot.")
        self.client = Client(message[0], message[1])
        self.BTC = 0  # available USD dollars
        self.balance = []  # shows currencies with amounts(0.0 currencies are also included)
        self.available_currencies = []  # shows only available currencies
        self.refreshBalance()
        time.sleep(2)
        
        to_trade = self.coins
        stock = self.available_currencies
        for y in stock:
            to_trade = [x for x in to_trade if x != y]
        print("Available coins to trade", to_trade)
        print("available currency for sale",self.available_currencies)
        print("Bot initialized")

    def run(self):
        
        print("Bot is running")
        while True:
            for coin in self.coins:
                buy = 0
                sell = 0
                #print("........................................................coin '", coin,"'","checked")
                for minute in self.interval:
                    
                    try:
                        klines = self.client.get_klines(symbol=coin, interval= minute, startTime=0, endTime=int(round(time.time() * 1000)))
                        array = np.array(klines, dtype='f8')
                        df = pd.DataFrame(data=array[:, 0:6], columns=["date", "open", "high", "low", "close", "volume"])
#                        
                        plus_di = tb.PLUS_DI(df, timeperiod=20)
                        
                        minus_di = tb.MINUS_DI(df, timeperiod=20)
                        
                        Close = df["close"]
#                        Open = df["open"]
#                        High = df["high"]
#                        Low  = df["low"]
                        Close10_chg  = df["close"].pct_change(10)
                        Close10_chg  = Close10_chg[len(Close10_chg) - 1]
                        Volume  = df["volume"].pct_change(3)
                        Volume  = Volume[len(Volume) - 1]

                        
                        upperBB, lowerBB, old_upperBB, old_lowerBB,old_upperBB_2, old_lowerBB_2 = self.BBANDS(df, length=20, mult=1.75)
                        upperKC, lowerKC, old_upperKC, old_lowerKC = self.MA(df, length=20, mult=1.75)
                        mfi       = self.MFI(df, length=23)
                        fastk, fastd = self.STOCH(df)
                        rsi       = self.RSI(df, length=9)
                        cci       = self.CCI(df, length=20 )
                        adx       = self.ADX(df )
                        ema       = self.EMA(df)
                        ema20     =  self.EMA20(df)
                        ema10     =  self.EMA10(df)
                        ema5      =  self.EMA5(df)
                        plus      = plus_di[len(plus_di) - 1]
                        old_plus  = plus_di[len(plus_di) - 2]
                        minus     = minus_di[len(minus_di) - 1]
                        old_minus = minus_di[len(minus_di) - 2]
                        price     = Close[len(Close) - 1]
                        def count_bb():          # combien de fois le close depasse le BB
                            upper_count = 0      # combien de fois le close depasse le upper_BB
                            lower_count = 0      # combien de fois le close depasse le lower_BB
                            upper_n = 5          # apres combien de depassement on vent
                            lower_n = 4          # apres combien de depassement on achete
                            bbands = tb.BBANDS(df ,  timeperiod=20)
                            UpperBB = bbands["upperband"]
                            LowerBB = bbands["lowerband"]
                            for i in range (100):
                                if Close.iloc[-1-i] > UpperBB.iloc[-1-i]: 
                                    upper_count +=1
                                    lower_count = 0
                                    #print("Upper close -{}".format(i+1),Close.iloc[-1-i], "upperBB ",upperBB.iloc[-1-i],"upper_count ",upper_count) 
                                    if upper_count > upper_n :  # quand est ce que l on doit vendre (upper_n)
                                        break
                            for i in range (100):
                                if Close.iloc[-1-i] < LowerBB.iloc[-1-i]: 
                                    lower_count +=1
                                    upper_count = 0
                                    #print("Lower close -{}".format(i+1),Close.iloc[-1-i], "upperBB ",upperBB.iloc[-1-i],"lower_count ", lower_count) 
                                    if lower_count > lower_n :  # quand est ce que l on doit vendre (lower_n)=> 
                                        break
                            return upper_count, lower_count
                        
                        def rate():
                            point = 0
                            if (mfi < 35 ):
                                point = point + 1
#                                print(coin," MFI is available + 1")
                            elif (mfi > 80):
                                point = point - 2
#                                print(coin," MFI is available - 1")
                            if (cci < -100):
                                point = point + 1
#                                print(coin," CCI is available + 1")
                            elif (cci > 200):
                                point = point - 1
#                                print(coin," CCi is available - 1")
                            if (rsi < 30):
                                point = point + 1
#                                print(coin," RSI is available + 1")
                            elif (rsi > 80):
                                point = point - 1
#                                print(coin," RSI is available - 1")
                            if (fastk < 20 or fastd < 20):
                                point = point + 1
#                                print(coin," RSI is available + 1")
                            elif (fastk > 80 or fastd > 80):
                                point = point - 1
#                                print(coin," RSI is available - 1")
                            if (ema == "buy" and mfi > 50):
                                point = point + 2
#                                print(coin," EMA is available + 1")
                            elif (ema10 > price and ema5 > price and mfi > 50 and rsi > 50):
                                point = point + 1
                            elif (ema == "sell"):
                                point = point - 1
#                                print(coin," EMA is available - 1")
                            if (minus > 25):
                                point = point + 1
#                                print(coin," MINUS is available + 1")
                            elif (minus < 8):
                                point = point - 1
#                                print(coin," MINUS is available - 1")
                            elif (minus < 6):
                                point = point - 2
#                                print(coin," MINUS is available - 2")
                            if (count_bb()[0] > 3 ):
                                point = point + 1
#                                print(coin," BBCount is available + 1")
                            
                            if (adx  > 41 ):
                                if point > 0:
                                    point = point + 2
                                if point < 0:
                                    point = point - 2
                            if (adx  > 25 and adx < 41 ):
                                if point > 0:
                                    point = point + 1
                                if point < 0:
                                    point = point - 1
                                    
                            return point
                        rate = rate()
#                        print(f"{coin} coin : rate for {minute} time interval =  ", self.rate)
                        if rate > 2 :
#                            print("rate ", self.rate)
                            buy = buy + 1
                            print(">>Buy<<: available for '", coin,"' time interval", minute, "   rate ", rate)
                            self.log_to_file(f">>Sell<< available for {coin} time interval {minute}")
#                            print(f"{coin} coin : buy total rate for {minute} time interval = ********* ", buy,"************ ") 
                        elif rate < -2 :
                            sell = sell + 1
                            print(">>Sell<< available for '", coin,"' time interval", minute, "   rate ", rate)
                            self.log_to_file(f">>Sell<< available for {coin} time interval {minute}")
                            
#                            print("rate ", self.rate)
#                            print(f"{coin} coin : sell total rate for {minute} time interval = ********* ", sell,"************ ") 
                    
#                            
#                    print(f"{coin} coin : buy total rate for {minute} time interval = ********* ", buy,"************ ")
#                    print(f"{coin} coin : sell total rate for {minute} time interval = ********* ", sell,"************ ")
                        
                        
    #                        if (ema5_chg > ema10_chg and ema5_1_chg < ema10_1_chg and cci < -99 and rsi < 35) or (ema5 > ema10 and ema5_old < ema10_old and roc > .7 and Volume > .01 and cci < .0001) or ((adx > 39.2 ) and (minus > 29 or rsi < 31 or plus < 8 )) :
    #                            print(coin," is available to Buy")
                        #self.buyCoin(coin, df)
    #                        if ((minus < 8 or plus > 40) and (count_bb()[0] > 4 or rsi > 78.9)) :    # SellSignal
    #                            #self.sellCoin(coin, df) 
    #                            print(coin," is available to Sell")
                       
                    except Exception as ex:
                        print("Exception", ex)
                        self.log_to_file(f"Exception {ex}")
                        time.sleep( 30.0)
                        pass
                    time.sleep(1.0)
                time.sleep(5.0)
#                print("coin", coin ,"buy rate ", buy)
#                print("coin", coin ,"sell rate ", sell)
                if (buy == len(self.interval)):
                    print("====================> Buy signal <============================coin = ", coin)
                    self.log_to_file(f"====================> Buy signal <============================coin = {coin}")
                    self.buyCoin(coin, df)

                elif(sell == len(self.interval)):
                    print("====================> Sell signal <============================coin = ", coin)
                    self.log_to_file(f"====================> Sell signal <============================coin = {coin}")
                    self.sellCoin(coin, df) 
                db_coin_list = self.db_coin_list()
                if coin in db_coin_list:
                    buy_price = self.get_buy_price(coin)
                    profit    = (price - buy_price)/buy_price
                    if profit  > .125:
                        self.sellCoin(coin, df)  
            print("----------------------------------------------------------",time.ctime()," running")
            self.log_to_file(f"----------------------------------------------------------{time.ctime()} Running")            
            time.sleep( 7*60)
            
    def buyCoin(self, coin, df):
        self.refreshBalance()

        if (coin not in self.available_currencies):
            print("Buying coin attempt: " + coin)
            print("Available currencies: " + str(self.available_currencies))

            if float(self.BTC) < 0.0011:
                print("Less than 0.001 BTC", self.BTC)
                min_coin = ""
                min_plus = 100   # PLUS_DI minimal
                min_df = None

                for curr_coin in self.available_currencies:
                    klines = self.client.get_klines(symbol=curr_coin, interval=Bot.interval)
                    array = np.array(klines, dtype='f8')
                    df = pd.DataFrame(data=array[:, 0:6], columns=["date", "open", "high", "low", "close", "volume"])
                    #roc1 = tb.ROC(df, timeperiod=1)
                    plus_di = tb.PLUS_DI(df, timeperiod=20)
                    minus_di = tb.MINUS_DI(df, timeperiod=20)
                    upperBB, lowerBB, old_upperBB, old_lowerBB = self.BBANDS(df, length=20, mult=1.75)
                    upperKC, lowerKC, old_upperKC, old_lowerKC = self.KELCH(df, length=20, mult=1.5)
                    plus_old = plus_di[len(plus_di) - 2]
                    #print("min_plus ",min_plus,"plus_old ",plus_old,"lowerBB ",lowerBB,"lowerKC ",lowerKC, "upperBB ",upperBB,"upperKC ",upperKC)
                    if min_plus > plus_old and lowerBB > lowerKC and upperBB < upperKC:
                        min_coin = curr_coin
                        min_plus = plus_old
                        min_df = df
                    print("traitement du solde insuffisant ",curr_coin )   
                    if min_plus < 25:
                        self.sellCoin(min_coin, min_df)
                        self.refreshBalance()
                        time.sleep(30.0)
                    
            else:
                price = df["close"][len(df) - 1]
                min_amount = int(float(Bot.min_amount_dict[coin]))
                amount = self.maxSpendInBTC / float(price)
                amount = round(amount, min_amount)
                while amount * price < 0.001:
                    amount += pow(10, -min_amount)
                print("Buying", amount, coin, "at", price)
                self.add_trade(coin, price)
                self.client.create_order(symbol=coin, side="BUY", type="MARKET", quantity=amount)
                self.email("Buy Signal",f"Buying {amount} {coin} at {price} time ={time.ctime()}")
                self.log_to_file(f"Buying {amount} {coin} at {price} time ={time.ctime()}")
                self.refreshBalance()

    def sellCoin(self, coin, df):
        self.refreshBalance()
        if (coin in self.available_currencies):                  # Les pairs disponibles a la vente
            print("Selling coin attempt: " + coin)
            print("Available currencies: " + str(self.available_currencies))
            amount = 0
            min_amount = int(Bot.min_amount_dict[coin])
            for asset in self.balance:
                if asset["asset"] == coin:
                    amount = asset["free"]
                    amount = round(amount, min_amount)
                    if amount > asset["free"]:
                        amount = asset["free"] - pow(10, -min_amount)
                        amount = round(amount, min_amount)
            price = df["close"][len(df) - 1]
            print("Selling", amount, coin, "at", price)
            print("Selling", amount, coin)
            self.client.create_order(symbol=coin, side="SELL", type="MARKET", quantity=amount)
            self.email("Sell Signal",f"Selling {amount} {coin} at {price} time ={time.ctime()}")
            self.log_to_file(f"Selling {amount} {coin} at {price} time ={time.ctime()}")
            
            db_coin_list = self.db_coin_list()
            if coin in db_coin_list:
                self.del_trade(coin)
            self.refreshBalance()

    def refreshBalance(self):
        asset_dict = self.client.get_account()['balances']
        if (asset_dict != None):
            self.available_currencies = []
            self.balance = []
            for asset in asset_dict:
                asset['free'] = float(asset['free'])
                asset['locked'] = float(asset['locked'])
                if asset['asset'] == 'BTC':
                    self.BTC = float(asset['free'])
                elif (asset['free'] > 0.0 and (asset["asset"] + "BTC" in self.coins)):
                        min_amount = pow(10, -int(float(Bot.min_amount_dict[asset['asset'] + 'BTC'])))
                        if (asset['free'] >= min_amount):
                            asset['asset'] = asset['asset'] + 'BTC'
                            self.available_currencies.append(asset['asset'])
                            self.balance.append(asset)

    def del_trade(self, coin):
        conn = sqlite3.connect('trade_db.db')
        c = conn.cursor()
        c.execute("DELETE FROM trade WHERE coin = :coin",{'coin': coin})
        conn.commit()
        conn.close()
    
    def db_coin_list(self):
        conn = sqlite3.connect('trade_db.db')
        c = conn.cursor()
        c.execute("SELECT coin FROM trade ")
        coin_list = c.fetchall()
        curr_list = []
        for i in range(len(coin_list)):
            curr_list.append(coin_list[i][0])
        conn.commit()
        conn.close()
        return curr_list
    
    def add_trade(self, coin, price):
        now = time.ctime()
        conn = sqlite3.connect('trade_db.db')
        c = conn.cursor()
        c.execute("INSERT INTO trade VALUES (:coin,:price, :statut, :o_date)", {'coin': coin, 'price': price , 'statut':0, 'o_date':now})
        conn.commit()
        conn.close()

    def get_buy_price(self, coin):
        conn = sqlite3.connect('trade_db.db')
        c = conn.cursor()
        c.execute("SELECT price FROM trade WHERE coin =:coin",{'coin':coin})
        buy_price = c.fetchone()[-1]
        conn.commit()
        conn.close()
        return buy_price
    
    def update_statut(self, coin):
        conn = sqlite3.connect('trade_db.db')
        c = conn.cursor()
        c.execute("UPDATE trade SET statut = :statut WHERE coin = :coin",{'statut': 1, 'coin': coin})
        conn.commit()
        conn.close()
        
    def BBANDS(self, df, length, mult):
        bbands = tb.BBANDS(df * 100000, nbdevup=mult, nbdevdn=mult, timeperiod=length)
        upperBB = bbands["upperband"] / 100000
        lowerBB = bbands["lowerband"] / 100000
        return upperBB[len(upperBB) - 1], lowerBB[len(lowerBB) - 1], upperBB[len(upperBB) - 2], lowerBB[
            len(lowerBB) - 2], upperBB[len(upperBB) - 3], lowerBB[len(lowerBB) - 3],

    def MA(self, df, length, mult):
        ma = tb.MA(df, timeperiod=length)
        range = tb.TRANGE(df)
        rangema = talib.MA(np.array(range), timeperiod=length)
        upperKC = ma + rangema * mult
        lowerKC = ma - rangema * mult
        return upperKC[len(upperKC) - 1], lowerKC[len(lowerKC) - 1], upperKC[len(upperKC) - 2], lowerKC[
            len(lowerKC) - 2]
        
    def RSI(self, df, length):
        rsi = tb.RSI(df, timeperiod = length)
        return rsi[len(rsi) - 1]
        
    def CCI(self, df, length):
        cci = tb.CCI(df, timeperiod = length)
        return cci[len(cci)-1]
    
    def MFI(self, df, length):
        mfi = tb.MFI(df, timeperiod = length)
        return mfi[len(mfi)-1]
    
    def EMA(self, df):
        buy = 0
        sell = 0
        for period in [5,10,20]:
            real = tb.EMA(df, timeperiod = period)
            ema = real[len(real)-1]
            price = df['close'][len(df['close']) - 1]
            if (ema < price):
                #print("EMA: " + str(value) + " sell")
                sell = sell + 1
            elif (ema > price ):
                #print("EMA: " + str(value) + " buy")
                buy = buy + 1
        if (sell == 3):
            #print("EMA: sell")
            return "sell"
        elif (buy == 3):
            #print("EMA: buy")
            return "buy"
        else:
            #print("EMA: neutral")
            return "neutral"
    
    def ADX(self ,df):
        adx = tb.ADX(df, timeperiod= 14)
        return adx[len(adx) - 1]
    
    def EMA20(self, df):
        ema = tb.EMA(df, timeperiod = 20)
        return ema[len(ema) - 1]
    
    def EMA10(self, df):
        ema = tb.EMA(df, timeperiod = 10)
        return ema[len(ema) - 1]
    
    def EMA5(self, df):
        ema = tb.EMA(df, timeperiod = 5)
        return ema[len(ema) - 1], 
    
    def SMA(self, df):
        ema = tb.EMA(df, timeperiod = 5)
        return ema[len(ema) - 1]
    
    def STOCH(self, df):
        stochstic = tb.STOCHRSI(df, fastk_period=14, fastd_period=14, fastd_matype=0)
        fastk = stochstic["fastk"]
        fastd = stochstic["fastd"]
        return fastk[len(fastk) - 1], fastd[len(fastd) - 1]
    
    def log_to_file(self, message):
        f = open("Bot_DataLog.txt", "a+")
        f.write('\n'+str(message)+f" {time.ctime()}")
        f.close()
    
    def email(self, obj, mess ):
        
        sender_address = "c*****.n*****@gmail.com" #  Gmail address
         
        receiver_address = "c*****.n*****@gmail.com" #  email address
         
        a_xxx = "M*****(*****" # The Gmail account password
         
        subject = obj
         
        body = mess 
        message = f"Subject: {subject}\n\n{body}"
         
        try:
    #           
        	    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        	    server.ehlo()
        	    server.login(sender_address, a_xxx)
        	    server.sendmail(sender_address, receiver_address, message)
        	    server.close()
    #    
        	    print ('Email sent!')
        except:
        	    print ('Something went wrong with email...') 
    
bot = Bot()
bot.run()
