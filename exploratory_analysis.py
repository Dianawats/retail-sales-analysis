# EDA and visualization

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def setup_plot_style():
    """Set up consistent plot style across all visualizations"""
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12

def exploratory_analysis(df):
    """
    Perform exploratory data analysis with comprehensive visualizations
    Args: df (pandas.DataFrame): Cleaned data
    """
    print("\n" + "="*50)
    print("🔍 EXPLORATORY DATA ANALYSIS")
    print("="*50)
    
    setup_plot_style()
    
    # Create a comprehensive EDA dashboard
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Retail Sales - Exploratory Data Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Total sales over time
    if 'Date' in df.columns and 'Sales' in df.columns:
        monthly_sales = df.groupby('Date')['Sales'].sum().reset_index()
        axes[0, 0].plot(monthly_sales['Date'], monthly_sales['Sales'], linewidth=2, color='blue')
        axes[0, 0].set_title('Total Monthly Sales Over Time', fontweight='bold')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Total Sales')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. Sales by product
    if 'Product' in df.columns and 'Sales' in df.columns:
        product_sales = df.groupby('Product')['Sales'].sum().sort_values(ascending=False)
        bars = axes[0, 1].bar(product_sales.index, product_sales.values, color=sns.color_palette())
        axes[0, 1].set_title('Total Sales by Product', fontweight='bold')
        axes[0, 1].set_xlabel('Product')
        axes[0, 1].set_ylabel('Total Sales')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                          f'{height:,.0f}', ha='center', va='bottom')
    
    # 3. Sales by region
    if 'Region' in df.columns and 'Sales' in df.columns:
        region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        bars = axes[0, 2].bar(region_sales.index, region_sales.values, color=sns.color_palette())
        axes[0, 2].set_title('Total Sales by Region', fontweight='bold')
        axes[0, 2].set_xlabel('Region')
        axes[0, 2].set_ylabel('Total Sales')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[0, 2].text(bar.get_x() + bar.get_width()/2., height,
                          f'{height:,.0f}', ha='center', va='bottom')
    
    # 4. Sales distribution
    if 'Sales' in df.columns:
        axes[1, 0].hist(df['Sales'], bins=50, alpha=0.7, edgecolor='black', color='skyblue')
        axes[1, 0].set_title('Sales Distribution', fontweight='bold')
        axes[1, 0].set_xlabel('Sales Amount')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].grid(True, alpha=0.3)
    
    # 5. Monthly sales pattern
    if 'Month' in df.columns and 'Sales' in df.columns:
        monthly_avg = df.groupby('Month')['Sales'].mean()
        axes[1, 1].plot(monthly_avg.index, monthly_avg.values, marker='o', linewidth=2, color='green')
        axes[1, 1].set_title('Average Sales by Month', fontweight='bold')
        axes[1, 1].set_xlabel('Month')
        axes[1, 1].set_ylabel('Average Sales')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_xticks(range(1, 13))
    
    # 6. Yearly sales trend
    if 'Year' in df.columns and 'Sales' in df.columns:
        yearly_sales = df.groupby('Year')['Sales'].sum()
        axes[1, 2].plot(yearly_sales.index, yearly_sales.values, marker='s', linewidth=2, color='red')
        axes[1, 2].set_title('Yearly Sales Trend', fontweight='bold')
        axes[1, 2].set_xlabel('Year')
        axes[1, 2].set_ylabel('Total Sales')
        axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('exploratory_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print summary statistics
    print("\n📈 SUMMARY STATISTICS:")
    if 'Sales' in df.columns:
        sales_stats = df['Sales'].describe()
        print("Sales Statistics:")
        print(f"   Count: {sales_stats['count']:,.0f}")
        print(f"   Mean: {sales_stats['mean']:,.2f}")
        print(f"   Std: {sales_stats['std']:,.2f}")
        print(f"   Min: {sales_stats['min']:,.2f}")
        print(f"   Max: {sales_stats['max']:,.2f}")
    
    if 'Revenue' in df.columns:
        revenue_stats = df['Revenue'].describe()
        print("\nRevenue Statistics:")
        print(f"   Count: {revenue_stats['count']:,.0f}")
        print(f"   Mean: {revenue_stats['mean']:,.2f}")
        print(f"   Std: {revenue_stats['std']:,.2f}")

if __name__ == "__main__":
    from data_loader import create_sample_data
    from data_cleaner import clean_data
    test_df = create_sample_data()
    cleaned_df = clean_data(test_df)
    exploratory_analysis(cleaned_df)