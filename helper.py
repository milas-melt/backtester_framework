import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def loading_and_pre_processing(path_to_file, nan_method='zero', START_DATE='1969-01-01', END_DATE='2023-05-18'):
    """
    Data loading and pre-processing
    
    Parameters:
        path_to_file (str)
        nan_method (str). default: 'zero', to replace NaN with zeros. 
            Other options: 'drop' to drop NaN values
        START_DATE (datetime64[ns]). format: YYYY-MM-DD. 
            default: '1969-01-01', which is the minimum start date of the given dataset. 
            Pick the start date of your dataset
        END_DATE (datetime64[ns]). format: YYYY-MM-DD.
        default: '2023-05-18', which is the maximum end date of the given dataset. 
            Pick the end date of your dataset
            
    Returns:
        excess_returns (pandas.Dataframe)
        log_commodity_market_factor (pandas.Dataframe)
    """
    # Load data
    raw_excess_returns = pd.read_excel('data.xlsx', sheet_name='Return Indices')

    # Set 'Dates' column as index
    raw_excess_returns.set_index('Dates', inplace=True)

    # Replace consecutive spaces with underscores in column names
    raw_excess_returns.columns = raw_excess_returns.columns.str.replace(r'\s+', '_').str.upper()

    # Convert the index to datetime
    raw_excess_returns.index = pd.to_datetime(raw_excess_returns.index)

    raw_excess_returns = raw_excess_returns.loc[START_DATE:END_DATE]

    # divide by 100 returns
    raw_excess_returns = raw_excess_returns.div(100)-1

    if nan_method == 'zero':
        # replace NaN with 0
        raw_excess_returns = raw_excess_returns.fillna(0)
    elif nan_method == 'drop':
        raw_excess_returns = raw_excess_returns.dropna()

    # get a list of all the assets
    assets_list = raw_excess_returns.columns.values

    # calculate the commodity market factor
    commodity_market_factor = raw_excess_returns.mean(axis=1).to_frame()
    commodity_market_factor.index.name = 'Date'
    commodity_market_factor.rename(columns = {list(commodity_market_factor)[0]: 'commodity_market_factor'}, inplace = True)

    # # Add the 'commodity_market_factor' column to the DataFrame
    # raw_excess_returns['commodity_market_factor'] = commodity_market_factor

    # convert returns to log returns
    excess_returns = np.log(1+raw_excess_returns)

    log_commodity_market_factor = np.log(1+commodity_market_factor)
    
    return excess_returns, log_commodity_market_factor

def plot_ticker(data, ticker):
    """
    Plot the time series of a specific ticker's returns.
    
    Parameters:
        data (pd.DataFrame): DataFrame containing the return data.
        ticker (str): Ticker symbol of the asset to plot.
    """
    # Select the ticker column from the DataFrame
    ticker_returns = data[ticker]

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the time series
    ax.plot(ticker_returns.index, ticker_returns, label=ticker, linewidth=2)

    # Set plot title and axis labels
    ax.set_title(f"Time Series of {ticker} Returns", fontsize=14)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Returns', fontsize=12)

    # Customize tick labels
    ax.tick_params(axis='both', labelsize=10)

    # Add grid lines
    ax.grid(True, linestyle='--', linewidth=0.5)

    # Add legend
    ax.legend(loc='upper left', fontsize=10)

    # Adjust spacing and layout
    fig.tight_layout()

    # Show the plot
    plt.show()
    
def plot_df(df, xlabel='Date', ylabel='Excess Return', title='Asset Excess Returns'):
    """
    Plots the excess returns of assets from a DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the excess returns of assets.
        xlabel (str): Label for the x-axis. Default is 'Date'.
        ylabel (str): Label for the y-axis. Default is 'Excess Return'.
        title (str): Title of the plot. Default is 'Asset Excess Returns'.
    """
    plt.figure(figsize=(12, 8))  # Set the figure size
    
    # Set a color palette for the plot
    colors = sns.color_palette("Set2", len(df.columns))
    
    # Iterate through each column in the DataFrame
    for i, column in enumerate(df.columns):
        plt.plot(df.index, df[column], label=column, color=colors[i])
    
    plt.xlabel(xlabel, fontsize=12, fontweight='bold')  # Set the x-axis label
    plt.ylabel(ylabel, fontsize=12, fontweight='bold')  # Set the y-axis label
    plt.title(title, fontsize=14, fontweight='bold')  # Set the plot title
    plt.grid(True)  # Add gridlines to the plot
    
    # Customize the tick labels
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    # Remove the top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    # Move the legend outside of the graph
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    
    plt.tight_layout()  # Adjust the layout
    
    plt.show()  # Display the plot