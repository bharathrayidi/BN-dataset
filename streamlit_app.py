import altair as alt
import pandas as pd
import streamlit as st
from IPython.display import clear_output
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pandasql import sqldf
import requests
import time
from bs4 import BeautifulSoup
pd.options.mode.copy_on_write = True

option_dataframe = pd.DataFrame(columns=['CALL_OI','PUT_OI','CALL_COI','PUT_COI' ,'CALL_VOL',
            'PUT_VOL','CALL_TBQ','CALL_TSQ','PUT_TBQ','PUT_TSQ',])
request_index = pd.DataFrame(columns=['key','index','indexSymbol',
'last','variation','percentChange','open','high','low','previousClose','yearHigh',
'yearLow','indicativeClose','pe','pb','dy','declines','advances','unchanged'])
max_df =  pd.DataFrame(columns=['max_CS','max_CB','max_CT','max_CTOI','max_COI','max_CCOI','STP',
                                'max_PCOI','max_POI','max_PTOI','max_PT','max_PB','max_PS'])
max_df_2 = pd.DataFrame(columns=['max_CS','max_CB','max_CBIDQ','max_CASKQ','max_CT','max_CTOI','max_COI','max_CCOI','STP',
                                'max_PCOI','max_POI','max_PTOI','max_PT','max_PBIDQ','max_PASKQ','max_PB','max_PS'])
max_df_3 =  pd.DataFrame(columns=['max_CS','max_CB','max_CT', 'max_COI','max_CCOI','STP','max_PCOI','max_POI','max_PT',
                            'max_PB','max_PS'])


url ='https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
header = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36",
    "Sec-Fetch-User": "?1", "Accept": "*/*", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
    }
session = requests.Session()
nse_live = session.get("http://nseindia.com", headers=header)
session.get(url, headers=header)

def dataframe(df):
    data = []
    for i in range(0,len(df)):
        calloi=callcoi=cltp=putoi=putcoi=pltp=0
        ctotaltradevaluem=ctotalBellq=ctotalSellq=ptotaltradevaluem=ptotalBellq=ptotalSellq=0
        pbidQty=pbidprice=paskQty=paskPrice=cbidQty=cbidprice=caskQty=caskPrice = 0
        stp = df['strikePrice'][i]
        if(df['CE'][i]==0):
            calloi = callcoi =0
        else:
            calloi = float(df['CE'][i]['openInterest'])
            callcoi = float(df['CE'][i]['changeinOpenInterest'])
            cltp    = float(df['CE'][i]['lastPrice'])
            ctotaltradevaluem  =float(df['CE'][i]['totalTradedVolume'])
            ctotalBellq = float(df['CE'][i]['totalBuyQuantity'])
            ctotalSellq = float(df['CE'][i]['totalSellQuantity'])
            cbidQty = float(df['CE'][i]['bidQty'])
            cbidprice = float(df['CE'][i]['bidprice'])
            caskQty = float(df['CE'][i]['askQty'])
            caskPrice = float(df['CE'][i]['askPrice'])
            CALL_iv = float(df['CE'][i]['impliedVolatility'])
            # cstp = float(df['CE'][i]['strikePrice'])
        if(df['PE'][i]==0):
            putoi = putcoi = 0
        else:
            putoi = float(df['PE'][i]['openInterest'])
            putcoi = float(df['PE'][i]['changeinOpenInterest'])
            pltp    = float(df['PE'][i]['lastPrice'])
            ptotaltradevaluem  = float(df['PE'][i]['totalTradedVolume'])
            ptotalBellq = float(df['PE'][i]['totalBuyQuantity'])
            ptotalSellq = float(df['PE'][i]['totalSellQuantity'])
            pbidQty = float(df['PE'][i]['bidQty'])
            pbidprice = float(df['PE'][i]['bidprice'])
            paskQty = float(df['PE'][i]['askQty'])
            paskPrice = float(df['PE'][i]['askPrice'])
            PUT_iv = float(df['PE'][i]['impliedVolatility'])
            pstp = float(df['PE'][i]['underlyingValue'])


        opdata = {
            'CALL_TTV':ctotaltradevaluem,'C_BID_Q': cbidQty,'C_BID_P' :cbidprice,'C_ASK_Q' :caskQty,'C_ASK_P' : caskPrice,
            'CALL_OI' : calloi,'CALL_CHNG_OI':callcoi,'total_call_OI':calloi+callcoi,'CALL_IV' : CALL_iv ,
            'CALL_BQ':ctotalBellq,'CALL_SA':ctotalSellq,'spread_call':caskQty-cbidprice,'STRICK_PRICE':stp,'PUT_TTV':ptotaltradevaluem
            ,'P_BID_Q': pbidQty,'P_BID_P' :pbidprice,'P_ASK_Q' :paskQty,'P_ASK_P' : paskPrice,'PUT_IV' : PUT_iv ,
            'PUT_SA':ptotalSellq,'PUT_BQ':ptotalBellq,'PUT_CHNG_OI':putcoi,'PUT_OI' : putoi,'total_put_OI':putcoi+putoi,'spread_put':paskQty-pbidprice,'current_stp':pstp}
        data.append(opdata)
    optionchain = pd.DataFrame(data)
    #optionchain =optionchain.append(optionchain[['CALL_OI','CALL_CHNG_OI','PUT_OI','PUT_CHNG_OI','CALL_TTV','PUT_TTV','CALL_BQ','PUT_BQ','CALL_SA','PUT_SA']].sum(),ignore_index=True).fillna(0)
    return optionchain

