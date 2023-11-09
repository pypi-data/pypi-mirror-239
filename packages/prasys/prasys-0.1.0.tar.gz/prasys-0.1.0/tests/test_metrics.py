from unittest.mock import Mock

import numpy as np
import pandas as pd
import pytest

from prasys.metrics import Metrics


# Test if the object is correctly instantiated with required attributes
def test_init(metrics):
    assert hasattr(metrics, "data")
    assert hasattr(metrics, "portfolio_groups")
    assert hasattr(metrics, "default_relative_benchmark")
    assert hasattr(metrics, "rolling_periods")


@pytest.mark.parametrize("mock_data", [6], indirect=True)
def test_init_with_short_data(mock_data, mock_client):
    with pytest.warns(UserWarning, match="Skipping calculations for portfolio group"):
        Metrics(mock_data, mock_client, "benchmark")


# Test if dynamically created attributes are correctly set.
def test_dynamic_attributes(metrics):
    assert hasattr(metrics, "portfolio_a")
    assert hasattr(metrics, "portfolio_a_returns")
    assert hasattr(metrics, "portfolio_a_risk")
    assert hasattr(metrics, "portfolio_a_rel_returns")
    assert hasattr(metrics, "portfolio_a_cumulative_returns")


# Test if portfolio groups are correctly defined.
def test_define_portfolio_groups(metrics, mock_portfolio):
    metrics.define_portfolio_groups([mock_portfolio])
    assert metrics.portfolio_groups == [mock_portfolio]


# Test if it returns the correct grouped data.
def test_group_data(metrics):
    grouped_data = metrics.group_data()
    assert "Portfolio_A" in grouped_data
    assert "portfolio" in grouped_data["Portfolio_A"]
    assert "benchmark" in grouped_data["Portfolio_A"]
    assert "target" in grouped_data["Portfolio_A"]


# Test if it returns the correct group data.
def test_set_group(metrics, mock_portfolio):
    group_data = metrics.set_group(mock_portfolio)
    assert "portfolio" in group_data
    assert "benchmark" in group_data
    assert "target" in group_data


@pytest.mark.parametrize("mock_data", [6], indirect=True)
def test_set_group_returns_none_for_insufficient_data(metrics, mock_portfolio):
    with pytest.warns(UserWarning, match="Insufficient data for portfolio"):
        result = metrics.set_group(mock_portfolio)
    assert result is None


# Test KeyError exceptions for missing portfolio, benchmark, or target.
def test_set_group_key_error(metrics):
    mock_portfolio = Mock()
    mock_portfolio.portfolio = "NonExistent"
    with pytest.raises(KeyError):
        metrics.set_group(mock_portfolio)


def test_non_existent_benchmark_error(metrics, mock_data):
    group_data = {
        "portfolio": mock_data.data["Portfolio_A"],
        "benchmark": mock_data.data["Benchmark_A"],
        "target": mock_data.data["Target_A"],
    }
    metrics.calculate_group_returns(group_data)
    group_return_data = {
        "portfolio": metrics.portfolio_a_returns["portfolio"],
        "benchmark": metrics.portfolio_a_returns["benchmark"],
        "target": metrics.portfolio_a_returns["target"],
    }

    with pytest.raises(KeyError):
        metrics.calculate_relative_returns(
            group_data, group_return_data, "non_existent_benchmark"
        )


# Test if rolling periods are correctly set based on data length.
# Parameterize the mock_data fixture to provide different lengths for the time period
@pytest.mark.parametrize("mock_data", [12], indirect=True)
def test_set_periods_one_year(metrics, mock_data):
    # Use the generated mock data for Portfolio_A
    group_data = {"portfolio": mock_data.data["Portfolio_A"]}

    # Call the set_periods method
    metrics.set_periods(group_data, "portfolio")

    # Assert the rolling_periods based on the length of the generated data
    assert metrics.rolling_periods == {"1Y": 12}


@pytest.mark.parametrize("mock_data", [60], indirect=True)
def test_set_periods_five_year(metrics, mock_data):
    # Use the generated mock data for Portfolio_A
    group_data = {"portfolio": mock_data.data["Portfolio_A"]}

    # Call the set_periods method
    metrics.set_periods(group_data, "portfolio")

    # Assert the rolling_periods based on the length of the generated data
    assert metrics.rolling_periods == {"1Y": 12, "2Y": 24, "3Y": 36, "4Y": 48, "5Y": 60}


def test_calculate_annualized_returns_df(metrics):
    data = pd.Series(
        [
            0.01235,
            0.02535,
            -0.01123,
            0.005456,
            0.00312354,
            0.0042134,
            0.0021234,
            0.001124,
            0.002454,
            0.0030215,
            0.0044532,
            0.0051245,
        ]
    )
    result = metrics.calculate_annualized_returns_df(data, len(data))

    # Calculate the expected annualized return
    expected_annual_return = (np.prod([1 + x for x in data]) ** (12 / len(data))) - 1
    assert np.isclose(result.iloc[-1], expected_annual_return, atol=1e-8)


def test_calculate_annualized_returns_df_with_zero(metrics):
    data = pd.Series([0, 0, 0])
    result = metrics.calculate_annualized_returns_df(data, 3)
    assert result.iloc[-1] == 0


