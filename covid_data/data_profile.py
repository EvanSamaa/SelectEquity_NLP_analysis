import pandas as pd
import matplotlib.pyplot as plt


# plot accumulative graph for top10 states
def plot_accum_topN(state_data, N):
    sorted_state_data = (state_data.T).sort_values(by=['10/9/20'],
                                                   ascending=False).T
    sorted_state_data.iloc[:, :N].plot()
    # plt.show()
    plt.savefig('./plots/accum_top%d.png' % N)


# plot daily graph for top5 states
def plot_daily_topN(daily_state_data, N):
    sorted_daily_state_data = (daily_state_data.T).sort_values(by=['10/9/20'],
                                                               ascending=False).T
    sorted_daily_state_data.iloc[:, :N].plot()
    # plt.show()
    plt.savefig('./plots/daily_top%d.png' % N)


# plot 7-day running avg graph for top5 states
def plot_rollavg_topN(daily_state_data, N):
    roll7_state_data = daily_state_data.rolling(7).mean()
    sorted_roll7_state_data = roll7_state_data.T.sort_values(by=['10/1/20'],
                                                             ascending=False).T
    sorted_roll7_state_data.iloc[:, :N].plot()
    # plt.show()
    plt.savefig('./plots/rollavg_top%d.png' % N)


# plot daily graph for top1 state in bar graph
def plot_rollavg_daily(daily_state_data):
    roll7_state_data = daily_state_data.rolling(7).mean()
    sorted_roll7_state_data = roll7_state_data.T.sort_values(by=['10/1/20'],
                                                             ascending=False).T
    sorted_daily_state_data = (daily_state_data.T).sort_values(by=['10/9/20'],
                                                               ascending=False).T
    ax = sorted_roll7_state_data.iloc[:, :1].plot(color='red')
    sorted_daily_state_data.iloc[:, :1].plot(kind='bar', ax=ax)
    # plt.show()
    plt.savefig('./plots/rollavg_daily.png')


if __name__ == "__main__":
    # read data
    data = pd.read_csv("./data/time_series_covid19_confirmed_US.csv",
                       delimiter=',',
                       index_col=0)
    temp = data.groupby(['Province_State']).sum()
    state_data = (temp.iloc[:, 5:]).T  # accumulative cases group by state
    daily_state_data = state_data.diff()  # daily cases group by state
    # print(daily_state_data.head(5))

    plot_accum_topN(state_data, 10)
    plot_daily_topN(daily_state_data, 5)
    plot_rollavg_topN(daily_state_data, 5)
    plot_rollavg_daily(daily_state_data)
