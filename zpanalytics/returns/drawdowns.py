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


class Drawdowns_g_R(Func):
    """Calculate rolling drawdowns given returns.
    """

    @classmethod
    def _std_params(cls, name=None):
        params = dict(freq='M', type=['flat'])
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> DataFrame:
        freq_returns = Cumulate_g_Returns({'freq': params['freq'], 'extrapolate': True})(operand)

        freq_index = (1.0 + freq_returns).cumprod()
        expanding_max_index = freq_index.expanding().max()
        drawdown = -1.0 * ((expanding_max_index - freq_index) / expanding_max_index).applymap(lambda x: x if x > 0 else 0)

        return drawdown


class AverageDrawdowns_g_R(Func):
    """Calculate the average drawdown given returns.
    """

    @classmethod
    def _std_params(cls, name=None):
        params = dict(freq='M')
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> DataFrame:
        drawdown = Drawdowns_g_R(params)(operand)

        # calculate rolling average of the drawdown
        avg_drawdown = drawdown.expanding().mean()

        return avg_drawdown


class MaxDrawdowns_g_R(Func):
    """Calculate the maximum drawdown given returns.
    """

    @classmethod
    def _std_params(cls, name=None):
        params = dict(freq='M')
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> DataFrame:
        drawdown = Drawdowns_g_R(params)(operand)

        # calculate rolling average of the drawdown
        max_drawdown = drawdown.expanding().max()

        return max_drawdown


class LongestDrawdownPeriods_g_R(Func):
    """Calculate the longest N drawdown periods given returns.
    """

    @classmethod
    def _std_params(cls, name=None):
        params = dict(freq='M', num_periods=5)
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> DataFrame:
        drawdowns = Drawdowns_g_R(params)(operand)

        def find_longest_drawdown_periods_for_column(drawdown_series, num_periods):
            in_drawdown = False
            drawdown_periods = []

            for i in range(len(drawdown_series)):
                if drawdown_series.iloc[i] < 0:
                    if not in_drawdown:
                        in_drawdown = True
                        start_date = drawdown_series.index[i]
                        max_drawdown = drawdown_series.iloc[i]
                        max_drawdown_date = drawdown_series.index[i]
                    else:
                        if drawdown_series.iloc[i] < max_drawdown:
                            max_drawdown = drawdown_series.iloc[i]
                            max_drawdown_date = drawdown_series.index[i]
                else:
                    if in_drawdown:
                        end_date = drawdown_series.index[i - 1]
                        period_length = end_date - start_date
                        drawdown_periods.append((start_date, end_date, period_length, max_drawdown, max_drawdown_date))
                        in_drawdown = False

            if in_drawdown:
                end_date = drawdown_series.index[-1]
                period_length = end_date - start_date
                drawdown_periods.append((start_date, end_date, period_length, max_drawdown, max_drawdown_date))

            drawdown_df = pd.DataFrame(drawdown_periods, columns=['start_date', 'end_date', 'length', 'max_drawdown', 'max_drawdown_date'])
            drawdown_df = drawdown_df.sort_values(by='length', ascending=False)
            drawdown_df = drawdown_df.head(num_periods)
            drawdown_df.index = range(1, len(drawdown_df) + 1)

            return drawdown_df

        all_results = []

        for column in drawdowns.columns:
            result_df = find_longest_drawdown_periods_for_column(drawdowns[column], params['num_periods'])
            result_df.columns = pd.MultiIndex.from_product([[column], result_df.columns])
            all_results.append(result_df)

        combined_results = pd.concat(all_results, axis=1)

        return combined_results
