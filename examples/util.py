import robin_stocks.helper as helper
import robin_stocks.orders as orders
from dataclasses import dataclass

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


# @helper.login_required
# def get_completed_option_orders():
#     ''''
#
# FFCB0934-4D96-4F93-82CF-47DF388F7B6F	AMC	2021-02-26	4	put	sell	2021-02-01T14:46:27.889319Z	credit	10	limit	short_put	short_put	0.63	10
#
# FFCB0934-4D96-4F93-82CF-47DF388F7B6F	AMC	2021-02-05	2	put	buy	2021-02-01T14:46:27.889319Z	credit	10	limit	short_put	short_put	0.63	10
#
#
# If we club orders together, then we are getting same reference id but 2 rows. and price is same which is not correct.
# So we will take only the sell side since sell side correctly reflects the price. (actual sell price - buy price)
#     '''
#     all_orders = orders.get_all_option_orders()
#     data = {}
#
#     for order in all_orders:
#         if order['state'] == 'filled':
#             for leg in order['legs']:
#                 instrument_data = helper.request_get(leg['option'])
#                 if ( (order['opening_strategy'] == 'short_put' or order['closing_strategy'] == 'short_put')):
#
#                     key = order['chain_symbol'] + "#" + instrument_data['expiration_date'] + "#" + instrument_data['strike_price']
#                     my_order = MyOrder(order['ref_id'],
#                                        order['chain_symbol'],
#                                        instrument_data['expiration_date'],
#                                        instrument_data['strike_price'],
#                                        order['created_at'],
#                                        order['direction'],
#                                        order['quantity'],
#                                        order['price'],
#                                        order['opening_strategy'],
#                                        order['closing_strategy'],
#                                        leg['side']
#                                        )
#                     if key in data:
#                         data[key].append(my_order)
#                     else:
#                         data[key] = [my_order]
#
#     return data


@helper.login_required
def get_completed_option_orders():
    ''''

FFCB0934-4D96-4F93-82CF-47DF388F7B6F	AMC	2021-02-26	4	put	sell	2021-02-01T14:46:27.889319Z	credit	10	limit	short_put	short_put	0.63	10

FFCB0934-4D96-4F93-82CF-47DF388F7B6F	AMC	2021-02-05	2	put	buy	2021-02-01T14:46:27.889319Z	credit	10	limit	short_put	short_put	0.63	10


If we club orders together, then we are getting same reference id but 2 rows. and price is same which is not correct.
So we will take only the sell side since sell side correctly reflects the price. (actual sell price - buy price)
    '''
    all_orders = orders.get_all_option_orders()
    data = {}

    for order in all_orders:
        if order['state'] == 'filled':
            for leg in order['legs']:
                instrument_data = helper.request_get(leg['option'])
                if ( (order['opening_strategy'] == 'short_put' or order['closing_strategy'] == 'short_put')):
                    key = order['ref_id']
                    my_order = MyOrder(order['ref_id'],
                                       order['chain_symbol'],
                                       instrument_data['expiration_date'],
                                       instrument_data['strike_price'],
                                       order['created_at'],
                                       order['direction'],
                                       order['quantity'],
                                       order['price'],
                                       order['opening_strategy'],
                                       order['closing_strategy'],
                                       leg['side']
                                       )
                    if key in data:
                        # If buy is already assigned in dict, overwrite it.
                        if leg['side'] == 'sell':
                            data[key] = my_order
                    else:
                        data[key] = my_order

    return data


def get_order_dict(data):
    result = {}
    for key in data:
        value = data[key]
        key = value.symbol + "#" + value.exp_date + "#" + value.strike_price
        if key in result:
            result[key].append(value)
        else:
            result[key] = [value]

    return result