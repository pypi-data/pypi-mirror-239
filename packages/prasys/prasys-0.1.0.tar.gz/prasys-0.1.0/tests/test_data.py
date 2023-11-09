import pytest

from prasys.data import Client, Data, Portfolio, load_client_from_yaml


def test_load_client_from_yaml(yaml_file_path):
    # Define the expected client name and attributes that are known in the YAML file
    expected_client_name = "Test Client"
    expected_year = 2020
    expected_portfolio_groups = [
        Portfolio(portfolio="Portfolio 1", benchmark="Benchmark 1", target="Target 1"),
        Portfolio(portfolio="Portfolio 2", benchmark="Benchmark 2", target="Target 2"),
    ]

    # Call the function with the known client name
    client = load_client_from_yaml(yaml_file_path, expected_client_name)

    # Assert that the returned Client object has the expected attributes
    assert client.name == expected_client_name
    assert client.year == expected_year
    assert client.portfolio_groups == expected_portfolio_groups


def test_load_client_from_yaml_raises_error(yaml_file_path):
    client_name = "Error Client"
    with pytest.raises(ValueError, match=f"Client with name {client_name} not found."):
        load_client_from_yaml(yaml_file_path, client_name)


def test_data_invalid_extension(csv_file_path_factory):
    csv_file_path = csv_file_path_factory()
    csv_file_path = csv_file_path.replace(".csv", ".txt")
    client = Client(name="Test Client", year=2020)
    with pytest.raises(ValueError, match="Data must be in .csv format"):
        Data(path=csv_file_path, client=client)


def test_data_invalid_directory(csv_file_path_factory):
    csv_file_path = csv_file_path_factory()
    csv_file_path = csv_file_path.replace("./data/", "./other/")
    client = Client(name="Test Client", year=2020)
    with pytest.raises(ValueError, match="Data must be in ./data/ directory"):
        Data(path=csv_file_path, client=client)


def test_no_date_error(csv_file_path_factory):
    csv_file_path = csv_file_path_factory(date_column=False)
    client = Client(name="Test Client", year=2020)
    with pytest.raises(ValueError, match="Data must contain a 'Date' column"):
        Data(path=csv_file_path, client=client)


def test_data_client_name(csv_file_path_factory):
    csv_file_path = csv_file_path_factory()
    client = Client(name="Test Client", year=2020)
    data = Data(path=csv_file_path, client=client)
    assert data.client_name == "Test Client"


def test_data_client_year(csv_file_path_factory):
    csv_file_path = csv_file_path_factory()
    client = Client(name="Test Client", year=2020)
    data = Data(path=csv_file_path, client=client)
    assert data.client_year == 2020
