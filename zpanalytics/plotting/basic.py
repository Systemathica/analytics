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
import scipy
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import seaborn as sns

def plot_linechart(drawdowns, title=None, filename=None, pct=True, log=False):
    # plot the drawdowns with nicely formatted dates on the horizontal axis, dates on the x-axis in the format '%Y-%m-%d' tilted at 90 degrees, and the y-axis in percentage format
    if title is None:
        title = 'Drawdowns'

    sns.set_style('whitegrid')
    sns.set_context('talk')
    sns.set_palette('dark')
    sns.set(font_scale=1.5)
    plt.figure(figsize=(36, 12))
    plt.plot(drawdowns)

    plt.title(title)

    # add legend
    plt.legend(drawdowns.columns)

    # add vertical and horizontal gridlines
    plt.grid(True, axis='both', which='both')

    # format the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    plt.xticks(rotation=45)

    # format the y-axis
    if pct:
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    if log:
        plt.yscale('log')

    # if filename is not None, save the plot to the filename as an HTML file
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')

    plt.show()


# plot the monthly and annual excess returns as bar charts
def plot_barchart(data, title=None, filename=None, xformat='%Y-%m', width=20, data2=None):
    if title is None:
        title = 'Returns'

    # if data is a dataframe, convert it to a series
    # if isinstance(data, pd.DataFrame):
    #     data = data.iloc[:,0]

    sns.set_style('whitegrid')
    sns.set_context('talk')
    sns.set_palette('dark')
    sns.set(font_scale=1.5)

    plt.figure(figsize=(36, 12))
    plt.bar(data.index, data, color='steelblue', edgecolor='steelblue', width=width)

    plt.title(title)

    # format the x-axis but only show the year
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(xformat))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    # format the y-axis
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.xticks(rotation=45)

    # add legend
    plt.legend([data.name])

    # if data2 is not None, plot it as a line chart with a secondary y-axis using axes
    if data2 is not None:
        ax2 = plt.gca().twinx()
        ax2.plot(data2, color='olivedrab', linewidth=4)
        ax2.set_ylabel(data2.name, color='olivedrab')
        ax2.tick_params(axis='y', labelcolor='olivedrab')
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        ax2.legend([data2.name], loc='upper left')

    # add horizontal gridlines
    plt.grid(True, axis='y', which='both')

    # add legend for both the y-axis and the secondary y-axis

    # if filename is not None, save the plot to the filename as an HTML file
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')

    plt.show()


# plot the correlation matrix, do not display the diagonal, and format the values to 2 decimal places
def plot_heatmap(correlation, title=None, filename=None):
    if title is None:
        title = 'Correlation Matrix'

    sns.set_style('whitegrid')
    sns.set_context('talk')
    sns.set_palette('dark')
    sns.set(font_scale=1.5)

    plt.figure(figsize=(36, 12))
    sns.heatmap(correlation, annot=True, fmt='.2f', vmin=-1, vmax=1, center=0, cmap='coolwarm', square=True)
    plt.title(title)

    # if filename is not None, save the plot to the filename as an HTML file
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')

    plt.show()