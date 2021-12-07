# import libraries
import numpy as np, pandas as pd
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

    def get_mkt_data(self):
        """ retrieves market data about the coin
        """
        mkt_data_df = pd.DataFrame(cg.get_coin_markets(vs_currency='usd'))
        mkt_data_df = mkt_data_df.drop(columns=['name','image','roi','last_updated'], axis=1)
        return mkt_data_df[mkt_data_df['id'] == self._coin]

# coin list for program
def coin_list():
    # turn the coin dataframe into strings
    global all_coins_list
    all_coins_list = []
    
    for i in CoinGeckoAPI().get_coin_id().values.tolist():
        for j in i:
            all_coins_list.append(j)
    return all_coins_list        
coin_list()

# delay print 
import time

def delay_print(s, t):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(t)

# test development 

import sys
import pyinputplus as pyip

def launch_program():
    
    global coin_choice
    
    while True:
        response = pyip.inputYesNo(prompt="Do you know which coin you're looking for? (yes/no): \n")
        
        if response == "yes".lower() or response == "y".lower():
                
                coin_choice = input("Enter your coin here: \n")
                if coin_choice in all_coins_list:
                    
                    data = CoinGeckoAPI(coin=coin_choice).data
                    print("Here is a snippet of the data for %s: \n" % (coin_choice))
                    return data
                else:
                    print("Error: Sorry, I couldn't find that coin in our list. Please verify and try again. \n")
                    continue
                    
        elif response == "no".lower() or response == "n".lower():    
                
                # ask the user if they know the first letter of the coin they are looking for
                
                while True:
                    char = input("What is the first character(s) of the coin you're looking for: \n")
                    if char.isalnum() == False:
                        print("Oops. I think you entered a special character. Please only enter letters or numbers. \n")
                    elif char.isalnum() == True:
                        
                        print("*All coins in the coingecko database that start with " + "'" + char + "'" + ": \n")
                        print("CoinGeckoAPI".center(50,"="))
                            
                        # iterates through the list to find all coins that start with the user's character
                        for i in all_coins_list:
                            if i.startswith(char):
                                print(i)
                                print("".center(50, "-"))
                        print("".center(50,"="))
                        print("*Note if you see an empty space, then the coin does not exist in the coingecko database. \n")
                        

                    question = pyip.inputYesNo(prompt="Do you see what you're looking for (yes/no)?: \n")
                    if question == "yes".lower() or question == "y".lower():
                        break
                    elif question == "no".lower() or question == "n".lower():
                        response = pyip.inputYesNo(prompt="Sorry about that. Did you want to look for another coin? (yes/no): \n")
                        if response == "yes".lower() or question == "y".lower():
                            continue
                        elif response == "no".lower() or response == "n".lower():
                            delay_print("No problem. Have a great day! \n", 0.0325)
                            sys.exit()

                # now, the user will input the name to get the data of the coin they were searching for
                response = input("Please enter the name of your coin here: \n")
                if response not in all_coins_list:
                    print("Error: Sorry, I couldn't find that coin in our list. Please verify and try again. \n")
                    continue
                    
                else:
                    coin_choice = response
                    print(f"Here is a snippet of the data for {coin_choice}: \n")
                    data = CoinGeckoAPI(coin=response).data
                    return data
                    break
                    
def slice_data(df):
    while True:
        print("The available data for " + coin_choice + " is from " + str(df.index[0])[0:10] + " to " + str(df.index[-1])[0:10] + ". \n")
        global timeframe_start
        timeframe_start = input("Where would you like your dataset to start? ('yyyy-mm-dd'): \n")
        if timeframe_start in df.index:
            break
        else:
            print("Sorry, you either inputted the date in the incorrect format or that timeframe isn't part of " + coin_choice + "'s dataset.\nPlease verify the start date and try again. \n")

    while True:
        global timeframe_end
        timeframe_end = input("Where would you like your dataset to end? ('yyyy-mm-dd'): \n")
        if timeframe_end in df.index:
            if (timeframe_end[0:4] > timeframe_start[0:4]) or (timeframe_end[0:4] == timeframe_start[0:4] and timeframe_end[5:7] == timeframe_start[5:7] and timeframe_end[8:] >= timeframe_start[8:]) or (timeframe_end[0:4] == timeframe_start[0:4] and timeframe_end[5:7] > timeframe_start[5:7]):
                break
            else:
                print("The end date you've entered is before the start date. Please try again. \n")
                 
        else:
            print("Sorry, you either inputted the date in the incorrect format or that timeframe isn't part of " + coin_choice + "'s dataset.\nPlease verify the end date and try again. \n")
    
    global df_slice
    df_slice = df.copy()
    df_slice = df.loc[(df.index >= timeframe_start)&(df.index <= timeframe_end)]
    print("Your sliced data has been saved in the variable df_slice. \n")
    return df_slice
    print(df_slice)                    

