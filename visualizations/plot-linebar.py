"""
plots a mixture of line and bar charts using matplotlib and numpy
"""
from csv import reader
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def read_data(filename):
    """
    read csv data from specified file into np array, skips the first row
    :param filename: the file to read from
    :return: np.array
    """
    with open(filename, 'rt') as datafile:
        data = np.array(list(reader(datafile, delimiter=';')))

    data = data[1:]     # skip header row
    return data


data = read_data("demo-data.csv")       # get data

print(data[:,0])        # print titles
print(data[0])          # print first row

N = len(data)
index = np.arange(N)        # the x locations for the barchart
width = 0.35                # bar width

# set custom ttf font, for example Quantico
# https://fonts.google.com/specimen/Quantico
prop = fm.FontProperties(fname='fonts/Quantico-Regular.ttf')

# adjust figure size
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 30
fig_size[1] = 10
plt.rcParams["figure.figsize"] = fig_size

# split plot into subplots to plot different charts
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

# plot barchart
p1 = ax1.bar(index,
             data[:, 2].astype(float),
             width,
             color="#0AC696"
             )

# calculate offset of second bar
sub_bar = data[:, 2].astype(float) - data[:, 3].astype(float)
p2 = ax1.bar(index,
             sub_bar,
             width,
             bottom=data[:, 3].astype(float),
             color="#0083b9"
             )

ax1.set_ylabel('y Label Bar', fontproperties=prop)      # set y label of first axis
ax1.set_autoscale_on(False)                             # disable autoscale
ax1.axis([-1, N, 0, 21])                                # add own scaling range
ax1.yaxis.set_ticks(np.arange(0, 21, 1))                # set custom ticks for y-axis

# plot line on axis 2
ax2.set_ylabel('y Label Line', fontproperties=prop)
ax2.plot(data[:, 1].astype(float), color="#0ACAD0")
ax2.plot(data[:, 1].astype(float), 'ro', color="#0ACAD0")

# set plot title and x axis ticks
plt.title('Plot Title', fontproperties=prop, size=22)
plt.xticks(index, (data[:,0]))                  # x ticks are our index titles

# set font properties of both axis
for label in ax1.get_xticklabels() + ax2.get_xticklabels():
    label.set_fontproperties(prop)

# save plot to file
plt.savefig("linebar.png")