def test_calculate_annualized_std_dev(metrics):
    data = pd.Series([0.01, 0.02, -0.01])
    result = metrics.calculate_annualized_std_dev(data, 3)
    monthly_std_dev = np.std([0.01, 0.02, -0.01], ddof=1)  # Sample standard deviation
    expected_annual_std_dev = monthly_std_dev * np.sqrt(12)
    assert np.isclose(result.iloc[-1], expected_annual_std_dev, atol=1e-8)


# Test if these methods return the correct calculated data for each group.
@pytest.mark.parametrize("mock_data", [12], indirect=True)
def test_calculate_group_returns(metrics, mock_data):
    group_data = {"portfolio": mock_data.data["Portfolio_A"]}
    result = metrics.calculate_group_returns(group_data)
    assert "portfolio" in result
    assert "1Y" in result["portfolio"]


@pytest.mark.parametrize("mock_data", [12], indirect=True)
def test_calculate_group_std_dev(metrics, mock_data):
    group_data = {"portfolio": mock_data.data["Portfolio_A"]}
    result = metrics.calculate_group_std_dev(group_data)
    assert "portfolio" in result
    assert "1Y" in result["portfolio"]


@pytest.mark.parametrize("mock_data", [12], indirect=True)
def test_calculate_relative_returns(metrics, mock_data):
    group_data = {
        "portfolio": mock_data.data["Portfolio_A"],
        "benchmark": mock_data.data["Benchmark_A"],
        "target": mock_data.data["Target_A"],
    }
    metrics.calculate_group_returns(group_data)
    group_return_data = {
        "portfolio": metrics.portfolio_a_returns["portfolio"],
        "benchmark": metrics.portfolio_a_returns["benchmark"],
        "target": metrics.portfolio_a_returns["target"],
    }
    result = metrics.calculate_relative_returns(
        group_data, group_return_data, "benchmark"
    )

    assert "portfolio" in result
    assert "benchmark" in result
    assert "target" in result
    assert "1Y" in result["portfolio"]
    assert "1Y" in result["target"]


@pytest.mark.parametrize("mock_data", [36], indirect=True)
def test_calculate_relative_returns_calculations(metrics, mock_data):
    group_data = {
        "portfolio": mock_data.data["Portfolio_A"],
        "benchmark": mock_data.data["Benchmark_A"],
        "target": mock_data.data["Target_A"],
    }
    metrics.calculate_group_returns(group_data)
    group_return_data = {
        "portfolio": metrics.portfolio_a_returns["portfolio"],
        "benchmark": metrics.portfolio_a_returns["benchmark"],
        "target": metrics.portfolio_a_returns["target"],
    }
    result = metrics.calculate_relative_returns(
        group_data, group_return_data, "benchmark"
    )

    for period in ["1Y", "2Y", "3Y"]:
        # Get the last value of the Series for the current period
        last_portfolio_return = group_return_data["portfolio"].get(period, None)
        last_benchmark_return = group_return_data["benchmark"].get(period, None)

        if last_portfolio_return is not None and last_benchmark_return is not None:
            last_portfolio_return = last_portfolio_return.iloc[-1]
            last_benchmark_return = last_benchmark_return.iloc[-1]

            last_rel_return = result["portfolio"].get(period, None)
            if last_rel_return is not None:
                last_rel_return = last_rel_return.iloc[-1]

                # Check if portfolio outperforms benchmark, relative should be positive
                if last_portfolio_return > last_benchmark_return:
                    assert last_rel_return > 0

                # The relative should be the portfolio return minus the benchmark return
                assert last_rel_return == last_portfolio_return - last_benchmark_return


@pytest.mark.parametrize("mock_data", [19], indirect=True)
def test_calculate_cumulative_returns(metrics, mock_data):
    group_data = {
        "portfolio": mock_data.data["Portfolio_A"],
        "benchmark": mock_data.data["Benchmark_A"],
        "target": mock_data.data["Target_A"],
    }
    result = metrics.calculate_cumulative_returns(group_data)

    # Check structure of the result
    assert "portfolio" in result
    assert "benchmark" in result
    assert "target" in result
    assert len(result["portfolio"]) == 19


@pytest.mark.parametrize("mock_data", [19], indirect=True)
def test_calculate_cumulative_returns_calculation(metrics, mock_data):
    group_data = {
        "portfolio": mock_data.data["Portfolio_A"],
        "benchmark": mock_data.data["Benchmark_A"],
        "target": mock_data.data["Target_A"],
    }
    result = metrics.calculate_cumulative_returns(group_data)

    # Check the first value is the same as in the original series
    assert np.isclose(
        result["portfolio"].iloc[0], mock_data.data["Portfolio_A"].iloc[0], atol=1e-8
    )

    # Manually calculate cumulative returns for a small set of values
    if len(mock_data.data["Portfolio_A"]) >= 3:  # Assuming at least 3 data points
        manual_cumulative_return = (
            (1 + mock_data.data["Portfolio_A"]).cumprod() - 1
        ).iloc[-1]
        assert np.isclose(
            result["portfolio"].iloc[-1], manual_cumulative_return, atol=1e-8
        )
