# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Zeroth-Principles.
# 
# Created on 1/27/2024 by Zeroth-Principles-Engineering.
# For suggestions, please write to engineering@zeroth-principles.com.
#
#  Zeroth-Meta is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Zeroth-Meta is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Zeroth-Meta. If not, see <http://www.gnu.org/licenses/>.

__copyright__ = '2024 Zeroth Principles'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = []

""" * """
from zpmeta.funcs.func import Func
from pandas import DataFrame
import pandas as pd
from dateutil.relativedelta import relativedelta
import os
import numpy as np
import math
import scipy


class Returns_g_Index(Func):
    """Function class for calculating the returns from prices.
    """
    @classmethod
    def _std_params(cls, name=None):
        params = dict()
        return params

    @classmethod
    def _execute(cls, operand: DataFrame = None, params: dict = None) -> object:
        result = operand.pct_change()
        return result

class Index_g_Returns(Func):
    """Function class for calculating the index from returns.
    """
    @classmethod
    def _execute(cls, operand: DataFrame = None, params: dict = None) -> DataFrame:
        total_performance_index = (1.0 + operand).cumprod()*100.0
        return total_performance_index


class IndexedCumulativeReturns_g_Returns(Func):
    """
    Function class for calculating the cumulative return from daily returns give index.

    Parameters
    ----------
    operand : pd.DataFrame
        The operand here is rebalanced weights.
    period : tuple
        The period is a tuple of (start_datetime, end_datetime).
    params : dict
        The params is a dictionary of parameters.

    Returns
    -------
    pd.DataFrame
        The output is a DataFrame of daily weights.
    """
    @classmethod
    def execute(cls, operand: pd.DataFrame = None, params: dict = None) -> object:
        idx = pd.Index(params["index"])
        period = (operand.index[0], operand.index[-1])

        temp = operand.truncate(period[0], period[1])
        temp = temp.fillna(0.0)

        return_grouped = (1 + temp).groupby(idx.searchsorted(temp.index)).cumprod() - 1
        return_grouped = return_grouped.fillna(0.0)

        return return_grouped


class Cumulate_g_Returns(Func):
    """Function class for calculating the cumulative return from daily returns.
    """
    @classmethod
    def _std_params(cls, name=None):
        params = dict(freq='M', extrapolate=True)
        return params

    @classmethod
    def _execute(cls, operand: DataFrame = None, params: dict = None) -> object:
        if params['extrapolate']:
            df = DataFrame(0, index=[operand.index[-1] + relativedelta(years=1)], columns=operand.columns)
            freq_returns = operand.combine_first(df)
        cumulative_returns = (1.0 + freq_returns).cumprod(skipna=True).fillna(method='pad').asfreq(params['freq'], method='pad')
        if params['extrapolate']:
            next_period_date = cumulative_returns.index[cumulative_returns.index >= operand.index[-1]][0]  # immediate next period date
            cumulative_returns = cumulative_returns.truncate(after=next_period_date)  # truncate after next period date

        prev_returns = cumulative_returns.shift(1).fillna(1.0)
        result = (cumulative_returns / prev_returns).dropna(how='all') - 1.0

        return result