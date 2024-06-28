# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Zeroth-Principles.
# 
# Created on 6/24/2024 by Zeroth-Principles-Engineering.
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

import pandas as pd
import statsmodels.api as sm


class Regress_g_Returns_p_MarketReturns(Func):
    """Regress returns witht he market returns.
    """
    @classmethod
    def _std_params(cls, name=None):
        params = dict(market_returns=None, market_label='', periods=None)
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> pd.DataFrame:
        mkt_label = params['market_label'] + "_MKT"

        mkt_ret = params['market_returns'].to_frame(name=mkt_label)

        # create a new df with the excess returns of the market and the portfolio
        regression_df = operand.join(mkt_ret, how='inner')

        # drop any rows with missing values
        regression_df = regression_df.dropna()

        # create a constant column for the regression
        regression_df = sm.add_constant(regression_df)

        # run the regression
        results_df = pd.DataFrame()
        for col in operand.columns:
            regression_results = sm.OLS(regression_df[col], regression_df[['const', mkt_label]]).fit()

            # save the results in a dataframe
            col_results_df = pd.DataFrame({'alpha': regression_results.params['const'], 'beta': regression_results.params[mkt_label],
                                           'alpha_t': regression_results.tvalues['const'], 'beta_t': regression_results.tvalues[mkt_label],
                                           'alpha_p': regression_results.pvalues['const'], 'beta_p': regression_results.pvalues[mkt_label],
                                           'r_squared': regression_results.rsquared}, index=[col])

            # concat the results to the results dataframe
            results_df = pd.concat([results_df, col_results_df])

        # scaling alpha to the right period scale
        if params['periods'] is not None:
            results_df['alpha'] = results_df['alpha'] * params['periods']

        return results_df
