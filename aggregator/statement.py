import robin_stocks as r
import os
from webull import webull

def get_robinhood_balance():
    r.login(os.getenv('robin_username'), os.getenv('robin_password'))
    result = r.load_portfolio_profile()
    # total portfolio amount is
    total_amount = float(result['equity'])
    return total_amount

def get_webull_balance():
    w = webull()
    '''
    content of the file. 
    <username>
    <password>
    <code>
    '''
    with open("/Users/iniyanparamasivam/webull.txt", encoding = 'utf-8') as f:
        username = f.readline().rstrip()
        password = f.readline().rstrip()
        code = f.readline().rstrip()

    w.login(username, password)
    w.get_trade_token(code)
    acc = w.get_account()
    return acc['netLiquidation']

if __name__ == "__main__":
    robinhood_balance = get_robinhood_balance()
    webull_balance = get_webull_balance()
    print("robinhood balance is " + str(robinhood_balance))
    print("webull balance is " + str(webull_balance))
    total_balance = float(robinhood_balance) + float(webull_balance)
    print("Total balance is " + str(total_balance))