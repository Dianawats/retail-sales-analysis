 # Forecasting models

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def setup_plot_style():
    """Set up consistent plot style"""
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

def exponential_smoothing(series, alpha=0.3):
    """
    Simple exponential smoothing forecasting
    Args: series (array-like): Time series data
          alpha (float): Smoothing parameter (0-1)
    Returns: list: Smoothed values
    """
    result = [series[0]]  # First value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

def simple_forecasting(monthly_data):
    """
    Implement simple forecasting using rolling mean and exponential smoothing
    Args: monthly_data (pandas.DataFrame): Monthly aggregated data
    """
    print("\n" + "="*50)
    print("🔮 SIMPLE FORECASTING")
    print("="*50)
    
    setup_plot_style()
    
    # Prepare data for forecasting
    sales_series = monthly_data['Sales'].dropna()
    
    if len(sales_series) < 12:
        print("❌ Insufficient data for forecasting. Need at least 12 months of data.")
        return
    
    # Method 1: Rolling Mean Forecast
    forecast_horizon = 6  # Forecast next 6 months
    last_rolling_mean = sales_series.rolling(window=12).mean().iloc[-1]
    rolling_forecast = [last_rolling_mean] * forecast_horizon
    
    # Method 2: Simple Exponential Smoothing
    exp_smooth = exponential_smoothing(sales_series.values, alpha=0.3)
    last_exp_smooth = exp_smooth[-1]
    exp_forecast = [last_exp_smooth] * forecast_horizon
    
    # Method 3: Seasonal Naive (using same month last year)
    seasonal_forecast = []
    if len(sales_series) >= 12:
        last_year_data = sales_series[-12:]
        for i in range(forecast_horizon):
            seasonal_forecast.append(last_year_data.iloc[i % 12])
    
    # Create future dates for forecast
    last_date = sales_series.index[-1]
    future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=forecast_horizon,
        freq='M'
    )
    
    # Plot historical data and forecasts
    plt.figure(figsize=(14, 8))
    
    # Plot historical data
    plt.plot(sales_series.index, sales_series.values, 
             label='Historical Sales', linewidth=2, color='blue', alpha=0.8)
    
    # Plot exponential smoothing on historical data
    plt.plot(sales_series.index, exp_smooth, 
             label='Exponential Smoothing (Historical)', linewidth=2, color='green', alpha=0.7)
    
    # Plot forecasts
    plt.plot(future_dates, rolling_forecast, 
             label='Rolling Mean Forecast', linewidth=3, color='red', linestyle='--', marker='o')
    plt.plot(future_dates, exp_forecast, 
             label='Exponential Smoothing Forecast', linewidth=3, color='orange', linestyle='--', marker='s')
    
    if seasonal_forecast:
        plt.plot(future_dates, seasonal_forecast, 
                 label='Seasonal Naive Forecast', linewidth=3, color='purple', linestyle='--', marker='^')
    
    plt.title('Sales Forecasting using Multiple Methods', fontsize=16, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('sales_forecasting.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create forecast dataframe
    forecast_data = {
        'Date': future_dates,
        'Rolling_Mean_Forecast': rolling_forecast,
        'Exponential_Smoothing_Forecast': exp_forecast
    }
    
    if seasonal_forecast:
        forecast_data['Seasonal_Naive_Forecast'] = seasonal_forecast
    
    forecast_df = pd.DataFrame(forecast_data)
    
    print("📅 FORECAST FOR NEXT 6 MONTHS:")
    print(forecast_df.round(2))
    
    # Calculate forecast accuracy on last 6 months of historical data
    if len(sales_series) >= 18:  # Need enough data for holdout test
        train_data = sales_series[:-6]
        test_data = sales_series[-6:]
        
        # Rolling mean forecast for test period
        rolling_pred = [train_data.rolling(window=12).mean().iloc[-1]] * 6
        
        # Exponential smoothing forecast for test period
        exp_train = exponential_smoothing(train_data.values, alpha=0.3)
        exp_pred = [exp_train[-1]] * 6
        
        # Seasonal naive forecast for test period
        seasonal_pred = []
        if len(train_data) >= 12:
            seasonal_train = train_data[-12:]
            for i in range(6):
                seasonal_pred.append(seasonal_train.iloc[i % 12])
        
        # Calculate metrics
        metrics = {}
        
        # Rolling Mean metrics
        metrics['Rolling Mean'] = {
            'MAE': mean_absolute_error(test_data, rolling_pred),
            'RMSE': np.sqrt(mean_squared_error(test_data, rolling_pred)),
            'MAPE': np.mean(np.abs((test_data - rolling_pred) / test_data)) * 100
        }
        
        # Exponential Smoothing metrics
        metrics['Exponential Smoothing'] = {
            'MAE': mean_absolute_error(test_data, exp_pred),
            'RMSE': np.sqrt(mean_squared_error(test_data, exp_pred)),
            'MAPE': np.mean(np.abs((test_data - exp_pred) / test_data)) * 100
        }
        
        # Seasonal Naive metrics
        if seasonal_pred:
            metrics['Seasonal Naive'] = {
                'MAE': mean_absolute_error(test_data, seasonal_pred),
                'RMSE': np.sqrt(mean_squared_error(test_data, seasonal_pred)),
                'MAPE': np.mean(np.abs((test_data - seasonal_pred) / test_data)) * 100
            }
        
        print(f"\n📊 FORECAST ACCURACY (Last 6 months holdout):")
        for method, method_metrics in metrics.items():
            print(f"\n{method}:")
            print(f"   MAE:  {method_metrics['MAE']:.2f}")
            print(f"   RMSE: {method_metrics['RMSE']:.2f}")
            print(f"   MAPE: {method_metrics['MAPE']:.2f}%")
    
    return forecast_df

if __name__ == "__main__":
    from data_loader import create_sample_data
    from data_cleaner import clean_data
    from time_series_analysis import time_series_analysis
    test_df = create_sample_data()
    cleaned_df = clean_data(test_df)
    monthly_data = time_series_analysis(cleaned_df)
    forecast_df = simple_forecasting(monthly_data)