def main():
    # cookie = request.cookies
    # responce = session.get(url,headers=header,cookies=cookie).json()
    # raw_data = responce['filtered']
    request = session.get(url,headers=header).json()['filtered']['data']
    request_index = session.get(url,headers=header).json()['records']['index']
    # df1 = pd.DataFrame(raw_data['data']).fillna(0)
    df1 = pd.DataFrame(request).fillna(0)
    option_df = dataframe(df1)
    opdata = {
            'CALL_OI'  : float(option_df['CALL_OI'].sum()),
            'PUT_OI'   : float(option_df['PUT_OI'].sum()),
            'CALL_COI' : float(option_df['CALL_CHNG_OI'].sum()),
            'PUT_COI'  : float(option_df['PUT_CHNG_OI'].sum()),
            'CALL_VOL' : float(option_df['CALL_TTV'].sum()),
            'PUT_VOL'  : float(option_df['PUT_TTV'].sum()),
            'CALL_TBQ' : float(option_df['CALL_BQ'].sum()),
            'CALL_TSQ' : float(option_df['CALL_SA'].sum()),
            'PUT_TBQ'  : float(option_df['PUT_BQ'].sum()),
            'PUT_TSQ'  : float(option_df['PUT_SA'].sum()),
            # 'OI_RATIO'  : float(option_df['PUT_OI'].sum()/option_df['CALL_OI'].sum()),
            # 'COI_RATIO' : float(option_df['PUT_CHNG_OI'].sum()/option_df['CALL_CHNG_OI'].sum()),
            # 'VOL_DIFF' : float(option_df['CALL_TTV'].sum()/option_df['PUT_TTV'].sum()),
            'CALL_PER' : ((float(option_df['CALL_SA'].sum())+ float(option_df['CALL_BQ'].sum()))/ (float(option_df['CALL_BQ'].sum()) * float(option_df['CALL_SA'].sum()))) * 100 ,
            'PUT_PER' : ((float(option_df['PUT_SA'].sum()) + float(option_df['PUT_BQ'].sum())) / (float(option_df['PUT_BQ'].sum()) * float(option_df['PUT_SA'].sum()))) * 100 ,
            'BUY_DIFF': float((option_df['PUT_SA'].sum()+option_df['CALL_BQ'].sum())/(option_df['CALL_SA'].sum()+option_df['PUT_BQ'].sum())),
            'SELL_DIFF': float((option_df['CALL_SA'].sum()+option_df['PUT_BQ'].sum())/(option_df['PUT_SA'].sum()+option_df['CALL_BQ'].sum())),
            # 'CALL_OI_RATIO' : float(option_df['CALL_OI'].sum()/option_df['CALL_CHNG_OI'].sum()),
            # 'PUT_OI_RATIO' : float(option_df['PUT_OI'].sum()/option_df['PUT_CHNG_OI'].sum()),
                                   }
    #print(opdata)
    return opdata,option_df,request_index

