# Include functions for creating plots for a specific state e.g. New York

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utilities import *


# plot accumulative graph for specified state
def plot_accum(all_states_data, state):
    one_state_data = all_states_data[[state]]
    one_state_data.plot()
    # plt.show()
    try:
        plt.savefig('./plots/specific_state/%s/accum_%s.png' % (state, state))
    except FileNotFoundError:
        mkdir_p("./plots/specific_state/%s" % state)
        plt.savefig('./plots/specific_state/%s/accum_%s.png' % (state, state))


# plot daily graph for specified state
def plot_daily(daily_states_data, state):
    daily_onestate_data = daily_states_data[[state]]
    daily_onestate_data.plot()
    # plt.show()
    try:
        plt.savefig('./plots/specific_state/%s/daily_%s.png' % (state, state))
    except FileNotFoundError:
        mkdir_p("./plots/specific_state/%s" % state)
        plt.savefig('./plots/specific_state/%s/daily_%s.png' % (state, state))


# plot 7-day running avg graph for specified state
def plot_rollavg(daily_states_data, state):
    daily_onestate_data = daily_states_data[[state]]
    roll7_state_data = daily_onestate_data.rolling(7).mean()
    roll7_state_data.plot()
    # plt.show()
    try:
        plt.savefig('./plots/specific_state/%s/rollavg_%s.png' % (state, state))
    except FileNotFoundError:
        mkdir_p("./plots/specific_state/%s" % state)
        plt.savefig('./plots/specific_state/%s/rollavg_%s.png' % (state, state))


# plot daily graph for top1 state in bar graph
def plot_rollavg_daily(daily_states_data, state):
    daily_onestate_data = daily_states_data[[state]]
    roll7_state_data = daily_onestate_data.rolling(7).mean()

    fig, ax = plt.subplots(figsize=(20, 10))
    daily_onestate_data.plot(kind='bar', ax=ax)
    roll7_state_data.plot(color='red', ax=ax)
    ax.legend(['7-day running average', 'actual daily cases'])
    plt.grid()
    ax.xaxis_date()
    my_xLocator = mticker.MultipleLocator(7)
    ax.xaxis.set_major_locator(my_xLocator)
    my_yLocator = mticker.MultipleLocator(500)
    ax.yaxis.set_major_locator(my_yLocator)
    fig.autofmt_xdate()
    plt.title("Daily Cases and 7-Day Running Average for %s State" % state)
    plt.xlabel('Dates')
    plt.ylabel('Daily new cases')
    # plt.show()
    try:
        plt.savefig('./plots/specific_state/%s/rollavg+daily_%s.png' % (state, state))
    except FileNotFoundError:
        mkdir_p("./plots/specific_state/%s" % state)
        plt.savefig('./plots/specific_state/%s/rollavg+daily_%s.png' % (state, state))


if __name__ == "__main__":
    # read data
    data = pd.read_csv("./data/time_series_covid19_confirmed_US.csv", delimiter=',', index_col=0)
    temp = data.groupby(['Province_State']).sum()
    all_states_data = (temp.iloc[:, 5:]).T  # accumulative cases group by state
    daily_states_data = all_states_data.diff()  # daily cases group by state

    # select your state of interest
    state_of_interest = 'New York'

    # select plotting options
    plot_accum(all_states_data, state_of_interest)
    plot_daily(daily_states_data, state_of_interest)
    plot_rollavg(daily_states_data, state_of_interest)
    plot_rollavg_daily(daily_states_data, state_of_interest)
