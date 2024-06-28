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
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

"""Weights util file contains ops related to transforming/aggregating weights across cross-sectionally and vertically."""

import pandas as pd
import numpy as np
from pandas.tseries.offsets import BusinessDay

from zpmeta.funcs.func import Func
from zputils.filesrw.xls import XLS_g_DoDf

import pandas as pd
import numpy as np
from pandas.tseries.offsets import BusinessDay

from zpmeta.funcs.func import Func
from zputils.filesrw.xls import XLS_g_DoDf


class Align_g_Weights_p_Returns(Func):
    """ Function class for calculating post-performance weights aligned with returns given the rebalance weights.

    Parameters
    ----------
    operand : pd.DataFrame
        The operand here is rebalanced weights.
    params : dict
        The params is a dictionary of parameters.

    Returns
    -------
    pd.DataFrame
        The output is a DataFrame of daily weights.
    """

    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        """
        Standard parameters for the function class.
        return: dict
            BOD: bool
                Whether the output weight is beginning of day or end of day.
            freq: str
                The frequency of the output weights.
            returns: DataFrame
                Portfolio asset returns
        """
        return dict(returns=None, portfolio_by='PORTFOLIO', asset_by=None)

    @classmethod
    def _execute(cls, operand: pd.DataFrame = None, params: dict = None) -> object:
        returns = params["returns"]

        blank_day = returns.index[-1] + BusinessDay()
        blank_day_ret = pd.DataFrame(np.NaN, columns=returns.columns, index=[blank_day])
        returns = returns.combine_first(blank_day_ret)

        one_plus_returns = 1.0 + returns

        # operand = operand.copy()
        # if params['portfolio_by'] is None:
        #     # add a level to the operand column with the level name 'Portfolio' and value 0
        #     operand.columns = pd.MultiIndex.from_tuples([(0, x) for x in operand.columns], names=['Portfolio', operand.columns.name])

        portfolio_dict = operand.groupby(by=params['portfolio_by'], axis='columns')

        res_ddf = dict()
        for plabel, pWeights in portfolio_dict:
            bodStartingWeights = pWeights.dropna(how='all').droplevel(params['portfolio_by'], axis='columns')

            bodStartingWeights['portfolio'] = range(0, len(bodStartingWeights))

            startWeightsOnAllDays = bodStartingWeights.reindex(one_plus_returns.index, method='pad')

            x = one_plus_returns.cumprod().shift().fillna(method='pad').fillna(1)
            cumulativeReturns = x / x.reindex(startWeightsOnAllDays['portfolio'].drop_duplicates().index, method='pad') \
                .reindex(startWeightsOnAllDays.index, method='pad') - 1
            one_plus_cumulativeReturns = 1.0 + cumulativeReturns

            startWeightsOnAllDays = startWeightsOnAllDays.drop(['portfolio'], axis=1)

            assetCumulativeReturns = startWeightsOnAllDays.mul(cumulativeReturns, level=params['asset_by'], axis='columns')

            portfolioCumulativeReturns = assetCumulativeReturns.sum(axis=1, skipna=True)

            one_plus_portfolioCumulativeReturns = 1.0 + portfolioCumulativeReturns

            nonNormalizedWeights = startWeightsOnAllDays.mul(one_plus_cumulativeReturns, level=params['asset_by'], axis='columns')

            normalizedWeights = nonNormalizedWeights.div(one_plus_portfolioCumulativeReturns, axis=0)

            pvalue = normalizedWeights

            pvalue = pvalue.reindex(startWeightsOnAllDays.columns, axis='columns')

            res_ddf[plabel] = pvalue

            # # save all the intermediate results to xls
            # worksp = r"C:\Users\raman\OneDrive\MSx\CMC\Applications\Citadel\Screening"
            # XLS_g_DoDf(dict(fpath=(worksp,f'PPWeights_g_RebalanceWeights')))(dict(
            #     returns=returns,
            #     bodStartingWeights=bodStartingWeights,
            #     startWeightsOnAllDays=startWeightsOnAllDays,
            #     cumulativeReturns=cumulativeReturns,
            #     assetCumulativeReturns=assetCumulativeReturns,
            #     portfolioCumulativeReturns=portfolioCumulativeReturns,
            #     nonNormalizedWeights=nonNormalizedWeights,
            #     normalizedWeights=normalizedWeights,
            #     pvalue=pvalue
            # ))

        # join the dictionary of df res_ddf
        res = pd.concat(res_ddf, axis=1, names=[params['portfolio_by']])

        return res


class PortfolioReturns_g_Weights_p_Returns_TC(Func):
    """ Function class for calculating portfolio returns given the rebalanced weights.

    Parameters
    ----------
    operand : pd.DataFrame
        The operand here is rebalanced weights.
    params : dict
        The params is a dictionary of parameters.

    Returns
    -------
    pd.DataFrame
        The output is a DataFrame of returns.
    """

    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        return dict(returns=None, portfolio_by=None, asset_by=None, TC=None)

    @classmethod
    def _execute(cls, operand: pd.DataFrame = None, params: dict = None) -> object:
        ppweights = Align_g_Weights_p_Returns(params)(operand)
        contributed_returns = ppweights.mul(params["returns"], level=params['asset_by'], axis='columns')

        if params['TC'] is not None:
            turnover = Turnover_g_Weights_p_Returns(params)(ppweights)
            contributed_returns = (contributed_returns - turnover*params['TC']*2.0)

        portfolio_returns = contributed_returns.groupby(axis=1, level=params['portfolio_by']).sum()

        return portfolio_returns

class Turnover_g_Weights_p_Returns(Func):
    """ Function class for calculating portfolio turnover given the rebalanced weights.
    """

    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        return dict(returns=None, portfolio_by=None, asset_by=None)

    @classmethod
    def _execute(cls, operand: pd.DataFrame = None, params: dict = None) -> object:
        security_returns = params["returns"]

        weights = Align_g_Weights_p_Returns(params)(operand)
        portfolio_returns = PortfolioReturns_g_Weights_p_Returns_TC(dict(returns=security_returns, portfolio_by=params['portfolio_by'],
                                                                           asset_by=params['asset_by']))(weights)
        ppweights = weights.mul(1.0+security_returns, level=params['asset_by'], axis='columns')
        ppweights = ppweights.div(1.0+portfolio_returns, level=params['portfolio_by'], axis='columns')
        ppweights = ppweights.shift(1).fillna(0.0)

        turnover = ppweights.sub(weights).abs() / 2.0

        return turnover