def max_values(x,option_df,n):
    return   (sqldf('''SELECT {x}  \
                            FROM \
                                    (SELECT STRICK_PRICE  , {x},row_number()OVER (PARTITION BY STRICK_PRICE order by {x} DESC)\
                                    AS rownumber FROM option_df)\
                        WHERE rownumber = 1 order by {x} DESC LIMIT 5'''.format(x=x)).values)[n]


def reurn_max(x,option_df,n):

    return   (sqldf('''SELECT STRICK_PRICE  \
                            FROM \
                                    (SELECT STRICK_PRICE  , {x},row_number()OVER (PARTITION BY STRICK_PRICE order by {x} DESC)\
                                    AS rownumber FROM option_df)\
                        WHERE rownumber = 1 order by {x} DESC LIMIT 5'''.format(x=x)).values)[n]


def max_dict(option_df):
    max_dic = {
                'max_CS'   : [
                    reurn_max('CALL_SA',option_df,0)[0],
                    reurn_max('CALL_SA',option_df,1)[0],
                    reurn_max('CALL_SA',option_df,2)[0]
                ],
                'max_CB'   : [
                    reurn_max('CALL_BQ',option_df,0)[0],
                    reurn_max('CALL_BQ',option_df,1)[0],
                    reurn_max('CALL_BQ',option_df,2)[0]
                ],
                # 'max_CBIDQ'   : [
                #     reurn_max('C_BID_Q',option_df,0)[0],
                #     reurn_max('C_BID_Q',option_df,1)[0],
                #     reurn_max('C_BID_Q',option_df,2)[0]
                # ],
                # 'max_CBIDp'   : [
                #     reurn_max('C_BID_P',option_df,0)[0],
                #     reurn_max('C_BID_P',option_df,1)[0],
                #     reurn_max('C_BID_P',option_df,2)[0]
                # ],
                #  'max_CASKQ'   : [
                #     reurn_max('C_ASK_Q',option_df,0)[0],
                #     reurn_max('C_ASK_Q',option_df,1)[0],
                #     reurn_max('C_ASK_Q',option_df,2)[0]
                # ],
                # 'max_CASKP'   : [
                #     reurn_max('C_ASK_P',option_df,0)[0],
                #     reurn_max('C_ASK_P',option_df,1)[0],
                #     reurn_max('C_ASK_P',option_df,2)[0]
                # ],
                'max_CT'   : [
                    reurn_max('CALL_TTV',option_df,0)[0],
                    reurn_max('CALL_TTV',option_df,1)[0],
                    reurn_max('CALL_TTV',option_df,2)[0]
                ],
                 'max_CTOI'   : [
                    reurn_max('total_call_OI',option_df,0)[0],
                    reurn_max('total_call_OI',option_df,1)[0],
                    reurn_max('total_call_OI',option_df,2)[0]
                ],
                'max_COI'  : [
                    reurn_max('CALL_OI',option_df,0)[0],
                    reurn_max('CALL_OI',option_df,1)[0],
                    reurn_max('CALL_OI',option_df,2)[0]
                ],
                'max_CCOI' : [
                    reurn_max('CALL_CHNG_OI',option_df,0)[0],
                    reurn_max('CALL_CHNG_OI',option_df,1)[0],
                    reurn_max('CALL_CHNG_OI',option_df,2)[0]
                ],
                'STP'      : [int(option_df['current_stp'][0]),int(option_df['current_stp'][0]),int(option_df['current_stp'][0])],

                'max_PCOI' : [
                    reurn_max('PUT_CHNG_OI',option_df,0)[0],
                    reurn_max('PUT_CHNG_OI',option_df,1)[0],
                    reurn_max('PUT_CHNG_OI',option_df,2)[0]
                ],
                'max_POI'  : [
                    reurn_max('PUT_OI',option_df,0)[0],
                    reurn_max('PUT_OI',option_df,1)[0],
                    reurn_max('PUT_OI',option_df,2)[0]
                ],
                'max_PTOI'   : [
                    reurn_max('total_put_OI',option_df,0)[0],
                    reurn_max('total_put_OI',option_df,1)[0],
                    reurn_max('total_put_OI',option_df,2)[0]
                ],
                'max_PT'   : [
                    reurn_max('PUT_TTV',option_df,0)[0],
                    reurn_max('PUT_TTV',option_df,1)[0],
                    reurn_max('PUT_TTV',option_df,2)[0]
                ],
                # 'max_PBIDQ'   : [
                #     reurn_max('P_BID_Q',option_df,0)[0],
                #     reurn_max('P_BID_Q',option_df,1)[0],
                #     reurn_max('P_BID_Q',option_df,2)[0]
                # ],
                # 'max_PBIDp'   : [
                #     reurn_max('P_BID_P',option_df,0)[0],
                #     reurn_max('P_BID_P',option_df,1)[0],
                #     reurn_max('P_BID_P',option_df,2)[0]
                # ],
                #  'max_PASKQ'   : [
                #     reurn_max('P_ASK_Q',option_df,0)[0],
                #     reurn_max('P_ASK_Q',option_df,1)[0],
                #     reurn_max('P_ASK_Q',option_df,2)[0]
                # ],
                # 'max_PASKP'   : [
                #     reurn_max('C_ASK_P',option_df,0)[0],
                #     reurn_max('C_ASK_P',option_df,1)[0],
                #     reurn_max('C_ASK_P',option_df,2)[0]
                # ],
                'max_PB'   : [
                    reurn_max('PUT_BQ',option_df,0)[0],
                    reurn_max('PUT_BQ',option_df,1)[0],
                    reurn_max('PUT_BQ',option_df,2)[0]
                ],
                'max_PS'   : [
                    reurn_max('PUT_SA',option_df,0)[0],
                    reurn_max('PUT_SA',option_df,1)[0],
                    reurn_max('PUT_SA',option_df,2)[0]
                ]
              }
    return max_dic

