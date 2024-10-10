# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Zeroth-Principles.
# 
# Created on 7/4/2024 by Zeroth-Principles-Engineering.
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

from dateutil.relativedelta import relativedelta
import pandas as pd

def convert_my_table_to_series(returns_my_table, name='PORTFOLIO'):
    returns_my_table = returns_my_table / 100.0
    returns_series = returns_my_table.stack().reset_index()
    returns_series.columns = ['Year', 'Month', name]
    returns_series['Year'] = returns_series['Year'].map(lambda x: x.year)
    # given the Year ad Month coumns in returns_prev, calculate a date column that has the last day of the month
    returns_series['Date'] = returns_series.apply(
        lambda x: pd.to_datetime(str(x['Year']) + '-' + str(x['Month']) + '-01') + relativedelta(months=1) - relativedelta(days=1), axis=1)
    returns_series = returns_series.set_index('Date')
    returns_series = returns_series.drop(['Year', 'Month'], axis=1)

    return returns_series