from __future__ import print_function

from dateutil import extractMonthYearFromDateString


def getPLBySymbols(my_order_obj_pl_list):
    '''
    symbol => p/l
    :param my_order_obj_pl:
    :return:
    '''
    sym_pl_dict = {}
    for my_order_obj_pl in my_order_obj_pl_list:

        symbol = my_order_obj_pl.orders[0].symbol
        if symbol in sym_pl_dict:
            value = sym_pl_dict[symbol] + my_order_obj_pl.pl
            sym_pl_dict[symbol] = value
        else:
            sym_pl_dict[symbol] = my_order_obj_pl.pl

    sorted_dict = {k: v for k, v in sorted(sym_pl_dict.items(), key=lambda item: item[1], reverse=True)}
    return sorted_dict


def getPLBByDate(my_order_obj_list_dict):

    date_pl_dict_list = []
    for k in my_order_obj_list_dict:
        date_pl_dict_list.append(getPLByDatePerBatch(my_order_obj_list_dict[k]))

    print(date_pl_dict_list)

    result_dict = {}
    for date_pl_dict in date_pl_dict_list:
        for k in date_pl_dict:
            if k in result_dict:
                result_dict[k] = result_dict[k] + date_pl_dict[k]
            else:
                result_dict[k] = date_pl_dict[k]

    return result_dict


def getPLByDatePerBatch(my_order_obj):
    '''
    result 01/2021 => pl

    :param my_order_obj:
    :return:
    '''
    # separate buy vs sell.

    # separate buy with order created at,

    # calculate sell per contract price
    total_orders = 0
    price = 0

    for order in my_order_obj:
        if order.side == 'sell':
            total_orders = total_orders + float(order.quantity)
            order_quantity = float(order.quantity)
            order_price = float(order.price)
            price = price + (order_quantity * order_price * 100)

    sell_price_per_contract = price / total_orders

    # for buy create a map with date as key and value  (quantity * price_per_contract * 100) - (quantity * price * 100)
    # and add all the values.

    buy_profit = {}
    is_buy_present = False
    for order in my_order_obj:
        if order.side == 'buy':
            is_buy_present = True
            key = extractMonthYearFromDateString(order.created_at)
            order_quantity = float(order.quantity)
            order_price = float(order.price)

            value = (order_quantity * sell_price_per_contract) - (order_quantity * order_price * 100)
            if key in buy_profit:
                buy_profit[key] = buy_profit[key] + value
            else:
                buy_profit[key] = value

    if not is_buy_present:
        for order in my_order_obj:
            key = extractMonthYearFromDateString(order.created_at)
            order_quantity = float(order.quantity)
            order_price = float(order.price)

            value = order_quantity * order_price * 100
            if key in buy_profit:
                buy_profit[key] = buy_profit[key] + value
            else:
                buy_profit[key] = value

    return buy_profit
