from __future__ import annotations

from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter

from prasys.metrics import Metrics, Portfolio


class Plots:
    def __init__(self, metrics: Metrics) -> Plots:
        self.metrics = metrics

    @staticmethod
    def percentage_format(x, pos):
        """
        Custom formatter function to format y-axis ticks as percentage.
        """
        return "{:.1f}%".format(x * 100)

    def plot_single_data(
        self,
        return_data: Metrics,
        sub_portfolio: str,
        period: str,
        title: str,
        y_min: float = 0,
        show_risk: bool = False,
        risk_data: Metrics = None,
    ) -> plt.Figure:
        """Plots a single portfolio's return data for the specified period.

        Parameters
        ----------
        return_data : Metrics
            A dictionary containing return data.
        sub_portfolio : str
            The sub-portfolio name to plot.
        period : str
            The period to plot.
        title : str
            The title for the plot.
        y_min : float, optional
            Min value of y axis, by default 0
        show_risk : bool, optional
            Displays the standard deviation of return, by default False
        risk_data : Metrics, optional
            A dictionary containing the risk data, by default None

        Returns
        -------
        plt.Figure
            The figure object of the plot.
        """
        # Check if the specified period exists in the return data
        if period not in return_data[sub_portfolio]:
            print(f"Skipped {title} for period {period} it does not exist in the data.")
            return None

        data = return_data[sub_portfolio][period]
        data = data.dropna()
        risks = None
        if show_risk:
            risks = risk_data[sub_portfolio][period]
            risks = risks.dropna()

        sns.set_style("whitegrid")
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title(f"{title} - {period} Rolling Returns")
        ax.set_xlabel("Date")
        formatter = FuncFormatter(self.percentage_format)
        ax.set_ylabel("Returns (%)")
        ax.yaxis.set_major_formatter(formatter)
        ax.plot(data.index, data.values, label="Annualized Return")
        if show_risk and risks is not None:
            upper_bound = data + risks
            lower_bound = data - risks
            ax.fill_between(
                data.index,
                lower_bound,
                upper_bound,
                alpha=0.2,
                label="Risk (Standard Deviation)",
            )
        ax.set_ylim(ymin=y_min)  # Set the minimum value for the y-axis
        plt.legend()
        plt.show()
        return fig

    def plot_grouped_data(
        self, return_data: Metrics, period: str, title: str
    ) -> plt.Figure:
        """Plots a grouped portfolio's return data for the specified period.

        Parameters
        ----------
        return_data : Metrics
            A dictionary containing return data.
        period : str
            The period to plot.
        title : str
            The title for the plot.

        Returns
        -------
        plt.Figure
            The figure object of the plot.
        """
        # Check if the specified period exists in the return data
        for portfolio, data in return_data.items():
            if period not in data:
                print(
                    f"Skipped {title} for period {period} it does not exist in the data"
                )
                return None

        # Get the portfolio data as the reference for alignment
        portfolio_data = return_data["portfolio"][period].dropna()

        sns.set_style("whitegrid")
        sns.set_palette("tab10")
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title(f"{title} - {period} Rolling Returns")
        ax.set_xlabel("Date")
        formatter = FuncFormatter(self.percentage_format)
        ax.set_ylabel("Returns (%)")
        ax.yaxis.set_major_formatter(formatter)

        for portfolio, data in return_data.items():
            # Select the data for the given period
            data_period = data[period]

            # Match the index with portfolio_data (including NaN values)
            aligned_data = data_period.reindex(portfolio_data.index)

            linestyle = "-"
            if portfolio == "target":
                linestyle = ":"
            elif portfolio == "benchmark":
                linestyle = "--"

            ax.plot(aligned_data, label=portfolio, linestyle=linestyle)

        ax.legend()
        plt.show()
        return fig

    def relative_barplot(
        self, return_data: Dict, period: str, title: str
    ) -> plt.Figure:
        """Plots a barplot of the relative returns for the specified period.

        Parameters
        ----------
        return_data : Dict
            Dictionary containing return data.
        period : str
            The period for the relative returns.
        title : str
            The title for the plot.

        Returns
        -------
        plt.Figure
            The figure object of the plot.
        """
        # Check if the specified period exists in the return data
        for portfolio, data in return_data.items():
            if period not in data:
                print(
                    f"Skipped {title} for period {period} it does not exist in the data"
                )
                return None

        sns.set_style("whitegrid")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_title(f"{title} - {period} Relative Returns")
        ax.set_xlabel("Date")
        formatter = FuncFormatter(self.percentage_format)
        ax.set_ylabel("Returns (%)")
        ax.yaxis.set_major_formatter(formatter)

        # Determine the width for the bars
        num_portfolios = len(return_data)
        width = 0.8 / num_portfolios

        # Collect positions and labels for x-axis
        positions = []
        labels = []

        # Plot the bars for each portfolio
        for i, (portfolio, data) in enumerate(return_data.items()):
            valid_data = data[period].dropna()  # Drop NaN values
            pos = np.arange(len(valid_data))
            ax.bar(pos + i * width, valid_data.values, width=width, label=portfolio)
            if i == 0:  # Collect positions and labels from the first portfolio
                positions = pos + width * (num_portfolios - 1) / 2
                labels = valid_data.index.strftime("%Y-%m-%d")

        # Determine the interval for x-axis ticks based on the number of dates
        max_ticks = 10
        interval = max(len(labels) // max_ticks, 1)
        selected_positions = positions[::interval]
        selected_labels = labels[::interval]

        # Adjust the x-axis ticks and labels
        ax.set_xticks(selected_positions)
        ax.set_xticklabels(selected_labels, rotation=45, ha="right")  # Rotate labels

        ax.legend()
        plt.tight_layout()  # Adjust layout to fit rotated labels
        plt.show()
        return fig

    def relative_horizon_barplot(
        self, return_data: Metrics, title: str, period=None
    ) -> plt.Figure:
        """Plots a horizontal barplot of the relative returns for the specified period.

        Parameters
        ----------
        return_data : Metrics
            A dictionary containing return data.
        title : str
            The title for the plot.
        period : _type_, optional
            The period to be plotted, by default None

        Returns
        -------
        plt.Figure
            The figure object of the plot.
        """
        sns.set_style("whitegrid")

        # Determine which periods to plot
        if period is None:
            periods = return_data[next(iter(return_data))].keys()
        else:
            periods = [period]

        # Prepare a DataFrame containing all the last values, grouped by period
        all_values = []
        for p in periods:
            for portfolio, data in return_data.items():
                last_value = data[p].dropna().iloc[-1]
                if last_value != 0:
                    all_values.append((portfolio, last_value, p))

        all_values_df = pd.DataFrame(
            all_values, columns=["Portfolio", "Returns", "Period"]
        )

        # Plot the horizontal bar plot using Seaborn
        fig = plt.figure(figsize=(12, 6))
        ax = sns.barplot(
            x="Returns",
            y="Portfolio",
            hue="Period",
            data=all_values_df,
            palette="tab10",
        )

        # Hide existing labels
        ax.set_xticklabels([])
        # ax.set_yticklabels([])

        ax.set_title(f"{title} - Relative Returns")
        ax.set_xlabel("Relative Returns (%)")
        # ax.set_ylabel("Portfolio")

        # Format y-axis percentage
        formatter = FuncFormatter(self.percentage_format)
        ax.xaxis.set_major_formatter(formatter)

        plt.tight_layout()
        plt.show()
        return fig

    def plot_cumulative_returns(self, return_data: Metrics, title: str) -> plt.Figure:
        """Plots the cumulative returns for the specified period.

        Parameters
        ----------
        return_data : Metrics
            A dictionary containing return data.
        title : str
            The title for the plot.

        Returns
        -------
        plt.Figure
            The figure object of the plot.
        """
        sns.set_style("whitegrid")
        sns.set_palette("tab10")
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title(f"{title} - Cumulative Returns")
        ax.set_xlabel("Date")
        formatter = FuncFormatter(self.percentage_format)
        ax.set_ylabel("Returns (%)")
        ax.yaxis.set_major_formatter(formatter)
        for portfolio, data in return_data.items():
            linestyle = "-"
            if portfolio == "target":
                linestyle = ":"
            elif portfolio == "benchmark":
                linestyle = "--"
            ax.plot(data, label=portfolio, linestyle=linestyle)
        ax.legend()
        plt.show()
        return fig

    def risk_return_scatterplot(
        self,
        data: Dict[str, Dict[str, pd.DataFrame]],
        period: str,
        last_value_only: bool = True,
    ) -> plt.Figure:
        """Plots a scatterplot of the risk and return for the specified period.

        Parameters
        ----------
        data : Dict[str, Dict[str, pd.DataFrame]]
            A dictionary containing risk and return data.
        period : str
            The period to be plotted.
        last_value_only : bool, optional
            Only plots the most recent data points, by default True

        Returns
        -------
        plt.Figure
            The figure object of the plot.
        """
        sns.set_style("whitegrid")
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title(f"{period} Risk-Return Scatterplot")
        formatter = FuncFormatter(self.percentage_format)
        ax.set_xlabel("Risk (%)")
        ax.xaxis.set_major_formatter(formatter)
        ax.set_ylabel("Returns (%)")
        ax.yaxis.set_major_formatter(formatter)
        marker_styles = {"portfolio": "o", "target": "*", "benchmark": "D"}

        colors = iter(sns.color_palette("tab10", len(data)))

        for portfolio_name, metrics in data.items():
            color = next(colors)  # Get the next color for this portfolio
            attribute_names = list(Portfolio.__annotations__.keys())
            for name in attribute_names:
                if name not in metrics["risk"] or name not in metrics["return"]:
                    # Skip this attribute if risk or return data is not available
                    continue
                # Check if the specified period exists in the risk and return data
                if (
                    period not in metrics["risk"][name]
                    or period not in metrics["return"][name]
                ):
                    print(
                        f"Skipped {portfolio_name} as period {period} does not exist in the data"
                    )
                    continue

                marker_style = marker_styles.get(name, "o")
                risk_data = metrics["risk"][name][period]
                return_data = metrics["return"][name][period]

                # Normalize dates to alpha values between 0.3 and 1
                alpha_values = (risk_data.index - risk_data.index.min()) / (
                    risk_data.index.max() - risk_data.index.min()
                )
                alpha_values = 0.7 * alpha_values + 0.3  # Scaling the alpha values
                alpha_values = pd.Series(
                    alpha_values, index=risk_data.index
                )  # Convert to a Series

                if last_value_only:
                    risk_data = risk_data.iloc[-1:]
                    return_data = return_data.iloc[-1:]
                    alpha_values = alpha_values.iloc[-1:]

                # Plot each point individually to assign different alpha values
                for i in range(len(risk_data)):
                    # Enlarge and add edge color for the last date value
                    marker_size = 100 if i == len(risk_data) - 1 else 50
                    edge_color = "black" if i == len(risk_data) - 1 else "none"

                    ax.scatter(
                        risk_data.iloc[i],
                        return_data.iloc[i],
                        label=f"{portfolio_name.title()} - {name.title()}"
                        if i == 0
                        else "",
                        alpha=alpha_values.iloc[i],
                        marker=marker_style,
                        color=color,
                        s=marker_size,  # Size of the marker
                        edgecolors=edge_color,  # Edge color of the marker
                        linewidths=1,  # Thickness of the edge
                    )

        ax.legend()
        plt.show()
        return fig

    def return_distribution(self, data: Dict[str, pd.DataFrame]) -> plt.Figure:
        """Plots a histogram of the monthly returns for each portfolio.

        Parameters
        ----------
        data : Dict[str, pd.DataFrame]
            A dictionary containing return data.

        Returns
        -------
        plt.Figure
            The figure object of the plot.
        """
        sns.set_style("whitegrid")
        num_portfolios = len(data)
        height_per_plot = 6
        total_height = num_portfolios * height_per_plot

        fig, axes = plt.subplots(num_portfolios, 1, figsize=(12, total_height))

        # If there's only one portfolio, axes won't be an array,
        # so we need to handle that case
        if num_portfolios == 1:
            axes = [axes]

        for ax, (portfolio_name, metrics) in zip(axes, data.items()):
            formatted_name = portfolio_name.replace("_", " ").title()
            ax.set_title(f"{formatted_name.title()} - Monthly Return Distribution")
            ax.set_xlabel("Monthly Returns (%)")
            formatter = FuncFormatter(self.percentage_format)
            ax.xaxis.set_major_formatter(formatter)
            ax.set_ylabel("Frequency")
            sns.histplot(
                metrics,
                ax=ax,
                kde=True,
            )
        plt.tight_layout()
        plt.show()
        return fig

    def stacked_return_distribution(
        self,
        return_data: dict,
        period: str = None,
        annualised: bool = False,
        column_wise: bool = False,
    ) -> plt.Figure:
        """Plots a stacked histogram of the returns for the specified period.

        Parameters
        ----------
        return_data : dict
            Dictionary containing return data.
        period : str, optional
            The period to be plotted, by default None
        annualised : bool, optional
            Should values be annualised, by default False
        column_wise : bool, optional
            Plots column wise, by default False

        Returns
        -------
        plt.Figure
            The figure object of the plot.
        """
        # Create an empty list to collect data for the DataFrame
        data_list = []

        # Iterate through each portfolio type (portfolio, target, benchmark)
        for portfolio_type, periods_data in return_data.items():
            if period not in periods_data:
                print(
                    f"Skipped {portfolio_type} for period {period} it does not exist in the data"
                )
                return None

            title = (
                return_data["portfolio"][period].name
                if annualised
                else return_data["portfolio"].name
            )

            # Extract the specific period's Series if annualised,
            # otherwise use periods_data directly
            series_data = periods_data[period] if annualised else periods_data

            # Convert Series to DataFrame
            period_data = series_data.reset_index()

            # Add the 'Portfolio' and 'Type' columns
            period_data["Portfolio"] = (
                period if annualised else return_data["portfolio"].name
            )
            period_data["Type"] = portfolio_type

            # Rename the value column to 'Value'
            period_data.rename(columns={series_data.name: "Value"}, inplace=True)

            # Append to the data list
            data_list.append(period_data)

        # Concatenate all the DataFrames into a single DataFrame
        df = pd.concat(data_list, ignore_index=True)

        # Plot using Seaborn's histplot
        sns.set_style("whitegrid")
        sns.set_palette("tab10")
        fig = plt.figure(figsize=(12, 8))
        if column_wise:
            g = sns.displot(
                data=df, x="Value", hue="Type", multiple="stack", col="Type"
            )

            # Apply percentage format to the x-axis of each subplot
            for ax in g.axes.flat:
                ax.xaxis.set_major_formatter(FuncFormatter(self.percentage_format))
                ax.set_xlabel("Returns (%)")

            # Iterate through the axes to set the titles
            for ax, title in zip(g.axes.flat, g.col_names):
                ax.set_title(
                    f"{title.title()} - {period} Annualised Returns"
                    if annualised
                    else title.title()
                )
        else:
            ax = sns.histplot(data=df, x="Value", hue="Type", multiple="stack")
            ax.set_title(
                f"{title} - {period} Annualised Returns" if annualised else title
            )
            formatter = FuncFormatter(self.percentage_format)
            ax.set_xlabel("Returns (%)")
            ax.xaxis.set_major_formatter(formatter)
            ax.set_ylabel("Frequency")

        plt.tight_layout()
        plt.show()
        return fig

    def boxplot(
        self, data: Dict[str, pd.DataFrame], separate_figures: bool = False
    ) -> List[plt.Figure]:
        """Creates a boxplot of the portfolio and the benchmark or target. Can
        be either as a single or seperate figures.

        Args:
            data (Dict[str, pd.DataFrame]): Dictionary containing return data.
            separate_figures (bool, optional): Create seperate figures for each group.
            Defaults to False.

        Returns:
            List[plt.Figure]: The figure object of the plot.
        """
        sns.set_style("whitegrid")
        sns.set_palette("tab10")

        figures = []  # To store the figures

        for portfolio_name, portfolio_data in data.items():
            if separate_figures:
                fig, ax = plt.subplots(
                    figsize=(12, 6)
                )  # Create a new figure for each portfolio
            else:
                fig, ax = plt.subplots(1, len(data), figsize=(12, 8), sharey=True)
                ax = ax.ravel()

            # Convert the dictionary into a DataFrame
            df_portfolio_data = pd.DataFrame.from_dict(portfolio_data)

            # Melt the data into long format for seaborn's boxplot
            melted_data = df_portfolio_data.melt()

            # Create the boxplot
            sns.boxplot(x="variable", y="value", data=melted_data, ax=ax)

            # Set the title, labels, and formatter
            formatted_name = portfolio_name.replace("_", " ").title()
            ax.set_title(f"{formatted_name} - Monthly Return Distribution")
            ax.set_xlabel("")
            ax.set_ylabel("Returns (%)")

            # Format y-axis percentage
            formatter = FuncFormatter(self.percentage_format)
            ax.yaxis.set_major_formatter(formatter)

            plt.tight_layout()
            plt.show()

            figures.append(fig)

        return figures