def max_dict_vlues(option_df):
    max_dic = {
                'max_CS'   : [
                    max_values('CALL_SA',option_df,0)[0],
                    max_values('CALL_SA',option_df,1)[0],
                    max_values('CALL_SA',option_df,2)[0]
                ],
                'max_CB'   : [
                    max_values('CALL_BQ',option_df,0)[0],
                    max_values('CALL_BQ',option_df,1)[0],
                    max_values('CALL_BQ',option_df,2)[0]
                ],
                # 'max_CBIDQ'   : [
                #     max_values('C_BID_Q',option_df,0)[0],
                #     max_values('C_BID_Q',option_df,1)[0],
                #     max_values('C_BID_Q',option_df,2)[0]
                # ],
                # 'max_CBIDp'   : [
                #     max_values('C_BID_P',option_df,0)[0],
                #     max_values('C_BID_P',option_df,1)[0],
                #     max_values('C_BID_P',option_df,2)[0]
                # ],
                #  'max_CASKQ'   : [
                #     max_values('C_ASK_Q',option_df,0)[0],
                #     max_values('C_ASK_Q',option_df,1)[0],
                #     max_values('C_ASK_Q',option_df,2)[0]
                # ],
                # 'max_CASKP'   : [
                #     max_values('C_ASK_P',option_df,0)[0],
                #     max_values('C_ASK_P',option_df,1)[0],
                #     max_values('C_ASK_P',option_df,2)[0]
                # ],
                'max_CT'   : [
                    max_values('CALL_TTV',option_df,0)[0],
                    max_values('CALL_TTV',option_df,1)[0],
                    max_values('CALL_TTV',option_df,2)[0]
                ],
                 'max_CTOI'   : [
                    max_values('total_call_OI',option_df,0)[0],
                    max_values('total_call_OI',option_df,1)[0],
                    max_values('total_call_OI',option_df,2)[0]
                ],
                'max_COI'  : [
                    max_values('CALL_OI',option_df,0)[0],
                    max_values('CALL_OI',option_df,1)[0],
                    max_values('CALL_OI',option_df,2)[0]
                ],
                'max_CCOI' : [
                    max_values('CALL_CHNG_OI',option_df,0)[0],
                    max_values('CALL_CHNG_OI',option_df,1)[0],
                    max_values('CALL_CHNG_OI',option_df,2)[0]
                ],
                'STP'      : [int(option_df['current_stp'][0]),int(option_df['current_stp'][0]),int(option_df['current_stp'][0])],

                'max_PCOI' : [
                    max_values('PUT_CHNG_OI',option_df,0)[0],
                    max_values('PUT_CHNG_OI',option_df,1)[0],
                    max_values('PUT_CHNG_OI',option_df,2)[0]
                ],
                'max_POI'  : [
                    max_values('PUT_OI',option_df,0)[0],
                    max_values('PUT_OI',option_df,1)[0],
                    max_values('PUT_OI',option_df,2)[0]
                ],
                'max_PTOI'   : [
                    max_values('total_put_OI',option_df,0)[0],
                    max_values('total_put_OI',option_df,1)[0],
                    max_values('total_put_OI',option_df,2)[0]
                ],
                'max_PT'   : [
                    max_values('PUT_TTV',option_df,0)[0],
                    max_values('PUT_TTV',option_df,1)[0],
                    max_values('PUT_TTV',option_df,2)[0]
                ],
                # 'max_PBIDQ'   : [
                #     max_values('P_BID_Q',option_df,0)[0],
                #     max_values('P_BID_Q',option_df,1)[0],
                #     max_values('P_BID_Q',option_df,2)[0]
                # ],
                # # 'max_PBIDp'   : [
                #     max_values('P_BID_P',option_df,0)[0],
                #     max_values('P_BID_P',option_df,1)[0],
                #     max_values('P_BID_P',option_df,2)[0]
                # ],
                #  'max_PASKQ'   : [
                #     max_values('P_ASK_Q',option_df,0)[0],
                #     max_values('P_ASK_Q',option_df,1)[0],
                #     max_values('P_ASK_Q',option_df,2)[0]
                # ],
                # 'max_PASKP'   : [
                #     max_values('C_ASK_P',option_df,0)[0],
                #     max_values('C_ASK_P',option_df,1)[0],
                #     max_values('C_ASK_P',option_df,2)[0]
                # ],
                'max_PB'   : [
                    max_values('PUT_BQ',option_df,0)[0],
                    max_values('PUT_BQ',option_df,1)[0],
                    max_values('PUT_BQ',option_df,2)[0]
                ],
                'max_PS'   : [
                    max_values('PUT_SA',option_df,0)[0],
                    max_values('PUT_SA',option_df,1)[0],
                    max_values('PUT_SA',option_df,2)[0]
                ]
              }
    return max_dic

