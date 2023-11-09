from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import pandas as pd
import yaml


def load_client_from_yaml(file_path: str, client_name: str) -> Client:
    """Loads the client data from the YAML file and returns a Client object.

    Parameters
    ----------
    file_path : str
        Path to the client YAML file.
    client_name : str
        Name of the client to load from the file.

    Returns
    -------
    Client
        The client object.

    Raises
    ------
    ValueError
        If the client name is not found in the YAML file.
    """
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
        for client_config in config["clients"]:
            if client_config["name"] == client_name:
                portfolio_groups = [
                    Portfolio(**pg) for pg in client_config["portfolio_groups"]
                ]
                return Client(
                    name=client_config["name"],
                    year=client_config["year"],
                    portfolio_groups=portfolio_groups,
                )
        raise ValueError(f"Client with name {client_name} not found.")


@dataclass
class Portfolio:
    portfolio: str
    benchmark: Optional[str] = None
    target: Optional[str] = None


@dataclass
class Client:
    name: str
    year: int
    portfolio_groups: List[Portfolio] = field(default_factory=list)


class Data:
    def __init__(self, path: str, client: Client) -> Data:
        self.validate_path(path)
        self.data = self.load_data(path)
        self.client_name = client.name
        self.client_year = client.year

    @staticmethod
    def validate_path(path: str) -> None:
        file_path = Path(path)
        if not file_path.suffix == ".csv":
            raise ValueError("Data must be in .csv format")
        if not file_path.parent == Path("./data"):
            raise ValueError("Data must be in ./data/ directory")

    @staticmethod
    def validate_columns(data: pd.DataFrame, required_columns: list) -> None:
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Data must contain a '{col}' column")

    @staticmethod
    def load_data(path: str) -> pd.DataFrame:
        data = pd.read_csv(path)

        # Validate the 'Date' column exists
        Data.validate_columns(data, required_columns=["Date"])

        # Convert the 'Date' column to datetime
        data["Date"] = pd.to_datetime(data["Date"])
        data.set_index("Date", inplace=True)
        return data
