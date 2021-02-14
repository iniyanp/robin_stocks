from __future__ import print_function


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