def analyze_trading_signals(df):
    results = []
    
    # Define thresholds for generating signals
    buy_diff_threshold = 1.5  # If BUY_DIFF is greater than this, consider buying calls
    sell_diff_threshold = 0.5  # If SELL_DIFF is less than this, consider buying puts
    oi_increase_threshold = 0  # Minimum threshold for an increase in OI (Open Interest)
    volume_threshold = 1e7  # Minimum volume to validate the signal

    for index, row in df.iterrows():
        # Extract data for each row
        call_oi = row['CALL_OI']
        put_oi = row['PUT_OI']
        call_coi = row['CALL_COI']
        put_coi = row['PUT_COI']
        call_vol = row['CALL_VOL']
        put_vol = row['PUT_VOL']
        call_tbq = row['CALL_TBQ']
        call_tsq = row['CALL_TSQ']
        put_tbq = row['PUT_TBQ']
        put_tsq = row['PUT_TSQ']
        call_per = row['CALL_PER']
        put_per = row['PUT_PER']
        buy_diff = row['BUY_DIFF']
        sell_diff = row['SELL_DIFF']
    

        # Calculate buyer and seller ratios
        total_call = call_tbq + call_tsq
        total_put = put_tbq + put_tsq
        
        call_buyer_ratio = (call_tbq / total_call) if total_call != 0 else 0
        put_buyer_ratio = (put_tbq / total_put) if total_put != 0 else 0
        call_seller_ratio = (call_tsq / total_call) if total_call != 0 else 0
        put_seller_ratio = (put_tsq / total_put) if total_put != 0 else 0

        # Initialize default action
        action = 'No Action'
        
        # Determine if there is a "Buy Call" signal
        if (
        put_seller_ratio > call_seller_ratio and 
            call_vol > volume_threshold and
            call_buyer_ratio > put_buyer_ratio):  # Adjust the ratio threshold as needed
            action = 'Buy Call'
        
        # Determine if there is a "Buy Put" signal
        elif (
        call_seller_ratio > put_seller_ratio and 
              put_vol > volume_threshold and
              put_buyer_ratio > call_buyer_ratio):  # Adjust the ratio threshold as needed
            action = 'Buy Put'
        
        # Compile the result for this row
        results.append({
            'Action': action,
            'CALL_OI': call_oi,
            'PUT_OI': put_oi,
            'CALL_COI': call_coi,
            'PUT_COI': put_coi,
            'CALL_VOL': call_vol,
            'PUT_VOL': put_vol,
            'CALL_TBQ': call_tbq,
            'CALL_TSQ': call_tsq,
            'PUT_TBQ': put_tbq,
            'PUT_TSQ': put_tsq,
            # 'CALL_PER': call_per,
            # 'PUT_PER': put_per,
            'BUY_DIFF': buy_diff,
            'SELL_DIFF': sell_diff,
            'Call_BR': call_buyer_ratio,
            'Put_BR': put_buyer_ratio,
            'Call_SR': call_seller_ratio,
            'Put_SR': put_seller_ratio
        })
    
    return pd.DataFrame(results)

