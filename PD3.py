import requests
import time

# API_KEY = {'X-API-key': 'W7J6V4W6'}

s = requests.Session()
s.headers.update({'X-API-key':'W7J6V4W6'})

def get_status():
    resp = s.get('http://localhost:9999/v1/case')
    if resp.ok:
        case = resp.json()
        return case['status']
   
def bid_ask(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/securities/book', params = payload)
    if resp.ok:
        book = resp.json()
        return book['bids'][0]['price'], book['asks'][0]['price']
   
def bid_ask_size(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/securities/book', params = payload)
    if resp.ok:
        book = resp.json()
        return book['bids'][0]['quantity'] -book['bids'][0]['quantity_filled'], book['asks'][0]['quantity'] -book['asks'][0]['quantity_filled']
   
def current_position(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/securities', params = payload)
    if resp.ok:
        book = resp.json()
        return book[0]['position']

   
def open_orders(ticker):
    payload = {'ticker': ticker}
    resp = s.get ('http://localhost:9999/v1/orders', params = payload)
    if resp.ok:
        orders = resp.json()
        buy_orders = [item for item in orders if item["action"] == "BUY"]
        sell_orders = [item for item in orders if item["action"] == "SELL"]
        return buy_orders, sell_orders
   
def news1():
    resp = s.get("http://localhost:9999/v1/news")
    if resp.ok:
        news = resp.json()
        return float(news[0]['body'][-5:])

def news():
    resp = s.get("http://localhost:9999/v1/news")
    if resp.ok:
        news = resp.json()  
        return news[0]
   
def main():
   
    status = get_status()
    while status == 'ACTIVE':
       
        bid_price_UB, ask_price_UB = bid_ask('UB')
        bid_price_GEM, ask_price_GEM = bid_ask('GEM')
        bid_price_ETF, ask_price_ETF = bid_ask('ETF')
       
        if 40 < news1() < 60:
            if news1() < bid_price_UB:
                sell_leg = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'UB', 'type': 'MARKET', 'quantity': 100, 'price': bid_price_UB, 'action': 'SELL'})          
            if news1() > ask_price_UB:
                buy_leg = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'UB', 'type': 'MARKET', 'quantity': 100, 'price': ask_price_UB, 'action': 'BUY'})
        if 20 < news1() < 30:
            if news1() < bid_price_GEM:
                sell_leg = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'GEM', 'type': 'MARKET', 'quantity': 100, 'price': bid_price_GEM, 'action': 'SELL'})
            if news1() > ask_price_GEM:
                buy_leg = s.post('http://localhost:9999/v1/orders', params = {'ticker': 'GEM', 'type': 'MARKET', 'quantity': 100, 'price': ask_price_GEM, 'action': 'BUY'})
        time.sleep(5)
