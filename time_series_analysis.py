# Trend and seasonal analysis

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def setup_plot_style():
    """Set up consistent plot style"""
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

def time_series_analysis(df):
    """
    Perform time series analysis including trends and seasonal patterns
    Args: df (pandas.DataFrame): Cleaned data
    Returns: pandas.DataFrame: Monthly aggregated data
    """
    print("\n" + "="*50)
    print("📈 TIME SERIES ANALYSIS")
    print("="*50)
    
    setup_plot_style()
    
    # Aggregate data to monthly level
    monthly_data = df.groupby('Date').agg({
        'Sales': 'sum',
        'Revenue': 'sum'
    }).reset_index()
    
    monthly_data = monthly_data.set_index('Date')
    
    # Calculate moving averages for trend analysis
    monthly_data['MA_3'] = monthly_data['Sales'].rolling(window=3).mean()
    monthly_data['MA_6'] = monthly_data['Sales'].rolling(window=6).mean()
    monthly_data['MA_12'] = monthly_data['Sales'].rolling(window=12).mean()
    
    # Create comprehensive time series dashboard
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Time Series Analysis - Trends, Seasonality and Patterns', fontsize=16, fontweight='bold')
    
    # 1. Original time series with moving averages
    axes[0, 0].plot(monthly_data.index, monthly_data['Sales'], 
                   label='Actual Sales', alpha=0.7, linewidth=1)
    axes[0, 0].plot(monthly_data.index, monthly_data['MA_3'], 
                   label='3-Month MA', linewidth=2)
    axes[0, 0].plot(monthly_data.index, monthly_data['MA_6'], 
                   label='6-Month MA', linewidth=2)
    axes[0, 0].plot(monthly_data.index, monthly_data['MA_12'], 
                   label='12-Month MA', linewidth=2)
    axes[0, 0].set_title('Sales Trend with Moving Averages', fontweight='bold')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Sales')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Seasonal decomposition (simplified)
    monthly_data['Year'] = monthly_data.index.year
    monthly_data['Month'] = monthly_data.index.month
    
    seasonal_pattern = monthly_data.groupby('Month')['Sales'].mean()
    axes[0, 1].plot(seasonal_pattern.index, seasonal_pattern.values, 
                   marker='o', linewidth=2, color='green')
    axes[0, 1].set_title('Seasonal Pattern (Monthly Average)', fontweight='bold')
    axes[0, 1].set_xlabel('Month')
    axes[0, 1].set_ylabel('Average Sales')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_xticks(range(1, 13))
    
    # Add month names to x-axis
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    axes[0, 1].set_xticklabels(month_names)
    
    # 3. Year-over-year comparison
    yearly_sales = monthly_data.groupby('Year')['Sales'].sum()
    bars = axes[1, 0].bar(yearly_sales.index, yearly_sales.values, 
                         color=sns.color_palette())
    axes[1, 0].set_title('Yearly Sales Comparison', fontweight='bold')
    axes[1, 0].set_xlabel('Year')
    axes[1, 0].set_ylabel('Total Sales')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Quarterly sales trend
    quarterly_sales = monthly_data.resample('Q').sum()['Sales']
    axes[1, 1].plot(quarterly_sales.index, quarterly_sales.values, 
                   marker='o', linewidth=2, color='red')
    axes[1, 1].set_title('Quarterly Sales Trend', fontweight='bold')
    axes[1, 1].set_xlabel('Quarter')
    axes[1, 1].set_ylabel('Sales')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('time_series_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print trend analysis results
    print("\n📊 TREND ANALYSIS RESULTS:")
    print(f"Data period: {monthly_data.index.min()} to {monthly_data.index.max()}")
    print(f"Total months: {len(monthly_data)}")
    print(f"Average monthly sales: {monthly_data['Sales'].mean():,.2f}")
    
    # Calculate growth rate
    if len(monthly_data) > 1:
        first_month = monthly_data['Sales'].iloc[0]
        last_month = monthly_data['Sales'].iloc[-1]
        growth_rate = ((last_month - first_month) / first_month) * 100
        print(f"Overall growth rate: {growth_rate:.2f}%")
    
    # Seasonal strength
    seasonal_strength = seasonal_pattern.std() / monthly_data['Sales'].mean() * 100
    print(f"Seasonal strength: {seasonal_strength:.2f}%")
    
    return monthly_data

if __name__ == "__main__":
    from data_loader import create_sample_data
    from data_cleaner import clean_data
    test_df = create_sample_data()
    cleaned_df = clean_data(test_df)
    monthly_data = time_series_analysis(cleaned_df)
    print(f"Monthly data shape: {monthly_data.shape}")