# Example usage:
# Assuming you have a DataFrame `df` with the necessary columns
# df = pd.DataFrame(your_data)
# signals_df = analyze_trading_signals(df)
# print(signals_df)


def analyze_options_with_buyers_sellers(df):
    results = []
    
    # Parameters for sell price and stoploss (as percentage changes)
    sell_percentage = 1.10  # Sell when price increases by 10%
    stoploss_percentage = 0.95  # Stoploss when price decreases by 5%
    
    for index, row in df.iterrows():
        # Extract all relevant columns
        call_iv = row['CALL_IV']
        put_iv = row['PUT_IV']
        call_oi = row['CALL_OI']
        put_oi = row['PUT_OI']
        call_change_oi = row['CALL_CHNG_OI']
        put_change_oi = row['PUT_CHNG_OI']
        current_price = row['current_stp']
        strike_price = row['STRICK_PRICE']
        call_bid = row['C_BID_P']
        call_ask = row['C_ASK_P']
        put_bid = row['P_BID_P']
        put_ask = row['P_ASK_P']
        spread_call = row['spread_call']
        spread_put = row['spread_put']
        call_buyers = row["CALL_BQ"]
        call_sellers = row["CALL_SA"]
        put_buyers = row["PUT_BQ"]
        put_sellers = row["PUT_SA"]

        # Calculate the Put-Call Ratio
        put_call_ratio = put_oi / call_oi if call_oi != 0 else float('inf')

        # Calculate buyer and seller ratios
        total_call = call_buyers + call_sellers
        total_put = put_buyers + put_sellers
        
        call_buyer_ratio = (call_buyers / total_call) if total_call != 0 else 0
        put_buyer_ratio = (put_buyers / total_put) if total_put != 0 else 0
        call_seller_ratio = (call_sellers / total_call) if total_call != 0 else 0
        put_seller_ratio = (put_sellers / total_put) if total_put != 0 else 0

        # Determine action, price to buy, sell price, and stoploss
        if put_oi > call_oi and put_change_oi>call_change_oi and call_buyer_ratio > put_buyer_ratio and put_seller_ratio > call_seller_ratio:
            action = 'Buy Call'
            price_to_buy = call_ask
            sell_price = price_to_buy * sell_percentage
            stoploss = price_to_buy * stoploss_percentage
        elif put_oi < call_oi and put_change_oi < call_change_oi and call_buyer_ratio < put_buyer_ratio and put_seller_ratio < call_seller_ratio:
            action = 'Buy Put'
            price_to_buy = put_ask
            sell_price = price_to_buy * sell_percentage
            stoploss = price_to_buy * stoploss_percentage
        else:
            action = 'No Action'
            price_to_buy = None
            sell_price = None
            stoploss = None

        # Compile the results for each row of data
        results.append({
            'Action': action,
            'PTB': price_to_buy,
            'Sell Price': sell_price,
            'Stoploss': stoploss,
            'Call_IV': call_iv,
            'Call_OI': call_oi,
            'Call_COI': call_change_oi,
            'Call_BQ': call_buyers,
            'Call_SQ': call_sellers,
            'Current Price': current_price,
            'STP': strike_price,
            'Put_SQ': put_sellers,
            'Put_BQ': put_buyers,
            'Put_COI': put_change_oi,
            'Put_OI': put_oi,
            'Put_IV': put_iv,
            'Put-Call Ratio': put_call_ratio
        })
    
    return pd.DataFrame(results)

