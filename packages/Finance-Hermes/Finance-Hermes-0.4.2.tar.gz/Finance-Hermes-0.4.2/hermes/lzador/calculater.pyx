# -*- encoding:utf-8 -*-
import importlib, inspect, copy, pdb
import pandas as pd


def batch_factors(data, packet_name, class_name, factors_columns,
            begin_date, end_date, data_format=2):
    res = []
    class_module = importlib.import_module(packet_name).__getattribute__(
        class_name)
    inst_module = class_module(begin_date=begin_date, end_date=end_date,
                    data_format=data_format)
    factors_func = inst_module.factors_list()
    factors_columns = factors_columns if isinstance(factors_columns, list) and len(factors_columns) > 0 else factors_func

    for func in factors_columns:
        func_module = getattr(class_module, func)
        fun_param = inspect.signature(func_module).parameters
        dependencies = fun_param['dependencies'].default
        result = getattr(class_module(),
                         func)(copy.deepcopy(data[dependencies]))
        res.append(result)
    return pd.concat(res, axis=1)
