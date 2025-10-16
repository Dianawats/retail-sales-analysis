 # Main script to run the entire analysis

"""
Retail Sales Time Series Analysis
Internship Assignment - Elevvo
Author: Diana Wats
Date: 2025-10-16

This project analyzes retail sales data to identify trends, seasonal patterns,
and provide revenue breakdowns by product and region.
"""

import time
from data_loader import load_and_prepare_data
from data_cleaner import clean_data
from exploratory_analysis import exploratory_analysis
from time_series_analysis import time_series_analysis
from revenue_analysis import revenue_breakdown
from forecasting import simple_forecasting
from insights import generate_insights

def main():
    """
    Main function to run the complete retail sales analysis
    """
    print("🚀 RETAIL SALES TIME SERIES ANALYSIS")
    print("=====================================")
    print("Internship Assignment - Elevvo")
    print("Starting comprehensive analysis...\n")
    
    start_time = time.time()
    
    try:
        # Step 1: Load and prepare data
        print("📁 STEP 1: Loading data...")
        df = load_and_prepare_data()
        
        # Step 2: Clean and preprocess data
        print("\n🧹 STEP 2: Cleaning data...")
        df_clean = clean_data(df)
        
        # Step 3: Exploratory Data Analysis
        print("\n🔍 STEP 3: Exploratory analysis...")
        exploratory_analysis(df_clean)
        
        # Step 4: Time Series Analysis
        print("\n📈 STEP 4: Time series analysis...")
        monthly_data = time_series_analysis(df_clean)
        
        # Step 5: Revenue Breakdown
        print("\n💰 STEP 5: Revenue breakdown analysis...")
        revenue_breakdown(df_clean)
        
        # Step 6: Forecasting (Bonus)
        print("\n🔮 STEP 6: Sales forecasting...")
        forecast_df = simple_forecasting(monthly_data)
        
        # Step 7: Generate Insights
        print("\n💡 STEP 7: Generating insights...")
        generate_insights(df_clean, monthly_data, forecast_df)
        
        # Calculate execution time
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
        
        print("\n🎉 ANALYSIS COMPLETED!")
        print("Generated files:")
        print("   - exploratory_analysis.png")
        print("   - time_series_analysis.png")
        print("   - revenue_breakdown.png")
        print("   - sales_forecasting.png")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("Please check your data and try again.")

if __name__ == "__main__":
    main()