import matplotlib.pyplot as plt

def plot_data(x):
        
    choice = pyip.inputChoice(prompt="What plot would you like to visualize? (price, log returns, market cap, total volume)?: \n",
                         choices=["price", "log returns", "market cap", "total volume"])
    
    timeframe_start = str(df.index[0])[0:10]
    timeframe_end = str(df.index[-1])[0:10]
    
    ylabel = ""
    if choice == "price".lower():
        x = x.price
        ylabel = "price (usd)"
        title = f"{coin_choice}'s price (usd) ({timeframe_start} to {timeframe_end})"
        label = "price"
        
    elif choice == "log returns".lower():
        x = x.log_returns
        ylabel = "returns (%)"
        title = f"{coin_choice}'s log returns (%) ({timeframe_start} to {timeframe_end})"
        label = "log returns"
        
    elif choice == "market cap".lower():
        x = x.market_cap
        ylabel = "market cap (usd)"
        title = f"{coin_choice}'s market cap ({timeframe_start} to {timeframe_end})"
        label = "market cap"
        
    elif choice == "total volume".lower():
        x = x.total_volume
        ylabel = "total volume"
        title = f"{coin_choice}'s total volume ({timeframe_start} to {timeframe_end})"
        label = "total volume"
        
    plt.figure(figsize=(8, 5), dpi=80)
    plt.plot(x, label=label)

    plt.title(title, fontsize=13)
    plt.xlabel("Date", fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.legend(loc="upper left")
    
    plt.show()
    
def visualize_data():
    response = pyip.inputChoice(prompt="Would you like to visualize the entire dataset or the sliced dataset (entire dataset, sliced dataset): \n",
                               choices=["entire dataset", "sliced dataset"])
    if response == "entire dataset":

        plot_data(df)
    elif response == "sliced dataset":
        try:
            plot_data(df_slice)
        except NameError:
            response = pyip.inputYesNo("No sliced dataset exists. Would you like to create a sliced dataset to visualize (yes/no)?: \n")
            if response == "yes".lower() or response == "y".lower():
                slice_data(df)
                plot_data(df_slice)
            elif response == "no".lower() or response == "n".lower():
                response = pyip.inputYesNo("Would you like to visualize the entire dataset (yes/no)?: \n")
                if response == "yes".lower() or response == "y".lower():
                    plot_data(df)
                elif response == "no".lower() or response == "n".lower():
                    print("No problem. *Change this if necessary later.* \n")

def export_data(x):

    import pandas as pd

    date = []
    price = []
    log_returns = []
    market_cap = []
    total_volume = []

    # create dates
    for i in x.index:
        date.append(str(i)[0:10])

    for i in x.price:
        price.append(i)

    for i in x.log_returns:
        log_returns.append(i)

    for i in x.market_cap:
        market_cap.append(i)

    for i in x.total_volume:
        total_volume.append(i)

    export_dict = {
        "date": date,
        "price": price,
        "log returns": log_returns,
        "market cap": market_cap,
        "total volume": total_volume
    }

    export_df = pd.DataFrame(export_dict)
    return export_df                    
                                     
def csv_questions():
    response = pyip.inputChoice(prompt="For your CSV file(s), would you like to export the entire dataset, sliced dataset or both? (entire dataset, sliced dataset, both) \n",
                                    choices=["entire dataset", "sliced dataset", "both"])
    # export entire dataset
    if response == "entire dataset".lower():
        delay_print("What would you like to name your csv file (entire dataset): \n", 0.0325)
        csv_name_entire = input()
        delay_print("Okay. Please wait a moment as we export your data to csv format: \n",0.0325)
        export_df = export_data(df)
        print("Exporting to CSV".center(30,"="))
        time.sleep(1.5)
        export_df.to_csv(csv_name_entire+".csv", index=False)
        delay_print(f"Your data has been saved as: {csv_name_entire}.csv \n",0.0325)
    
    # export sliced dataset
    elif response == "sliced dataset".lower():
        delay_print("What would you like to name your csv file (sliced dataset): \n", 0.0325)
        csv_name_sliced = input()
        try:
            delay_print("Okay. Please wait a moment as we export your data to csv format: \n",0.0325)
            export_df_slice = export_data(df_slice)
            print("Exporting to CSV".center(30,"="))
            time.sleep(1.5)
            export_df_slice.to_csv(csv_name_sliced+".csv", index=False)
            delay_print(f"Your data has been saved as: {csv_name_sliced}.csv \n",0.0325)
        except NameError:
            response = pyip.inputYesNo("No sliced dataset exists. Would you like to create a sliced dataset to export (yes/no)?: \n")
            if response == "yes".lower() or response == "y".lower():
                slice_data(df)
                delay_print("Okay. Please wait a moment as we export your data to csv format: \n",0.0325)
                export_df_slice = export_data(df_slice)
                print("Exporting to CSV".center(30,"="))
                time.sleep(1.5)
                export_df_slice.to_csv(csv_name_sliced+".csv", index=False)
                delay_print(f"Your data has been saved as: {csv_name_sliced}.csv \n",0.0325)
            elif response == "no".lower() or response == "n".lower():
                response = pyip.inputYesNo("Would you like to export the entire dataset instead (yes/no)?: \n")
                if response == "yes".lower() or response == "y".lower():
                    delay_print("What would you like to name your csv file (entire dataset): \n", 0.0325)
                    csv_name_entire = input()
                    delay_print("Okay. Please wait a moment as we export your data to csv format: \n",0.0325)
                    export_df = export_data(df)
                    print("Exporting to CSV".center(30,"="))
                    time.sleep(1.5)
                    export_df.to_csv(csv_name_entire+".csv", index=False)
                    delay_print(f"Your data has been saved as: {csv_name_entire}.csv \n",0.0325)
                elif response == "no".lower() or response == "n".lower():
                    print("No problem. Change this if necessary later. \n")
    
    # export both the entire dataset and sliced dataset
    elif response == "both".lower():
        
        # saving the entire dataset
        delay_print("What would you like to name your csv file (entire dataset): \n", 0.0325)
        csv_name_entire = input()
        delay_print("Okay. Please wait a moment as we export your data to csv format: \n",0.0325)
        export_df = export_data(df)
        print("Exporting to CSV".center(30,"="))
        time.sleep(1.5)
        export_df.to_csv(csv_name_entire+".csv", index=False)
        delay_print(f"Your data has been saved as: {csv_name_entire}.csv \n",0.0325)
        
        # saving the sliced dataset
        delay_print("What would you like to name your csv file (sliced dataset): \n", 0.0325)
        csv_name_sliced = input()
        try:
            delay_print("Okay. Please wait a moment as we export your data to csv format: \n",0.0325)
            export_df_slice = export_data(df_slice)
            print("Exporting to CSV".center(30,"="))
            export_df_slice.to_csv(csv_name_sliced+".csv", index=False)
            time.sleep(1.5)
            delay_print(f"Your data has been saved as: {csv_name_sliced}.csv \n",0.0325)
        except NameError:
            response = pyip.inputYesNo("No sliced dataset exists. Would you like to create a sliced dataset to export (yes/no)?: \n")
            if response == "yes".lower() or response == "y".lower():
                slice_data(df)
                delay_print("Okay. Please wait a moment as we export your data to csv format: \n",0.0325)
                export_df_slice = export_data(df_slice)
                print("Exporting to CSV".center(30,"="))
                time.sleep(1.5)
                export_df_slice.to_csv(csv_name_sliced+".csv", index=False)
                delay_print(f"Your data has been saved as: {csv_name_sliced}.csv \n",0.0325)
            elif response == "no".lower() or response == "n".lower():
                response = pyip.inputYesNo("Would you like to export the entire dataset instead (yes/no)?: \n")
                if response == "yes".lower() or response == "y".lower():
                    delay_print("What would you like to name your csv file (entire dataset): \n", 0.0325)
                    csv_name_entire = input()
                    delay_print("Okay. Please wait a moment as we export your data to csv format: \n",0.0325)
                    export_df = export_data(df)
                    print("Exporting to CSV".center(30,"="))
                    time.sleep(1.5)
                    export_df.to_csv(csv_name_entire+".csv", index=False)
                    delay_print(f"Your data has been saved as: {csv_name_entire}.csv \n",0.0325)
                elif response == "no".lower() or response == "n".lower():
                    print("No problem. Change this if necessary later. \n")

def xlsx_questions():
    response = pyip.inputChoice(prompt="For your xlsx file(s), would you like to export the entire dataset, sliced dataset or both? (entire dataset, sliced dataset, both) \n",
                                    choices=["entire dataset", "sliced dataset", "both"])
    # export entire dataset
    if response == "entire dataset".lower():
        delay_print("What would you like to name your xlsx file (entire dataset): \n", 0.0325)
        xlsx_name_entire = input()
        delay_print("Okay. Please wait a moment as we export your data to xlsx format: \n",0.0325)
        export_df = export_data(df)
        print("Exporting to XLSX".center(30,"="))
        time.sleep(1.5)
        export_df.to_excel(xlsx_name_entire+".xlsx", index=False)
        # remember to change it so the name is show: your data has been saved to 'filename.xlxs'
        delay_print(f"Your data has been saved as: {xlsx_name_entire}.xlsx \n",0.0325)
    
    # export sliced dataset
    elif response == "sliced dataset".lower():
        delay_print("What would you like to name your xlsx file (sliced dataset): \n",0.0325)
        xlsx_name_sliced = input()
        try:
            delay_print("Okay. Please wait a moment as we export your data to xlsx format: \n",0.0325)
            export_df_slice = export_data(df_slice)
            print("Exporting to XLSX".center(30,"="))
            time.sleep(1.5)
            export_df_slice.to_excel(xlsx_name_sliced+".xlsx", index=False)
            delay_print(f"Your data has been saved as: {xlsx_name_sliced}.xlsx \n",0.0325)
        except NameError:
            response = pyip.inputYesNo("No sliced dataset exists. Would you like to create a sliced dataset to export (yes/no)?: \n")
            if response == "yes".lower() or response == "y".lower():
                slice_data(df)
                delay_print("Okay. Please wait a moment as we export your data to xlsx format: \n",0.0325)
                export_df_slice = export_data(df_slice)
                print("Exporting to XLSX".center(30,"="))
                time.sleep(1.5)
                export_df_slice.to_excel(xlsx_name_sliced+".xlsx", index=False)
                delay_print(f"Your data has been saved as: {xlsx_name_sliced}.xlsx \n",0.0325)
            elif response == "no".lower() or response == "n".lower():
                response = pyip.inputYesNo("Would you like to export the entire dataset instead (yes/no)?: \n")
                if response == "yes".lower() or response == "y".lower():
                    delay_print("What would you like to name your xlsx file (entire dataset): \n", 0.0325)
                    xlsx_name_entire = input()
                    delay_print("Okay. Please wait a moment as we export your data to xlsx format: \n",0.0325)
                    export_df = export_data(df)
                    print("Exporting to XLSX".center(30,"="))
                    time.sleep(1.5)
                    export_df.to_excel(xlsx_name_entire+".xlsx", index=False)
                    # remember to change it so the name is show: your data has been saved to 'filename.xlxs'
                    delay_print(f"Your data has been saved as: {xlsx_name_entire}.xlsx \n",0.0325)
                elif response == "no".lower() or response == "n".lower():
                    print("No problem. Change this if necessary later. \n")
    
    # export both the entire dataset and sliced dataset
    elif response == "both".lower():
        
        # saving the entire dataset
        delay_print("What would you like to name your xlsx file (entire dataset): \n", 0.0325)
        xlsx_name_entire = input()
        delay_print("Okay. Please wait a moment as we export your data to xlsx format: \n",0.0325)
        export_df = export_data(df)
        print("Exporting to XLSX".center(30,"="))
        time.sleep(1.5)
        export_df.to_excel(xlsx_name_entire+".xlsx", index=False)
        # remember to change it so the name is show: your data has been saved to 'filename.xlxs'
        delay_print(f"Your data has been saved as: {xlsx_name_entire}.xlsx \n",0.0325)
        
        # saving the sliced dataset
        delay_print("What would you like to name your xlsx file (sliced dataset): \n",0.0325)
        xlsx_name_sliced = input()
        try:
            delay_print("Okay. Please wait a moment as we export your data to xlsx format: \n",0.0325)
            export_df_slice = export_data(df_slice)
            print("Exporting to XLSX".center(30,"="))
            time.sleep(1.5)
            export_df_slice.to_excel(xlsx_name_sliced+".xlsx", index=False)
            delay_print(f"Your data has been saved as: {xlsx_name_sliced}.xlsx \n",0.0325)
        except NameError:
            response = pyip.inputYesNo("No sliced dataset exists. Would you like to create a sliced dataset to export (yes/no)?: \n")
            if response == "yes".lower() or response == "y".lower():
                slice_data(df)
                delay_print("Okay. Please wait a moment as we export your data to xlsx format: \n",0.0325)
                export_df_slice = export_data(df_slice)
                print("Exporting to XLSX".center(30,"="))
                time.sleep(1.5)
                export_df_slice.to_excel(xlsx_name_sliced+".xlsx", index=False)
                delay_print(f"Your data has been saved as: {xlsx_name_sliced}.xlsx \n",0.0325)
            elif response == "no".lower() or response == "n".lower():
                response = pyip.inputYesNo("Would you like to export the entire dataset instead (yes/no)?: \n")
                if response == "yes".lower() or response == "y".lower():
                    delay_print("What would you like to name your xlsx file (entire dataset): \n", 0.0325)
                    csv_name_entire = input()
                    delay_print("Okay. Please wait a moment as we export your data to xlsx format: \n",0.0325)
                    export_df = export_data(df)
                    print("Exporting to XLSX".center(30,"="))
                    time.sleep(1.5)
                    export_df.to_excel(xlsx_name_entire+".xlsx", index=False)
                    delay_print(f"Your data has been saved as: {xlsx_name_entire}.xlsx \n",0.0325)
                elif response == "no".lower() or response == "n".lower():
                    print("No problem. Change this if necessary later. \n")

def export_data_questions():
    global csv_name_entire
    global csv_name_sliced
    global xlsx_name_entire
    global xlsx_name_sliced
    
    delay_print("Would you like to export your data as a csv or xlsx file? (yes/no): \n",0.0325)
    response = pyip.inputYesNo()
    if response == "yes".lower() or response == "y".lower():
        response = pyip.inputChoice(prompt="Which format would you like? (csv, xlsx, both) \n",
                                   choices=["csv", "xlsx", "both"])
        if response == "csv".lower():
            csv_questions()
        elif response == "xlsx".lower():
            xlsx_questions()
        elif response == "both".lower():
            csv_questions()
            xlsx_questions()
            
    elif response == "no".lower() or response == "n".lower():
        delay_print("Okay, no problem. \n",0.0325)

delay_print("Welcome to the CoinGecko API service!\n",0.0325)
df = launch_program()
print(df, '\n')
print("Your data has been stored in the variable df for any further data analysis. \n")

while True:
    response = pyip.inputYesNo(prompt="Would you like to perform additional operations on your data? (yes/no): \n")
    if response == "yes".lower() or response == "y".lower():
        response = pyip.inputChoice(prompt="What operation would you like to perform? (slice data, visualize data, close program): \n",
                                    choices=["slice data", "visualize data", "close program"])
        if response == "slice data":
            df_slice = slice_data(df)
        elif response == "visualize data":
            visualize_data()
        elif response == "close program":
            delay_print("Please wait a few moments as we save your data: \n", 0.0325)
            print("Saving Data".center(30,"="))
            time.sleep(3)
            delay_print("Your data as been saved! \n", 0.0325)
            export_data_questions()
            delay_print("Please wait a few moments as we close the program: \n".center(20,"="),0.0325)
            print("Closing Program".center(30,"="))
            time.sleep(3)
            break
            
    # can add more logic here later when necessary
    elif response == "no".lower() or response == "n".lower():
        delay_print("Please wait a few moments as we save your data: \n", 0.0325)
        print("Saving Data".center(30,"="))
        time.sleep(3)
        delay_print("Your data has been saved! \n", 0.0325)
        export_data_questions()
        delay_print("Please wait a few moments as we close the program: \n".center(20,"="),0.0325)
        print("Closing Program".center(30,"="))
        time.sleep(3)
        break
delay_print("Thank you for using the CoinGeckoApi program. Happy analyzing!",0.0325)
