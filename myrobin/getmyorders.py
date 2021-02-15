import robin_stocks as r
import os
import robin_stocks.orders as orders
import robin_stocks.export as export
import pyotp
from myrobin.robinorders import get_completed_option_orders, get_order_dict, MyOrder
from datetime import datetime
from datetime import date
from dataclasses import dataclass

'''
orders is list of this objects.

@dataclass
class MyOrder:
    ref_id: str
    symbol: str
    exp_date: str
    strike_price: str
    created_at: str
    direction: str
    quantity: int
    price: float
    opening_strategy: str
    closing_strategy: str
    side: str
    pl: float

'''

@dataclass
class MyOrdersProfitLoss:
    orders: list
    pl : float



def exportOrders():
    login = r.login(os.getenv('robin_username'), os.getenv('robin_password'))
    export.export_completed_option_orders('/Users/iniyanparamasivam/code-base/robin_stocks')


def getOrders():
    r.login(os.getenv('robin_username'), os.getenv('robin_password'))
    completed_orders = get_completed_option_orders()
    completed_orders_dict = get_order_dict(completed_orders)

    (ongoing_orders, past_orders) = separateOrders(completed_orders_dict)
    return (ongoing_orders, past_orders)

def getPastOrdersPL(past_orders):

    result_list = convertDictToListOrders(past_orders)
    order_pl_outer_list = []

    for outer in result_list:
        pl = calculate_profit_loss(outer)
        order_pl_outer_list.append(MyOrdersProfitLoss(outer, pl))

    return order_pl_outer_list



def calculate_profit_loss(orders):
    # TODO: correct this logic. If only some orders are closed, (by buying back), we will have issues.

    pl = 0.0
    for order in orders:
        quantity = (float)(order.quantity)
        price = (float)(order.price)

        if(order.direction == 'credit'):
            pl = pl + (quantity * 100.0 * price)

        if(order.direction == 'debit'):
            pl = pl - (quantity * 100.0 * price)

    return pl


def convertDictToListOrders(result_dict):
    # list of list carrying all the order objects.
    result_list = []
    for key in result_dict:
        inner_list = []
        for v in result_dict[key]:
            inner_list.append(v)
        result_list.append(inner_list)
    return result_list


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
    (ongoing_orders, past_orders) = getOrders()
    getPastOrdersPL(past_orders)
