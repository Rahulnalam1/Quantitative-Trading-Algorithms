import alpaca_trade_api as tradeapi
import threading
import time
import datetime

API_KEY = "PKXKRKJRJT5LU1E5AIEJ"
API_SECRET = "A5XrhvpLEQPGHYmr9vrWjaFcKHjWwppEPAPUVacC"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"


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
      self.blacklist = set()
      self.longAmount = 0
      self.shortAmount = 0
      self.timeToClose = None

  # When the run method is called, it is going to cancel any orders that are currently
  #existing
  # so I can increase my buying power to the max limit. This is done by looking at the orders
  #iterating through each order and cancelling the order identification.
  def run(self):
    orders = self.alpaca.list_orders(status="open")
    for order in orders:
      self.alpaca.cancel_order(order.id)

    # Need to wait for the market to open, this function will count down second by second        till the market is open

    print("Awaiting for today's market start... ")
    alpacaMA = threading.Thread(target=self.awaitMarketOpen)  
    #alpaca api checking time till market is opened.
    alpacaMA.start()
    alpacaMA.join()
    print("Today's Market has Officially Opened!!")
    #Market opens at 9:30 EST every weekday and closed on weekends
