from __future__ import annotations

import warnings
from typing import Dict, List

import pandas as pd

from prasys.data import Client, Data, Portfolio, load_client_from_yaml


class Metrics:
    def __init__(self, data: Data, client: Client, relative_benchmark: str) -> Metrics:
        self.data = data.data
        self.define_portfolio_groups(client.portfolio_groups)
        self.default_relative_benchmark = relative_benchmark
        self.rolling_periods = {
            "1Y": 12,
            "2Y": 24,
            "3Y": 36,
            "4Y": 48,
            "5Y": 60,
            "6Y": 72,
            "7Y": 84,
            "10Y": 120,
            "15Y": 180,
            "20Y": 240,
        }
        # Create attributes dynamically for each portfolio group
        for group in self.portfolio_groups:
            attribute_name = group.portfolio.replace(" ", "_").lower()

            group_data = self.set_group(group)

            if group_data is None:
                warnings.warn(
                    f"Skipping calculations for portfolio group '{group.portfolio}' due to insufficient data."
                )
                continue

            setattr(self, f"{attribute_name}", group_data)

            # Determine the relative_benchmark for this specific group
            relative_benchmark_for_group = self.default_relative_benchmark

            # Check if the default relative_benchmark exists in the portfolio data
            if getattr(group, self.default_relative_benchmark) is None:
                # If not, switch to the other option
                relative_benchmark_for_group = (
                    "target"
                    if self.default_relative_benchmark == "benchmark"
                    else "benchmark"
                )

            setattr(
                self,
                f"{attribute_name}_returns",
                self.calculate_group_returns(getattr(self, f"{attribute_name}")),
            )
            setattr(
                self,
                f"{attribute_name}_risk",
                self.calculate_group_std_dev(getattr(self, f"{attribute_name}")),
            )
            setattr(
                self,
                f"{attribute_name}_rel_returns",
                self.calculate_relative_returns(
                    getattr(self, f"{attribute_name}"),
                    getattr(self, f"{attribute_name}_returns"),
                    relative_benchmark_for_group,
                ),
            )
            setattr(
                self,
                f"{attribute_name}_cumulative_returns",
                self.calculate_cumulative_returns(getattr(self, f"{attribute_name}")),
            )

    def define_portfolio_groups(self, portfolio_definitions: List[Portfolio]) -> None:
        """Defines the portfolio groups.

        Parameters
        ----------
        portfolio_definitions : List[Portfolio]
            The portfolio definitions.
        """
        self.portfolio_groups = portfolio_definitions

    def group_data(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Groups the data by portfolio.

        Returns
        -------
        Dict[str, Dict[str, pd.DataFrame]]
            The grouped data.
        """
        grouped_data = {}
        for group in self.portfolio_groups:
            portfolio_data = self.data[group.portfolio]
            target_data = self.data[group.target]
            benchmark_data = self.data[group.benchmark]
            grouped_data[group.portfolio] = {
                "portfolio": portfolio_data,
                "target": target_data,
                "benchmark": benchmark_data,
            }
        return grouped_data

    def set_group(self, group: Portfolio) -> Dict[str, pd.DataFrame]:
        """Sets the data for a portfolio group.

        Parameters
        ----------
        group : Portfolio
            The portfolio group.

        Returns
        -------
        Dict[str, pd.DataFrame]
            The portfolio group data.

        Raises
        ------
        KeyError
            If portfolio name not found in the portfolio group.
        KeyError
            If benchmark name not found in the portfolio group.
        KeyError
            If target name not found in the portfolio group.
        """
        try:
            portfolio_data = self.data[group.portfolio].dropna()
        except KeyError:
            raise KeyError(
                f"Portfolio name '{group.portfolio}' not found in the data file."
            )

        # Check for sufficient data
        if len(portfolio_data) < 12:  # Assuming 12 is the minimum for a 1Y calculation
            warnings.warn(
                f"Insufficient data for portfolio '{group.portfolio}'. Minimum 12 data points required for 1Y calculations."
            )
            return None

        group_data = {
            "portfolio": portfolio_data,
        }

        # Include benchmark and target data only if it's present in the group
        if group.benchmark is not None:
            try:
                benchmark_data = self.data[group.benchmark]
                # Align benchmark data with portfolio data
                benchmark_data = benchmark_data.reindex(portfolio_data.index)
                group_data["benchmark"] = benchmark_data
            except KeyError:
                raise KeyError(
                    f"Benchmark name '{group.benchmark}' not found in the data file."
                )

        if group.target is not None:
            try:
                target_data = self.data[group.target]
                # Align target data with portfolio data
                target_data = target_data.reindex(portfolio_data.index)
                group_data["target"] = target_data
            except KeyError:
                raise KeyError(
                    f"Target name '{group.target}' not found in the data file."
                )

        return group_data

    def set_periods(self, group_data: Dict[str, pd.DataFrame], key_name: str) -> None:
        """Sets the rolling periods for a portfolio group.

        Parameters
        ----------
        group_data : Dict[str, pd.DataFrame]
            The portfolio group data.
        key_name : str
            The name of the portfolio.
        """
        if group_data.get(key_name) is None:
            warnings.warn(f"Data for {key_name} is not available.")
            return

        selected_column = group_data[key_name]
        selected_column = selected_column.dropna()
        data_len = len(selected_column)

        max_period = min(240, data_len)  # Setting an upper bound for the period

        # Define the periods with their corresponding labels
        all_periods = [
            ("1Y", 12),
            ("2Y", 24),
            ("3Y", 36),
            ("4Y", 48),
            ("5Y", 60),
            ("6Y", 72),
            ("7Y", 84),
            ("10Y", 120),
            ("15Y", 180),
            ("20Y", 240),
        ]

        # Only include periods that are within the range of the data length
        periods = {label: value for label, value in all_periods if value <= max_period}

        self.rolling_periods = periods

    def calculate_annualized_returns_df(
        self, data: Dict[str, pd.DataFrame], period: int
    ) -> pd.Series:
        """Calculates the annualized returns of a dataframe.

        Parameters
        ----------
        data : Dict[str, pd.DataFrame]
            The portfolio group data.
        period : int
            The period to calculate the annualized returns for.

        Returns
        -------
        pd.Series
            The annualized returns of the dataframe.
        """
        return data.rolling(window=period).apply(
            lambda x: (1 + x).prod() ** (1 / (period / 12)) - 1
        )

    def calculate_annualized_std_dev(
        self, data: Dict[str, pd.DataFrame], period: int
    ) -> pd.Series:
        """Calculates the annualized standard deviation of a dataframe.

        Parameters
        ----------
        data : Dict[str, pd.DataFrame]
            The portfolio group data.
        period : int
            The period to calculate the annualized standard deviation for.

        Returns
        -------
        pd.Series
            The annualized standard deviation of the dataframe.
        """
        return data.rolling(window=period).std() * (12**0.5)

    def calculate_group_returns(self, group_data: Dict[str, pd.DataFrame]) -> Dict:
        """Calculates the annualized returns of a portfolio group.

        Parameters
        ----------
        group_data : Dict[str, pd.DataFrame]
            The portfolio group data.

        Returns
        -------
        Dict
            The annualized returns of each portfolio group.
        """
        all_annualized_returns = {}
        for portfolio_name, portfolio_data in group_data.items():
            self.set_periods(group_data, portfolio_name)
            annualized_returns = {}
            for period, window_size in self.rolling_periods.items():
                if len(portfolio_data) >= window_size:
                    annualized_returns[period] = self.calculate_annualized_returns_df(
                        portfolio_data, window_size
                    )
            all_annualized_returns[portfolio_name] = annualized_returns
        return all_annualized_returns

    def calculate_group_std_dev(self, group_data: Dict[str, pd.DataFrame]) -> Dict:
        """Calculates the standard deviation of a portfolio group.

        Parameters
        ----------
        group_data : Dict[str, pd.DataFrame]
            The portfolio group data.

        Returns
        -------
        Dict
            The standard deviation of each portfolio group.
        """
        all_annualized_returns = {}
        for portfolio_name, portfolio_data in group_data.items():
            self.set_periods(group_data, portfolio_name)
            annualized_returns = {}
            for period, window_size in self.rolling_periods.items():
                annualized_returns[period] = self.calculate_annualized_std_dev(
                    portfolio_data, window_size
                )
            all_annualized_returns[portfolio_name] = annualized_returns
        return all_annualized_returns

    def calculate_relative_returns(
        self,
        group_data: Dict[str, pd.DataFrame],
        group_return_data: Dict[str, pd.DataFrame],
        benchmark_name: str,
    ) -> Dict[str, Dict[str, pd.Series]]:
        """Calculates the relative returns of a portfolio group.

        Parameters
        ----------
        group_data : Dict[str, pd.DataFrame]
            The portfolio group data.
        group_return_data : Dict[str, pd.DataFrame]
            The portfolio group return data.
        benchmark_name : str
            The name of the benchmark.

        Returns
        -------
        Dict[str, Dict[str, pd.Series]]
            The relative returns of each portfolio group.
        """
        all_relative_returns = {}
        for portfolio_name, portfolio_data in group_return_data.items():
            self.set_periods(group_data, portfolio_name)
            relative_returns = {}
            for period, window_size in self.rolling_periods.items():
                relative_returns[period] = (
                    group_return_data[portfolio_name][period]
                    - group_return_data[benchmark_name][period]
                )
            all_relative_returns[portfolio_name] = relative_returns
        return all_relative_returns

    def calculate_cumulative_returns(self, group_data: Dict[str, pd.DataFrame]) -> Dict:
        """Calculates the cumulative returns of a portfolio group.

        Parameters
        ----------
        group_data : Dict[str, pd.DataFrame]
            The portfolio group data.

        Returns
        -------
        Dict
            The cumulative returns of each portfolio group.
        """
        cumulative_returns = {}
        for portfolio_name, portfolio_data in group_data.items():
            cumulative_returns[portfolio_name] = (1 + portfolio_data).cumprod() - 1
        return cumulative_returns


if __name__ == "__main__":  # pragma: no cover
    path = "./data/prasa_managers.csv"
    client_name = "PRASA_managers"
    client = load_client_from_yaml("clients.yaml", client_name)
    data = Data(path, client)
    relative_benchmark = "benchmark"
    metrics = Metrics(data, client, relative_benchmark)
