# Final insights and summary

import pandas as pd
import numpy as np

def generate_insights(df, monthly_data, forecast_df=None):
    """
    Generate final insights and business recommendations
    Args: df (pandas.DataFrame): Original cleaned data
          monthly_data (pandas.DataFrame): Monthly aggregated data
          forecast_df (pandas.DataFrame): Forecast results
    """
    print("\n" + "="*50)
    print("💡 FINAL INSIGHTS AND BUSINESS RECOMMENDATIONS")
    print("="*50)
    
    # Key metrics calculation
    total_sales = df['Sales'].sum()
    total_revenue = df['Revenue'].sum() if 'Revenue' in df.columns else 0
    avg_monthly_sales = monthly_data['Sales'].mean()
    
    # Growth calculation
    if len(monthly_data) > 1:
        sales_growth = ((monthly_data['Sales'].iloc[-1] - monthly_data['Sales'].iloc[0]) / 
                       monthly_data['Sales'].iloc[0] * 100)
    else:
        sales_growth = 0
    
    # Top performing products and regions
    top_product = df.groupby('Product')['Sales'].sum().idxmax() if 'Product' in df.columns else "N/A"
    top_region = df.groupby('Region')['Sales'].sum().idxmax() if 'Region' in df.columns else "N/A"
    
    # Seasonal insights
    monthly_avg = df.groupby('Month')['Sales'].mean()
    best_month = monthly_avg.idxmax()
    worst_month = monthly_avg.idxmin()
    
    # Product performance
    if 'Product' in df.columns:
        product_performance = df.groupby('Product')['Sales'].sum().sort_values(ascending=False)
        best_product = product_performance.index[0]
        worst_product = product_performance.index[-1]
    
    # Region performance
    if 'Region' in df.columns:
        region_performance = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        best_region = region_performance.index[0]
        worst_region = region_performance.index[-1]
    
    print("📊 KEY BUSINESS METRICS:")
    print(f"   • Total Sales: ${total_sales:,.2f}")
    if total_revenue > 0:
        print(f"   • Total Revenue: ${total_revenue:,.2f}")
    print(f"   • Average Monthly Sales: ${avg_monthly_sales:,.2f}")
    print(f"   • Overall Sales Growth: {sales_growth:.1f}%")
    print(f"   • Data Period: {len(monthly_data)} months")
    
    print("\n🏆 PERFORMANCE HIGHLIGHTS:")
    print(f"   • Top Performing Product: {top_product}")
    print(f"   • Top Performing Region: {top_region}")
    print(f"   • Best Sales Month: {best_month} ({monthly_avg[best_month]:,.0f} avg sales)")
    print(f"   • Worst Sales Month: {worst_month} ({monthly_avg[worst_month]:,.0f} avg sales)")
    
    print("\n📈 TREND ANALYSIS:")
    # Calculate recent trend (last 6 months vs previous 6 months)
    if len(monthly_data) >= 12:
        recent_sales = monthly_data['Sales'].tail(6).mean()
        previous_sales = monthly_data['Sales'].tail(12).head(6).mean()
        recent_trend = ((recent_sales - previous_sales) / previous_sales) * 100
        print(f"   • Recent Trend (last 6 months): {recent_trend:+.1f}%")
    
    # Seasonal strength
    seasonal_strength = (monthly_avg.max() - monthly_avg.min()) / monthly_avg.mean() * 100
    print(f"   • Seasonal Variation: {seasonal_strength:.1f}%")
    
    print("\n💡 STRATEGIC RECOMMENDATIONS:")
    print("1. 📦 PRODUCT STRATEGY:")
    print(f"   • Focus on expanding {top_product} product line")
    print(f"   • Review underperforming products for improvement opportunities")
    
    print("\n2. 🌍 REGIONAL STRATEGY:")
    print(f"   • Leverage success factors from {top_region} region")
    print(f"   • Develop targeted campaigns for underperforming regions")
    
    print("\n3. 📅 SEASONAL PLANNING:")
    print(f"   • Prepare for peak season in month {best_month}")
    print(f"   • Implement promotions during slow month {worst_month}")
    
    print("\n4. 📊 FORECASTING & INVENTORY:")
    print("   • Use moving averages for short-term inventory planning")
    print("   • Consider seasonal patterns for long-term strategy")
    
    if forecast_df is not None:
        print("\n5. 🔮 FORECAST INSIGHTS:")
        avg_forecast = forecast_df['Exponential_Smoothing_Forecast'].mean()
        forecast_growth = ((avg_forecast - monthly_data['Sales'].mean()) / monthly_data['Sales'].mean()) * 100
        print(f"   • Expected average sales: ${avg_forecast:,.0f}")
        print(f"   • Projected growth: {forecast_growth:+.1f}%")
    
    print("\n6. 🎯 ACTIONABLE NEXT STEPS:")
    print("   • Implement the forecasting model for inventory management")
    print("   • Conduct deep-dive analysis on top-performing categories")
    print("   • Develop region-specific marketing strategies")
    print("   • Monitor seasonal patterns for promotional planning")
    
    print("\n" + "="*50)
    print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*50)

if __name__ == "__main__":
    from data_loader import create_sample_data
    from data_cleaner import clean_data
    from time_series_analysis import time_series_analysis
    from forecasting import simple_forecasting
    
    test_df = create_sample_data()
    cleaned_df = clean_data(test_df)
    monthly_data = time_series_analysis(cleaned_df)
    forecast_df = simple_forecasting(monthly_data)
    generate_insights(cleaned_df, monthly_data, forecast_df)