from tw import *
from stocks import *
from helpers import *

tw =Tw()
stock_ticker = "TSLA"
t = GoldHand(stock_ticker)
t.plotly_last_year(tw.get_plotly_title(stock_ticker)).show()


t = GoldHand(stock_ticker, static_plot=True)
t.plotly_last_year(tw.get_plotly_title(stock_ticker, static_plot=True)).show()
