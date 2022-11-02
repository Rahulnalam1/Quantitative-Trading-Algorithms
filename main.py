import alpaca_trade_api as tradeapi
import threading
import time
import datetime

API_KEY = 'PKLOXCYTX7XTOB9R9BS6'
API_SECRET = 'G1XXZTQtuyHXo6OVPcg5iIZkWB9cUFpPPEyJX8fq'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'


#Creating a longShort python class (constructor)
class longShort:

  def __init__(self):
    self.alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')
    self.allStocks = []
    rahulsStockUniverse = [
      'META', 'ATVI', 'AMZN', 'U', 'AAPL', 'SQ', 'MTTR', 'AMD', 'GOOG', 'VZ',
      'TMUS', 'RIVN', 'SPOT', 'NFLX', 'CRM', 'BAC', 'GS', 'BLK', 'TSLA',
      'INTC', 'T', 'NVDA', 'SHOP', 'CMCSA', 'DIS', 'VMW', 'AVGO'
    ]

    #Variables to use later on.
    for stock in rahulsStockUniverse:
      self.allStocks.append([stock, 0])
      self.long = []
      self.short = []
      self.qShort = None
      self.qLong = None
      self.adjustedQLong = None
      self.adjustedQShort = None
      self.blacklistPosition = set()
      self.stockLongVal = 0
      self.stockShortVal = 0
      self.timeToClose = None

  # When the run method is called, it is going to cancel any orders that are existing
  # so I can increase my buying power to the max limit. This is done by looking orders
  #iterating through each order and cancelling the order identification.
  def run(self):
    orders = self.alpaca.list_orders(status="open")
    for order in orders:
      self.alpaca.cancel_order(order.id)

    # Need to wait for the market to open, this function will count down second by second till the market is open

    print("Awaiting for today's market start... ")
    alpacaMA = threading.Thread(target=self.awaitMarketOpen)
    #alpaca api checking time till market is opened.
    alpacaMA.start()
    alpacaMA.join()
    print("Today's Market has Officially Opened!!")
    #Market opens at 9:30 EST every weekday and closed on weekends
    #This also means the portfolio rebalances every minute so data is new, will either go long or short on stocks based on the percentage change from the previous few minutes.

    #Execution of the Trading Algo

    while True: 

      #Need to figure out when the market will close to efficiently exercise trades. 
      alpacaClock = self.alpaca.get_clock()
      marketClosingTime = alpacaClock.next_close.replace(tzinfo = datetime.timezone.utc).timestamp()
      currentTime = alpacaClock.timestamp.replace(tzinfo = datetime.timezone.utc).timestamp()
      self.timeToClose = marketClosingTime - currentTime


      if (self.timeToClose < (60 * 10)): #closing all positions 10 minutes before the market closes (test with 10, 15, and 20 minutes to see what gets a better result.) 
        #Also no trades will be made in the last ten minutes before close. 
        print("The market is closing in ten minutes, exercising/closing all positions")

        stockPositions = self.alpaca.list_positions()
        for stockPosition in stockPositions: 
          if stockPosition.side == 'long':
            orderSide = 'sell'
          else:
            orderSide = 'buy'

          stockQuantity = abs(int(float(stockPosition.stockQuantity)))
          rSubmitOrder = []
          submittOrder = threading.Thread(target = self.submitOrder(stockQuantity, stockPosition.symbol, orderSide, rSubmitOrder))
          submittOrder.start()
          submittOrder.join()
          

          #Remember, run this script everyday after the market closes to see results.

          print("Snoozing for the next ten minutes until market closes.")
          time.sleep(60 * 10)
      else:
        #Need to rebalance portfolio otherwise. 
        targetRebalance = threading.Thread(target = self.rebalance)
        targetRebalance.start()
        targetRebalance.join()
        time.sleep(60)

       # If you keep this running it will run till the market open.
            
            
          
          
        

        
      

    
      
      
      

    