def run_main(option_dataframe,max_df,max_df_2,request_index):
    while True:
        clear_output(wait=True)
        option_dataframe,option_df,request_index=option_dataframe._append(main()[0],ignore_index=True),main()[1],request_index._append(main()[2],ignore_index=True)
        option_dataframe.drop_duplicates(inplace = True)
        analysis_results = analyze_options_with_buyers_sellers(option_df)
        dis_option_dataframe = analyze_trading_signals(option_dataframe)
        price = int(option_df['current_stp'][0])
        max_dic = max_dict(option_df)
        max_dic_2= max_dict_vlues(option_df)
        range_price = list(range(round(price/100)*100-500,round(price/100)*100+500,100))
        max_dic = max_dict(option_df)
        max_dic_2= max_dict_vlues(option_df)
        max_df = max_df._append(pd.DataFrame(max_dic))
        max_df_2 = max_df_2._append(pd.DataFrame(max_dic_2))
        option_df['index_trading'] =  price
        display_df = option_df[['CALL_IV','spread_call','CALL_OI','CALL_CHNG_OI','CALL_BQ','CALL_SA','STRICK_PRICE',
                                'PUT_SA','PUT_BQ','PUT_CHNG_OI','PUT_OI','spread_put','PUT_IV']]
        # option_dataframe = generate_signals(option_dataframe)
        clear_output(wait=True)
        # display(dis_option_dataframe.tail(5))
        # display(max_df.tail(3)
        # ,max_df_2.tail(3)
        # ,analysis_results[(analysis_results.STP.isin(range_price))]
        # ,display_df[(display_df.STRICK_PRICE.isin(range_price))]
                # )
        # display(request_index.tail(3))
        # time.sleep(2)
    return dis_option_dataframe.tail(5),max_df.tail(3),analysis_results[(analysis_results.STP.isin(range_price))],request_index.tail(3)



# Show the page title and description.
st.set_page_config(page_title="BANKNIFT dataset")
st.title(" banknifty  dataset")
st.write(
    """
    This app visualizes data from [The NSE (BN)](https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY).
    It shows data of today !
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
dis_option_dataframe = run_main(option_dataframe,max_df,max_df_2,request_index)[0]
max_df = run_main(option_dataframe,max_df,max_df_2,request_index)[1]
analysis_results = run_main(option_dataframe,max_df,max_df_2,request_index)[2]

# Display the data as a table using `st.dataframe`.
st.dataframe(
    dis_option_dataframe,
    use_container_width=True,hide_index=True
)

