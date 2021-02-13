import robin_stocks as r
import os
import robin_stocks.orders as orders
import robin_stocks.export as export
import pyotp
from util import get_completed_option_orders, get_order_dict
from datetime import datetime
from datetime import date

def getOrders():
    login = r.login(os.getenv('robin_username'), os.getenv('robin_password'))
    allOrders = orders.get_all_option_orders()
    i = 0
    for order in allOrders:
        if order['state'] == 'filled':
            print(order['chain_symbol'])
            i = i + 1
    print(i)

def exportOrders():
    login = r.login(os.getenv('robin_username'), os.getenv('robin_password'))
    export.export_completed_option_orders('/Users/iniyanparamasivam/code-base/robin_stocks')


def getOrders():
    r.login(os.getenv('robin_username'), os.getenv('robin_password'))
    completed_orders = get_completed_option_orders()
    completed_orders_dict = get_order_dict(completed_orders)

    (ongoing_orders, past_orders) = separateOrders(completed_orders_dict)

    # printOrders(ongoing_orders)
    # print("$$$$$$$$$$$$")
    printOrders(past_orders)
    print("Close orders\n")
    print_pl(calculate_profit_loss(past_orders))
    print("Open orders\n")
    print_pl(calculate_profit_loss(ongoing_orders))



def print_pl(pl_dict):
    total_pl = 0
    for k in pl_dict:
        total_pl = total_pl + pl_dict[k]
        print(k + "===> " + (str)(pl_dict[k]))
        print("\n")

    print("Orders p/l   " + (str)(total_pl))

def calculate_profit_loss(order_dict):
    '''
    result is <symbol#exp_date> = p/l
    :param order_dict:
    :return:
    '''
    pl_dict = {}
    for key in order_dict:
        pl = 0.0
        new_key = ""
        for obj in order_dict[key]:
            new_key = obj.symbol + "#" + obj.exp_date

            quantity = (float)(obj.quantity)
            price = (float)(obj.price)

            if(obj.direction == 'credit'):
                pl = pl + (quantity * 100.0 * price)

            if(obj.direction == 'debit'):
                pl = pl - (quantity * 100.0 * price)

        pl_dict[new_key] = pl

    return pl_dict


def printOrders(result):
    for key in result:
        for v in result[key]:
            print(v)
            print("\n")
        print("##########################\n")


def separateOrders(input):
    '''
    Separate the orders into past orders and ongoing orders.

    If all the values in the key has closing_strategy as None and exp date is in future,
    then it is considered as ongoing order.

    Others are past orders.
    :return:
    '''
    ongoing_orders = {}
    past_orders = {}

    for key in input:
        values = input[key]
        closing_strategies = [v.closing_strategy for v in values]
        res = all(ele == closing_strategies[0] for ele in closing_strategies)
        exp_date = datetime.strptime(values[0].exp_date, "%Y-%m-%d").date()
        now = date.today()
        if res and exp_date > now:
            ongoing_orders[key] = values
        else:
            past_orders[key] = values

    return (ongoing_orders, past_orders)

if __name__ == "__main__":
    # d1 = datetime.strptime('2021-02-11', "%Y-%m-%d").date()
    # now = date.today()
    # print(d1 < now)
    getOrders()
