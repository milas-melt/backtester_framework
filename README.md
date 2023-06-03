# Custom Python Framework Backtester
- Breakout strat with combined signals from different breakout criteria. 
- Look Back Straddle Deltas MA Cross Over strat
- Returns prediction using ML for seasonality detection fed into a random forest for prediction. (unsupervised-to-supervised learning methods)
- Backtester from 1969 to 2023 with rolling_table and performance analysis

## Benchmark
Equally weighted portfolio of all commodities in the dataset.

## Breakout strat
Breakout trading is a popular and dynamic trading strategy employed by traders.
It revolves around identifying and capitalizing on significant price movements that occur
when an asset's price breaks through a well-defined level of support or resistance. 

### High Low 
#### Signal strat
"Buy a higher high, sell a lower low, and hold the position to make a profit."
- Long if today’s return is the highest of all the returns in the window.
- Short if today’s return is the lowest of all the returns in the window.
- Else, hold.

#### Performance

<img width="855" alt="Screenshot 2023-06-03 at 20 00 42" src="https://github.com/milas-melt/backtester_framework/assets/55765976/c2ac1b96-b262-4ac1-977c-d133cce4f77a">

### Mean Std 
#### Signal strat

- Long when return is higher than mean +1 * std 
- Short when return is below the mean -1 * std
- Else, hold.

#### Performance

<img width="855" alt="Screenshot 2023-06-03 at 20 01 11" src="https://github.com/milas-melt/backtester_framework/assets/55765976/3840b20e-1931-4f30-88f2-77a7c4fe3f59">

### Combine the two criteria
Many ways of doing so. Assuming no tx fees, one solution is to compute the equally weighted average of both signals.

#### Performance

<img width="855" alt="Screenshot 2023-06-03 at 20 01 33" src="https://github.com/milas-melt/backtester_framework/assets/55765976/cbbfba57-251c-443e-b5a3-1737e9b007d7">

## Lookback straddle delta MA crossover
### Method

![image](https://github.com/milas-melt/backtester_framework/assets/55765976/400f06b4-f339-4a92-9e91-6f183e4b9443)
We assume the first day price is one and compute the subsequent price based on. We then compute that 5 day Moving Average of the delta. We choose to use the delta’s MA rather than the price volatility since it can catch up the reversal more quickly, as shown in the figure below. 

Thus, it would be helpful to limit our loss.

<img width="671" alt="Screenshot 2023-06-03 at 20 19 04" src="https://github.com/milas-melt/backtester_framework/assets/55765976/8f3459ce-780e-4623-9792-dd001f124f07">

### Signal strat
The signals are generated as follow:
- If the current delta crosses the 5 Day delta MA to go down, we sell.
- If the current delta crosses the 5 Day delta MA to go up, we buy.

### Performance

<img width="671" alt="Screenshot 2023-06-03 at 20 19 45" src="https://github.com/milas-melt/backtester_framework/assets/55765976/a04cc323-a4aa-4fcc-b802-416a7a2762cf">

<img width="671" alt="Screenshot 2023-06-03 at 20 20 03" src="https://github.com/milas-melt/backtester_framework/assets/55765976/ded10791-e3ca-4992-8ee8-5c3b640f7a55">

According to both performance graphs, it is clear that although the strategy generated is better than the benchmark, further computation is required in order to define how well the strategy does in comparison to the others. A similar computation with other signals cannot be done within less than 6 hours at least which is why the trategy is backtested on 5 months data only.

## Machine Learning Methods
First, the prophet model was used to decompose the returns into different time intervals, according to the signals seasonalities and patterns (such as harvesing cycles for agricultural commodities, for instance).

<img width="655" alt="Screenshot 2023-06-03 at 20 24 51" src="https://github.com/milas-melt/backtester_framework/assets/55765976/9ad71bd3-95b1-4dc6-b9c0-da488bb256c9">

Then, these variables are fed in a random forest model for future return predictions.

<img width="638" alt="Screenshot 2023-06-03 at 20 26 01" src="https://github.com/milas-melt/backtester_framework/assets/55765976/e93d1700-8736-4501-88d0-936688747b4e">

### Error Metrics
MSE: 0.0346 
R^2: 0.000305. 

The MSE is small however, the R^2 suggests that the model requires further improvements.
