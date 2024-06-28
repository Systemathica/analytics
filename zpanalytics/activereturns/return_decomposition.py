# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Zeroth-Principles.
# 
# Created on 10/28/2023 by Zeroth-Principles-Engineering.
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

__copyright__ = '2023 Zeroth Principles'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = []

""" Funcs for decomposing asset returns into benchmark and alpha returns. """

import pandas as pd
import numpy as np

from zpmeta.funcs.func import Func


class ActiveReturns_p_BenchmarkReturns_g_TotalReturns(Func):
    """ This is Func class that takes benchmark returns as a param. Given a dataframe of retuns it returns the active returns.
    """
    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> object:
        result = operand.subtract(params['benchmark_returns'], axis=0)
        return result


class GrinoldDecomposition_p_BenchmarkParams_g_TotalReturns(Func):
    """ This is Func class that takes benchmark returns as a param. Given a dataframe of retuns it returns the active returns.
    """
    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> object:
        benchmark_returns = params['benchmark_returns']
        benchmark_expected_return = params['benchmark_expected_return']
        riskfree_returns = params['riskfree_returns']

        result = DataFrame(index=operand.index, columns=['time_premium', 'risk_premium', 'exceptional_benchmark_returns', 'alpha'])
        result['time_premium'] = riskfree_returns
        result['risk_premium'] = benchmark_expected_return - riskfree_returns
        result = operand.subtract(params['benchmark_returns'], axis=0)
        return result

