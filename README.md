# Mean-Variance Portfolio Optimization
The objective of this project is to determine an optimal portfolio of perpetual futures using [historical data](https://docs.ftx.com/#get-historical-prices) from FTX Markets API.

## Approach
The approach is to create a vector of weights from a portfolio of 'BTC-PERP', 'ETH-PERP', and 'SOL-PERP'.
Using mean-variance portfolio optimization, and hourly data from 1st June 2022 - 1st July 2022, a scatter plot is generated to visualize the Efficient Frontier.

## Clone the repository
To begin, start a terminal session and navigate to the directory you wish to clone this repository into. Run the following command:
```bash
git clone https://github.com/ngweikai/mean_var_pfl.git
```

After the repository has been cloned, navigate into the folder by running the command:
```bash
cd mean_var_pfl/
```

## Install dependencies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages (one by one):
```bash
pip install matplotlib
pip install numpy
pip install pandas
pip install pandas-datareader
```

## Adjust the script parameters (Optional)
Using an editor of your choice, open 'mean_var_opt.py' and change the following code snippet to your requirements:
```python
portfolio = ['BTC', 'ETH', 'SOL']
market_type = 'PERP'

# datetime params: (year, month, day, hour, minute, second)
start = dt(2022, 6, 1, 0, 0, 0)
end = dt(2022, 7, 1, 23, 0, 0)
```

You may also edit below code snippet and increase the number of simulations to get a more accurate Efficient Frontier:
```python
# portfolio simulations
sim_count = 100000
weights = []
returns = []
risks = []
sharpe = []
```

## Select output location and filename
Edit your desired filepath in below code snippet.

Example for Linux:
```python
msg = f'Optimal Weights: {output}'
file_path = '/path/to/directory/efficient_frontier.png'
```

Example for Windows:
```python
msg = f'Optimal Weights: {output}'
file_path = 'C:/Users/<user>/Desktop/efficient_frontier.png'
```

If you just edit file_path = 'efficient_frontier.png', a .png file would be generated at your present working directory.

## Run the script
After adjusting the script parameters and selecting the output location, execute the script with the following command:
```bash
python mean_var_opt.py
```

Depending on the number of simulations (value of 'sim_count'), it would take up to several seconds to output the .png file at above location.