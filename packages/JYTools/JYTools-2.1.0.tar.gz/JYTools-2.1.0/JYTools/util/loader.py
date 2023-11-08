# !/usr/bin/env python
# coding: utf-8
import importlib

__author__ = 'zhouhenglc'


def load_function(func_name, reload=False):
    """

    :param func_name:  mode_name.func_name
            eg: JYTools.demo.some_funcs.func_plus
    :param reload:
    :return:
    """
    mod_name, _f_name = func_name.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    if reload:
        importlib.reload(mod)
    func = getattr(mod, _f_name)
    return func


if __name__ == '__main__':
    func = load_function('JYTools.demo.some_funcs.func_plus', reload=True)
