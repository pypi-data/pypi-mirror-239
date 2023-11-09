# Performance and Risk Analysis

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The project is for calculating and plotting performance and risk analysis for a portfolio of assets.

## Installation

First, clone the repository:

git clone <https://github.com/PlainStack/performance_risk_analysis>

Then navigate to your project folder and install using conda:

conda env create -f environment.yml

## Usage

Create a clients.yaml file with the below structure:

clients:
  - name: name_of_client
  - year: year_of_analysis
  - portfolio_groups:
    - portfolio: portfolio_1
    - benchmark: benchmark_1
    - target: target_1

Add more clients and portfolio groups as required.

Choose which plots you want in the main.py file and run it.
