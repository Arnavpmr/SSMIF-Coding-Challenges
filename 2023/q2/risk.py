import pandas as pd
import numpy as np


class CompareMetrics():

    def __init__(self, portfolio='sp500prices.pkl'):
        self.portfolio = pd.read_pickle(portfolio)
        self.myMetric = self.__my_metric()
        self.sharpeRatio = self.__sharpe_ratio()
        self.compareMetrics = self.__compare_metrics()
        self.correlationCoefficient = self.__get_correlation_coefficient()


    """ Part 1: Define your metric """
    # TODO

    def __my_metric(self, period=1, risk_free_rate=0.0525) -> float:
        return self.__my_metric_dateframe(period, risk_free_rate).mean()


    def __my_metric_dateframe(self, period=1, risk_free_rate=0.0525) -> float:
      num_days = 252 / period

      # This computes the average daily returns
      avg_daily_returns = self.portfolio.pct_change().mean()

      # The daily risk-free rate (assuming 5.72% us treasury bond annual yield 2022)
      daily_risk_free_rate = risk_free_rate / num_days

      # Excess returns are computed
      excess_returns = avg_daily_returns - daily_risk_free_rate

      # Compute downside deviation
      downside_returns = self.portfolio.pct_change()[self.portfolio.pct_change() < 0]
      downside_deviation = np.sqrt((downside_returns ** 2).mean())

      # Compute Sterling Ratio
      sterling_ratio = (excess_returns.mean() * period) / downside_deviation

      # return the mean of the sterling ratios of all the assets from the data frame
      return sterling_ratio


    """ Part 2: Define the Sharpe Ratio """
    # TODO

    def __sharpe_ratio(self, period=1, risk_free_rate=0.0525) -> float:
      return self.__sharpe_ratio_dataframe(period, risk_free_rate).mean()


    def __sharpe_ratio_dataframe(self, period=1, risk_free_rate=0.0525) -> float:
      num_days = 252 / period

      # Calculate daily returns which is a new data frame which represents the percent change of each asset daily
      daily_returns = self.portfolio.pct_change()

      # Calculate the annualized mean and standard deviation of those daily returns
      mean_return = daily_returns.mean() * num_days
      std_dev = daily_returns.std() * np.sqrt(num_days)

      # Calculate the Sharpe Ratio from the previously calculated values
      sharpe_ratio = (mean_return - risk_free_rate) / std_dev

      return sharpe_ratio


    """ Part 3: Evaluate Metric Correlation """

    def __compare_metrics(self) -> pd.DataFrame:

      # Construct a dataframe from those 2 columns
      df = pd.DataFrame({'Sharpe Ratio': list(self.__sharpe_ratio_dataframe().values[1:20]), 'Sterling Ratio': list(self.__my_metric_dateframe().values[1:20])})
      
      return df


    def __get_correlation_coefficient(self) -> float:
      return self.compareMetrics['Sterling Ratio'].corr(self.compareMetrics['Sharpe Ratio'])



if __name__ == '__main__':

    sp500 = CompareMetrics()
    # TODO: enter the name of the metric you chose
    myMetric = "Sterling Ratio"

    print("1. " + myMetric + " of the portfolio is: " + str(sp500.myMetric))
    print("2. Sharpe Ratio of the portfolio is: " + str(sp500.sharpeRatio))
    print("3. Metric comparison is: " + '\n' + str(sp500.compareMetrics))
    print("4. Correlation Coefficient between " + myMetric +
          " and Sharpe Ratio is: " + str(sp500.correlationCoefficient))