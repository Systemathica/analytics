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
from zpanalytics.returns.basic import Cumulate_g_Returns

from pandas import DataFrame
import pandas as pd
from dateutil.relativedelta import relativedelta
import os
import numpy as np
import math
import scipy


class Performance_g_Returns(Func):
    """Calculate Sharpe given excess returns.
    """
    @classmethod
    def _std_params(cls, name=None):
        params = dict(rfr=None, periods=12)
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> DataFrame:
        returns = operand.fillna(0.0)

        rfr = params['rfr'].fillna(method='ffill')
        rfr = rfr.reindex(returns.index, method='ffill')

        if params['rfr'] is None:
            excess_returns = returns
        else:
            excess_returns = returns.sub(rfr, axis=0)

        geometric_mean = scipy.stats.mstats.gmean(1.0 + excess_returns)
        gmean = geometric_mean ** (params['periods']) - 1.0
        stdev = (excess_returns.std(skipna=True)) * math.sqrt(params['periods'])
        sharpe = gmean / stdev
        skew = excess_returns.skew(skipna=True)
        kurtosis = excess_returns.kurtosis(skipna=True)

        result = DataFrame([gmean, stdev, skew, kurtosis, sharpe], index=['gmean', 'stdev', 'skew', 'kurtosis', 'sharpe'],
                           columns=excess_returns.columns).T

        return result

class Index_g_Returns(Func):
    """Calculate Sharpe given excess returns.
    """
    @classmethod
    def _std_params(cls, name=None):
        params = dict(rfr=None, periods=12)
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> DataFrame:
        returns = operand.fillna(0.0)

        rfr = params['rfr'].fillna(method='ffill')
        rfr = rfr.reindex(returns.index, method='ffill')
        print("rfr: ", rfr)

        if params['rfr'] is None:
            excess_returns = returns
        else:
            excess_returns = returns.sub(rfr, axis=0)

        print("excess_returns: ", excess_returns)

        geometric_mean = scipy.stats.mstats.gmean(1.0 + excess_returns)
        gmean = geometric_mean ** (params['periods']) - 1.0
        stdev = (excess_returns.std(skipna=True)) * math.sqrt(params['periods'])
        sharpe = gmean / stdev
        skew = excess_returns.skew(skipna=True)
        kurtosis = excess_returns.kurtosis(skipna=True)

        result = DataFrame([gmean, stdev, skew, kurtosis, sharpe], index=['gmean', 'stdev', 'skew', 'kurtosis', 'sharpe'],
                           columns=excess_returns.columns).T

        return result
