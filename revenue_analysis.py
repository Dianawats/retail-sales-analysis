# Product and region breakdown

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def setup_plot_style():
    """Set up consistent plot style"""
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

def revenue_breakdown(df):
    """
    Analyze revenue breakdown by product and region over time
    Args: df (pandas.DataFrame): Cleaned data
    """
    print("\n" + "="*50)
    print("💰 REVENUE BREAKDOWN ANALYSIS")
    print("="*50)
    
    setup_plot_style()
    
    # Create comprehensive revenue analysis dashboard
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Revenue Breakdown by Product and Region Over Time', fontsize=16, fontweight='bold')
    
    # 1. Revenue by product over time (stacked area)
    if 'Product' in df.columns:
        product_time_series = df.pivot_table(
            index='Date', 
            columns='Product', 
            values='Revenue', 
            aggfunc='sum'
        ).fillna(0)
        
        product_time_series.plot.area(ax=axes[0, 0], alpha=0.8)
        axes[0, 0].set_title('Revenue by Product Over Time', fontweight='bold')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Revenue')
        axes[0, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Revenue by region over time (stacked area)
    if 'Region' in df.columns:
        region_time_series = df.pivot_table(
            index='Date', 
            columns='Region', 
            values='Revenue', 
            aggfunc='sum'
        ).fillna(0)
        
        region_time_series.plot.area(ax=axes[0, 1], alpha=0.8)
        axes[0, 1].set_title('Revenue by Region Over Time', fontweight='bold')
        axes[0, 1].set_xlabel('Date')
        axes[0, 1].set_ylabel('Revenue')
        axes[0, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Product-region heatmap (average revenue)
    if 'Product' in df.columns and 'Region' in df.columns:
        product_region_heatmap = df.pivot_table(
            index='Product',
            columns='Region',
            values='Revenue',
            aggfunc='mean'
        )
        
        sns.heatmap(product_region_heatmap, annot=True, fmt='.0f', 
                   cmap='YlOrRd', ax=axes[1, 0], cbar_kws={'label': 'Average Revenue'})
        axes[1, 0].set_title('Average Revenue: Product vs Region', fontweight='bold')
    
    # 4. Monthly revenue trend by product (line plot)
    if 'Product' in df.columns:
        monthly_product_revenue = df.groupby(['Date', 'Product'])['Revenue'].sum().unstack()
        monthly_product_revenue.plot(ax=axes[1, 1], linewidth=2)
        axes[1, 1].set_title('Monthly Revenue Trend by Product', fontweight='bold')
        axes[1, 1].set_xlabel('Date')
        axes[1, 1].set_ylabel('Revenue')
        axes[1, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('revenue_breakdown.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print detailed revenue analysis
    print("\n📊 REVENUE ANALYSIS SUMMARY:")
    
    if 'Product' in df.columns:
        print("\n📦 Revenue by Product:")
        product_summary = df.groupby('Product')['Revenue'].agg(['sum', 'mean', 'std', 'count']).round(2)
        product_summary['sum'] = product_summary['sum'].apply(lambda x: f"${x:,.2f}")
        product_summary['mean'] = product_summary['mean'].apply(lambda x: f"${x:,.2f}")
        print(product_summary)
    
    if 'Region' in df.columns:
        print("\n🌍 Revenue by Region:")
        region_summary = df.groupby('Region')['Revenue'].agg(['sum', 'mean', 'std', 'count']).round(2)
        region_summary['sum'] = region_summary['sum'].apply(lambda x: f"${x:,.2f}")
        region_summary['mean'] = region_summary['mean'].apply(lambda x: f"${x:,.2f}")
        print(region_summary)
    
    # Calculate overall revenue metrics
    if 'Revenue' in df.columns:
        total_revenue = df['Revenue'].sum()
        avg_revenue = df['Revenue'].mean()
        print(f"\n💰 Overall Revenue Metrics:")
        print(f"   Total Revenue: ${total_revenue:,.2f}")
        print(f"   Average Transaction: ${avg_revenue:,.2f}")
        print(f"   Total Transactions: {len(df):,}")

if __name__ == "__main__":
    from data_loader import create_sample_data
    from data_cleaner import clean_data
    test_df = create_sample_data()
    cleaned_df = clean_data(test_df)
    revenue_breakdown(cleaned_df)