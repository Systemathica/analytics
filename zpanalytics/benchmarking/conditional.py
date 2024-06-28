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
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class ConditionalPerformance_g_Returns(Func):
    """Function class for calculating returns in different environment conditions.
    """
    @classmethod
    def _std_params(cls, name=None):
        params = dict(environment_returns=None, environment_label='Environment', bins=[10, 30, 70, 90],
                      bin_labels=['0-10%', '10-30%', '30-70%', '70-90%', '90-100%'])
        return params

    @classmethod
    def _execute(cls, operand: pd.DataFrame = None, params: dict = None) -> object:
        # Function to determine bins
        def determine_bin(row, boundaries):
            for i, b in enumerate(boundaries):
                if row < b:
                    return i
            return len(boundaries)

        # joining portfolio returns with environment returns
        benchmark = params['environment_label'] + "_ENV"
        df = operand.join(params['environment_returns'].to_frame(benchmark), how='inner')

        # calculate the percentiles of the environment returns
        percentiles = np.percentile(df[params['environment_label']], params['bins'])
        df['bin'] = df[benchmark].apply(lambda x: determine_bin(x, percentiles))
        df['bin_labels'] = df['bin'].map(dict(enumerate(params['bin_labels'])))
        avg_returns = df.groupby('bin_labels').mean()

        # plotting
        sns.set_style('whitegrid')
        sns.set_context('talk')
        sns.set_palette('dark')
        sns.set(font_scale=0.75)

        fig, axs = plt.subplots(1, 1, figsize=(8, 6))
        fig.suptitle('Portfolio Returns in Benchmark Performance Bins', wrap=True)
        bar_width = 0.40 / len(operand.columns)

        # Creating index for grouped bar chart
        r1 = np.arange(len(avg_returns))
        df = df.drop(columns=['bin', 'bin_labels', benchmark])
        for p, port in enumerate(df.columns):
            rp = [x + (p - 1) * bar_width for x in r1]
            axs.bar(rp, avg_returns[port] * 100, width=bar_width, label=port)

        rb = [x + p * bar_width for x in r1]
        axs.bar(rb, avg_returns[benchmark] * 100, width=bar_width, label=benchmark, alpha=0.7)

        #  Plotting
        axs.set_title(f'{benchmark}')
        # axs.set_xlabel('Benchmark Return Percentile')
        axs.set_ylabel('Average Return (%)')
        axs.set_xticks([r + bar_width / 2 for r in range(len(avg_returns))])
        axs.set_xticklabels(avg_returns.index)
        axs.legend()
        axs.grid(True, axis='y', which='both')

        # save
        plt.savefig('Results Environment Analysis.png', bbox_inches='tight')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

        avg_returns = avg_returns.drop(columns=['bin'])

        return avg_returns