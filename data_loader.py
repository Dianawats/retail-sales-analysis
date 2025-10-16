# Data loading and preparation

import pandas as pd
import numpy as np

def load_and_prepare_data():
    """
    Load and prepare the retail sales data from multiple files
    Returns: pandas.DataFrame
    """
    try:
        # Try to load actual dataset - adjust filename based on your downloaded file
        # Use the first dataset from your Google Drive links
        df = pd.read_csv('walmart_sales_data.csv')  # Change this to your actual file name
        
        print("✅ Dataset loaded successfully!")
        print(f"📊 Dataset shape: {df.shape}")
        
        return df
    
    except FileNotFoundError:
        print("⚠️  File not found. Creating sample data for demonstration...")
        return create_sample_data()

def create_sample_data():
    """
    Create sample retail sales data if actual files aren't available
    Returns: pandas.DataFrame
    """
    print("🛠️  Creating sample data for demonstration...")
    
    # Generate realistic sample data
    dates = pd.date_range('2010-01-01', '2015-12-31', freq='M')
    products = ['Electronics', 'Clothing', 'Home Goods', 'Sports']
    regions = ['North', 'South', 'East', 'West']
    
    data = []
    for date in dates:
        for product in products:
            for region in regions:
                # Create realistic sales patterns with trend and seasonality
                base_sales = 1000 + (date.year - 2010) * 200  # Upward trend
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.month / 12)  # Seasonality
                product_factor = {'Electronics': 1.5, 'Clothing': 1.2, 'Home Goods': 1.0, 'Sports': 0.8}[product]
                region_factor = {'North': 1.1, 'South': 1.0, 'East': 0.9, 'West': 1.2}[region]
                
                sales = base_sales * seasonal_factor * product_factor * region_factor * np.random.uniform(0.8, 1.2)
                
                data.append({
                    'Date': date,
                    'Product': product,
                    'Region': region,
                    'Sales': max(0, sales),
                    'Revenue': sales * np.random.uniform(10, 100)
                })
    
    df = pd.DataFrame(data)
    print("✅ Sample data created successfully!")
    return df

if __name__ == "__main__":
    # Test the data loading
    test_df = load_and_prepare_data()
    print(f"Test data shape: {test_df.shape}")
    print(test_df.head())