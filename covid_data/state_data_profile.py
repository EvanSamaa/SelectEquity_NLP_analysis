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
    roll7_state_data.plot(color='red', ax=ax)
    daily_onestate_data.plot(kind='bar', ax=ax)
    ax.xaxis_date()
    myLocator = mticker.MultipleLocator(7)
    ax.xaxis.set_major_locator(myLocator)
    fig.autofmt_xdate()
    # plt.show()
    try:
        plt.savefig('./plots/specific_state/%s/rollavg+daily_%s.png' % (state, state))
    except FileNotFoundError:
        mkdir_p("./plots/specific_state/%s" % state)
        plt.savefig('./plots/specific_state/%s/rollavg+daily_%s.png' % (state, state))


if __name__ == "__main__":
    # read data
    data = pd.read_csv("./data/time_series_covid19_confirmed_US.csv",
                       delimiter=',',
                       index_col=0)
    temp = data.groupby(['Province_State']).sum()
    all_states_data = (temp.iloc[:, 5:]).T  # accumulative cases group by state
    daily_states_data = all_states_data.diff()  # daily cases group by state

    state_of_interest = 'Texas'

    plot_accum(all_states_data, state_of_interest)
    plot_daily(daily_states_data, state_of_interest)
    plot_rollavg(daily_states_data, state_of_interest)
    plot_rollavg_daily(daily_states_data, state_of_interest)
