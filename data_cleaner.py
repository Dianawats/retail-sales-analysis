# Data cleaning functions

import pandas as pd

def clean_data(df):
    """
    Clean and preprocess the retail sales data
    Args: df (pandas.DataFrame): Raw data
    Returns: pandas.DataFrame: Cleaned data
    """
    print("\n" + "="*50)
    print("🧹 DATA CLEANING AND PREPROCESSING")
    print("="*50)
    
    # Create a copy to avoid modifying original data
    df_clean = df.copy()
    
    # Check for missing values
    print("🔍 Missing values analysis:")
    missing_values = df_clean.isnull().sum()
    print(missing_values)
    
    # Handle Date column (check common column names)
    date_columns = ['Date', 'date', 'DATE', 'order_date', 'sales_date']
    date_col = None
    
    for col in date_columns:
        if col in df_clean.columns:
            date_col = col
            break
    
    if date_col:
        df_clean['Date'] = pd.to_datetime(df_clean[date_col])
        print(f"✅ Converted '{date_col}' to datetime")
    else:
        print("❌ No date column found. Using existing 'Date' column.")
    
    # Sort by date
    df_clean = df_clean.sort_values('Date')
    
    # Create time-based features for analysis
    df_clean['Year'] = df_clean['Date'].dt.year
    df_clean['Month'] = df_clean['Date'].dt.month
    df_clean['Quarter'] = df_clean['Date'].dt.quarter
    df_clean['Month_Name'] = df_clean['Date'].dt.month_name()
    
    # Ensure numeric columns are properly formatted
    numeric_columns = ['Sales', 'Revenue', 'sales', 'revenue', 'amount']
    for col in numeric_columns:
        if col in df_clean.columns and col != 'Date':
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Fill missing numeric values with 0
    df_clean = df_clean.fillna(0)
    
    print(f"📅 Data range: {df_clean['Date'].min()} to {df_clean['Date'].max()}")
    print(f"📊 Total records: {len(df_clean)}")
    print(f"🏷️  Products: {df_clean['Product'].nunique() if 'Product' in df_clean.columns else 'N/A'}")
    print(f"🌍 Regions: {df_clean['Region'].nunique() if 'Region' in df_clean.columns else 'N/A'}")
    
    return df_clean

if __name__ == "__main__":
    # Test the cleaning function
    from data_loader import create_sample_data
    test_df = create_sample_data()
    cleaned_df = clean_data(test_df)
    print(cleaned_df.info())
