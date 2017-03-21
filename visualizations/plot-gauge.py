"""
Plots several gauges from our demo data using pygal http://www.pygal.org/en/stable/documentation/types/solidgauge.html
"""

from csv import reader
import numpy as np
import pygal
from pygal.style import LightenStyle

import os


# set custom plot style
plot_style = LightenStyle('#0083b9', step=5, font_family='googlefont:Quantico',
                               font_size=22,
                               value_font_size=24,
                               value_label_font_size=22,
                               label_font_size=22,
                               major_label_font_size=22,
                               no_data_font_size=22,
                               title_font_size=22,
                               legend_font_size=15,
                               tooltip_font_size=18)


def read_data(filename):
    # read data file
    with open(filename, 'rt') as datafile:
        d = np.array(list(reader(datafile, delimiter=';')))

    # create dict where title is the key and a np array of floats represents the data columns
    data = {}
    for row in range(1, len(d)):
        data[d[row,0]] = d[row, 1:].astype(float)
    return data


def get_max(data, col):
    """
    :return: Max of specified data col
    """
    m = 0
    for row in data:
        if data[row][col] > m:
            m = data[row][col]
    return m


def gauge_plot_multi(data, png=False):
    """
    Plots multiple Gauges into one file
    :param data: data file with "title":[data]  structure
    :param png: if true plot as png, default is svg
    :return:
    """
    for ticker in data:
        # create new SolidGauge plot
        gauge = pygal.SolidGauge(
            title=ticker,
            legend_at_bottom=True,
            legend_at_bottom_columns=4,
            inner_radius=0.70,
            style=plot_style)

        # create custom formatters for values
        percent_formatter = lambda x: '{:.10g}%'.format(x)
        dollar_formatter = lambda x: '{:.2f}B$'.format(x)

        # add gauges from data
        gauge.add('Gauge $', [{'value': data[ticker][0], 'max_value': get_max(data, 0)}],
                  formatter=dollar_formatter)
        gauge.add('Gauge %', [{'value': data[ticker][1]*100, 'max_value': get_max(data, 1)*100}],
                  formatter=percent_formatter)

        gauge.add('Gauge 2', [{'value': data[ticker][2], 'max_value': get_max(data, 2)}])
        gauge.add('Gauge 3', [{'value': data[ticker][3], 'max_value': get_max(data, 3)}])

        # render plot to file
        if png:
            gauge.render_to_png(plot_dir+"/"+ticker+'_multi_gauge.png')
        else:
            gauge.render_to_file(plot_dir + "/" + ticker + '_multi_gauge.svg')


def gauge_plot_single(data, png=False):
    """
    Plots a single data col into one file for each title
    :param data: data file with "title":[data]  structure
    :param png: if true plot as png, default is svg
    :return:
    """
    for ticker in data:
        if np.isnan(data[ticker][0]): continue

        gauge = pygal.SolidGauge(
            title=ticker,
            show_legend=False,
            legend_at_bottom=True,
            legend_at_bottom_columns=4,
            inner_radius=0.70,
            style=plot_style)

        # create custom formatter for values
        custom_formatter = lambda x: '{:.2f} Custom Score'.format(x)

        # add gauges with fixed max value
        gauge.add(
            'Custom Label',
            [
                {'value': data[ticker][0], 'max_value': 5}
            ],
            formatter=custom_formatter)

        # render plot to file
        if png:
            gauge.render_to_png(plot_dir+"/"+ticker+'_gauge.png')
        else:
            gauge.render_to_file(plot_dir + "/" + ticker + '_gauge.svg')


data = read_data('demo-data.csv')

plot_dir = "gaugeplots"

# create plot directory if not exists
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

gauge_plot_multi(data, png=True)    # plot multi as png
gauge_plot_single(data)             # plot single as svg
