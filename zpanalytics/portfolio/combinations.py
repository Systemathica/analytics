# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Zeroth-Principles.
# 
# Created on 6/25/2024 by Zeroth-Principles-Engineering.
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
from zpanalytics.portfolio.basic import Align_g_Weights_p_Returns, PortfolioReturns_g_Weights_p_Returns_TC

import pandas as pd
from copy import copy


class WeightedPortfolio_g_Portfolios_p_DollarBudget(Func):
    """Calculate the security-wise weights of the combined weighted portfolio given the individual portfolio weights and the allocation budget.
    """

    @classmethod
    def _std_params(cls, name=None):
        params = dict(returns=None, frequency=None, budget=None, portfolio_by='PORTFOLIO', asset_by='Security')
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> pd.DataFrame:
        portfolio_returns = PortfolioReturns_g_Weights_p_Returns_TC(dict(returns=params['returns'], portfolio_by='PORTFOLIO', asset_by='Security'))(operand)
        portfolio_returns.columns.name = 'Security'

        ppweights = Align_g_Weights_p_Returns(dict(returns=params['returns'], portfolio_by='PORTFOLIO', asset_by='Security'))(operand=operand)

        pLabels = operand.columns.get_level_values(params['portfolio_by']).unique()

        if params['budget'] is None:
            # create equal weighted budget
            wt = 1.0 / len(pLabels)
            budget_dict = {p_name: wt for p_name in pLabels}
        else:
            # normalize the budget
            budget_dict = {p_name: wt for p_name, wt in copy(params['budget']).items() if p_name in pLabels}
            budget_dict = {p_name: wt / sum(budget_dict.values()) for p_name, wt in copy(budget_dict).items()}

        drange = pd.date_range(start=portfolio_returns.index[0], end=portfolio_returns.index[-1], freq=params['frequency'])
        raf = pd.DataFrame(1.0, index=drange, columns=list(budget_dict.keys()))
        raf = raf.mul(budget_dict, axis=1)
        raf.columns = pd.MultiIndex.from_tuples([('Total', x) for x in raf.columns], names=['PORTFOLIO', 'Security'])

        # print("Portfolio Returns\n", portfolio_returns.head())
        # print("PPWeights\n", ppweights.head())
        # print("RAF\n", raf.head())

        raf_ppw = Align_g_Weights_p_Returns(dict(returns=portfolio_returns, portfolio_by='PORTFOLIO', asset_by='Security'))(operand=raf)
        raf_ppw.columns = raf_ppw.columns.droplevel('PORTFOLIO')
        raf_ppw.columns.name = 'PORTFOLIO'
        # print("RAF PPW\n", raf_ppw.head())

        weighted_contributions = ppweights.mul(raf_ppw, level=params['portfolio_by'], axis='columns')
        # print("Weighted Contributions\n", weighted_contributions.head())

        final_weights = weighted_contributions.groupby(axis=1, level=params['asset_by']).sum()
        # print("Final Weights\n", final_weights.head())

        return final_weights