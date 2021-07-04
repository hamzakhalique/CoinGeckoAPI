# import libraries
import numpy as np
import pandas as pd

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# define CoinGeckoAPI class
class CoinGeckoAPI():
    ''' Class to retrieve cryptocurrency data from CoinGeckoAPI 
    
    Attributes
    ==========
    coin: str
        id of coin (default is set to bitcoin)
    
    Methods
    ==========
    get_data:
        retrieves daily prices, log returns, market caps and total volume data and transforms to pandas dataframe
        
        to get pandas dataframe, use .data after initialization
            ex. CoinGeckoAPI().data
            
    get_top_100:
        retrieves id of top 100 cryptocurrencies on CoinGecko, organized by largest market cap (rank) in a pandas dataframe
        
        top 100 coins can be found using get_top_100 method on CoinGeckoAPI class
            ex. CoinGeckoAPI().get_top_100()
            
    get_coin_id:
        retrieves coin id for all cryptocurrencies listed on CoinGecko in a pandas dataframe
        
        default is set to bitcoin. can be changed by passing id of coin you want as a str
        
        all coin ids can be found using get_coin_id method on CoinGeckoAPI class
            ex. CoinGeckoAPI().get_coin_id()
            
        to search for a specific coin id, chain loc operator and pass ticker symbol in lowercase letters
            ex. CoinGecko().get_coin_id().loc["eth"] 
                the output (ethereum) can be passed as a str as follows to retrieve data of coin
                    CoinGeckoAPI("ethereum").data
        
        *if you know the name of the coin but not the ticker, the ticker can be found from the CoinGecko website
    
        
            
            

    '''
    
    def __init__(self, coin="bitcoin"):
        self._coin = coin
        self.top_100 = None
        self.coin_id = None
        
        self.get_data()  
    
    def __repr__(self):
        return "CoinGeckoAPI(coin = {})".format(self._coin)
        
    def get_data(self):
        ''' retrieves daily prices, log returns, market caps and total volume data and transforms to pandas dataframe
        '''
        data = cg.get_coin_market_chart_by_id(id=self._coin,vs_currency='usd',days='10000')
        data = pd.DataFrame(data)
        
        dates = []
        for i, j in data.prices:
            dates.append(i)
    
        prices = []
        for i, j in data.prices:
            prices.append(j)
    
        market_caps = []
        for i, j in data.market_caps:
            market_caps.append(j)
    
        total_volumes = []
        for i, j in data.total_volumes:
            total_volumes.append(j)
    
        data["date"] = pd.DataFrame(dates)
        data["price"] = pd.DataFrame(prices)
        data["log_returns"] = np.log(data.price / data.price.shift(1))
        data["market_cap"] = pd.DataFrame(market_caps)
        data["total_volume"] = pd.DataFrame(total_volumes)
        data["date"] = (pd.to_datetime(data["date"],unit='ms'))
        data = data.drop(columns=["prices", "market_caps", "total_volumes"], axis=1)
        data = data.set_index(data.date)
        data = data.drop(columns="date", axis=1)

        pd.set_option("display.float_format", lambda x: "%.3f" % x)
    
        self.data = data
        
    def get_top_100(self):
        ''' retrieves rank and id of the top 100 cryptocurrencies on CoinGecko, organized by market cap
        '''
        top_100 = pd.DataFrame(cg.get_coins_markets(vs_currency="usd"))
        top_100 = top_100.id, top_100.market_cap_rank
        top_100 = pd.DataFrame(top_100).T.set_index(keys="market_cap_rank")
        return top_100
        self.top_100 = top_100
    
    def get_coin_id(self):
        ''' retrieves coin id for all cryptocurrencies listed on CoinGecko 
        '''
        coin_id = pd.DataFrame(cg.get_coins_list())
        coin_id = coin_id.id, coin_id.symbol
        coin_id = pd.DataFrame(coin_id).T.set_index(keys='symbol')
        return coin_id
        self.coin_id = coin_id

