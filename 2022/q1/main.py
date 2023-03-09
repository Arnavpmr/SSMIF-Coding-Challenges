"""
Arnav Marchareddy
I pledge my honor that I have abided by the Stevens Honor System
"""

import pandas as pd
import pandas_datareader as pdr
import numpy as np
import scipy.stats as stats


tsla = pdr.DataReader('TSLA', 'yahoo', start='01/01/2021', end='12/31/2021', retry_count=2, api_key='ENSW68DAY10U01RF')
cola = pdr.DataReader('KO', 'yahoo', start='01/01/2021', end='12/31/2021', retry_count=2, api_key='ENSW68DAY10U01RF')

tsla_open_prices = list(tsla.get('Open'))
tsla_close_prices = list(tsla.get('Adj Close'))

cola_open_prices = list(cola.get('Open'))
cola_close_prices = list(cola.get('Adj Close'))


def statistics():
    # Part A
    tsla_daily_returns = [(tsla_close_prices[i] - tsla_open_prices[i]) / tsla_open_prices[i] * 100 for i in range(len(tsla_close_prices) - 1)]
    cola_daily_returns = [(cola_close_prices[i] - cola_open_prices[i]) / cola_open_prices[i] * 100 for i in range(len(cola_close_prices) - 1)]

    tsla_group = np.array(tsla_daily_returns)
    cola_group = np.array(cola_daily_returns)

    t_test_means_result = stats.ttest_ind(tsla_group, cola_group)

    print(f"""a)  To test for a statistically significant difference in mean daily returns, I used a 2 sample t test.
    In order to conduct this test, I am assuming that the observations in each sample are independent and have equal
    variances.\n\n    p-value: {t_test_means_result[1]}\n\n    Result: Because the p-value is less than the significance level
    of 0.05, we reject the null hypothesis, meaning there is a very significant difference between the mean daily returns
    of the two equities""")

    #Part B
    cola_deviation = [abs((cola_close_prices[i] - np.mean(cola_close_prices)))/cola_close_prices[i] for i in range(len(cola_close_prices) - 1)]
    tsla_deviation = [abs((tsla_close_prices[i] - np.mean(tsla_close_prices)))/tsla_close_prices[i] for i in range(len(tsla_close_prices) - 1)]

    tsla_group = np.array(tsla_deviation)
    cola_group = np.array(cola_deviation)

    t_test_deviation_result = stats.ttest_ind(tsla_group, cola_group)

    print(f"""b)  To test for a statistically significant difference in deviations, I used a 2 sample t test.
    In order to conduct this test, I am assuming that the observations in each sample are independent and have equal
    variances.\n\n    p-value: {t_test_deviation_result[1]}\n\n    Result: Because the p-value is less than the significance level
    of 0.05, we reject the null hypothesis, meaning there is a very significant difference between the deviations 
    of the two equities""")


def metrics():
    cola_close_prices = list(cola.get('Adj Close'))

    n = len(cola_close_prices)

    # Part A
    # the std of cola is divided by its mean, then multiplied by 100 to standardize it to a percentage
    volatility = np.std(cola_close_prices) / np.mean(cola_close_prices) * 100

    print(f"""a)  The volatility of Coca Cola is {volatility}%. This value represents the standard deviation of the
    stocks annualised return. It essentially represents how quickly the prices, and in turn, the the returns
    fluctuate over a period of time.\n\n""")

    # Part B
    cola_daily_returns = [(cola_close_prices[i] - cola_open_prices[i]) / cola_open_prices[i] * 100 for i in range(len(cola_close_prices) - 1)]
    cola_daily_returns.sort()

    historic_var = np.percentile(cola_daily_returns, 5, method='lower')

    print(f"""b)  The VAR of {historic_var} is essentially saying that there's a 95% chance that I won't lose more than
    {abs(historic_var)} for my investment on any given day. The VaR or Value At Risk is a statistic that is great for risk
    management because it is used to predict the greatest possible losses over a given period of time. Although volatility
    is used in risk management, it does not account for the direction of the stock's movement, only the movement itself.
    The VaR takes into account the momentum and direction of the stock.\n\n""")

    #Part C
    trading_days = 252

    expected_cola_return = (cola_close_prices[-1] - cola_open_prices[0]) / cola_open_prices[0] * 100

    risk_free_rate = 0.0428 * 100
    sd_cola_returns = np.std(cola_daily_returns)

    sharpe_ratio = (expected_cola_return - risk_free_rate) / sd_cola_returns

    print(f"""c)  The sharpe ratio, whose risk free rate is calculated from the Treasury's current interest rates, is {sharpe_ratio}.
    In essence, this ratio divide's the excess returns of a portfolio or stock by its volatility to obtain the risk to reward
    ratio. In any case a higher sharpe ratio is better as it indicates a better return for a lesser risk. Coca Cola's sharpe ratio is
    very good by all metrics which indicate that it has great returns for its level of risk and volatility.\n\n""")

    #Part D
    mar = 4.428 
    num_observations = len(cola_daily_returns)

    cola_daily_returns_mar = [(daily_return - mar) for daily_return in cola_daily_returns]

    negative_squares = [daily_return**2 for daily_return in cola_daily_returns_mar if daily_return < 0]
    negative_squares_sum = sum(negative_squares)

    downside_deviation = np.sqrt(negative_squares_sum / len(negative_squares))

    print(f"""d)  The downside deviation is {downside_deviation}. This metric is very important when it comes to an investors risk tolerance
    because it measures to what extent a certain investment can fall short of a minimal acceptable return, which in this case is the interest
    rate of the Treasury Bill. It's calculations specifically focus on the negative returns in the historic data and calculates a standard
    deviation from there. A normal standard deviation wouldn't give as good of a picture of downside risk as this method.\n\n""")

    #Part E
    max_drawdown = (min(cola_close_prices) - max(cola_close_prices)) / max(cola_close_prices)

    print(f"""e)  The max drawdown of this stock is {max_drawdown}. It is essentially the maximum loss from a peak to trough in a portfolio or
    stock. It is effectively looking for the greatest movement from a high point to a low point in a stocks history in order to get a better
    of its bigger swings. Because it only measures the maximum drawdown of the stock, it cannot determine the time it takes for the stock to recover
    from the drawdown.\n\n""")
    


def capm():
    print("TODO")
    


if __name__ == "__main__":
    print("Statistics:\n")
    statistics()
    print("Metrics:\n")
    metrics()
    print("Capm:\n")