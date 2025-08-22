#!/usr/bin/env python3
"""
Test script to verify data loading functionality
"""

import pandas as pd
import numpy as np
import os

def test_excel_loading():
    """Test loading the existing Excel file"""
    print("🧪 Testing Excel file loading...")
    
    # Check if the Excel file exists
    excel_file = 'Duomenys_AI_tikrinimui.xlsx'
    if not os.path.exists(excel_file):
        print(f"❌ Excel file '{excel_file}' not found!")
        return False
    
    try:
        # Load the Excel file
        print(f"📁 Loading file: {excel_file}")
        df = pd.read_excel(excel_file)
        
        print(f"✅ Successfully loaded Excel file!")
        print(f"📊 Data shape: {df.shape}")
        print(f"🏢 Number of companies: {len(df)}")
        print(f"📋 Number of features: {len(df.columns)}")
        
        # Display column information
        print("\n📋 Column information:")
        for i, col in enumerate(df.columns):
            dtype = str(df[col].dtype)
            non_null = df[col].notna().sum()
            null_count = df[col].isna().sum()
            unique_count = df[col].nunique()
            
            print(f"  {i+1:2d}. {col:<20} | Type: {dtype:<10} | Non-null: {non_null:3d} | Null: {null_count:3d} | Unique: {unique_count:3d}")
        
        # Check data completeness
        print("\n📊 Data completeness analysis:")
        completeness = df.notna().sum(axis=1)
        total_features = len(df.columns)
        completeness_percentage = (completeness / total_features) * 100
        
        print(f"  Overall completeness: {(df.notna().sum().sum() / (len(df) * total_features)) * 100:.1f}%")
        print(f"  Companies with 100% data: {(completeness_percentage == 100).sum()}")
        print(f"  Companies with 80-99% data: {((completeness_percentage >= 80) & (completeness_percentage < 100)).sum()}")
        print(f"  Companies with 50-79% data: {((completeness_percentage >= 50) & (completeness_percentage < 80)).sum()}")
        print(f"  Companies with <50% data: {(completeness_percentage < 50).sum()}")
        
        # Check data types
        print("\n🔍 Data type analysis:")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        print(f"  Numeric columns: {len(numeric_cols)}")
        print(f"  Categorical columns: {len(categorical_cols)}")
        
        if numeric_cols:
            print(f"  Numeric features: {', '.join(numeric_cols[:5])}{'...' if len(numeric_cols) > 5 else ''}")
        
        if categorical_cols:
            print(f"  Categorical features: {', '.join(categorical_cols[:5])}{'...' if len(categorical_cols) > 5 else ''}")
        
        # Sample data preview
        print("\n👀 Sample data preview (first 3 rows):")
        print(df.head(3).to_string())
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return False

def test_data_analysis_functions():
    """Test the data analysis functions from app.py"""
    print("\n🧪 Testing data analysis functions...")
    
    try:
        # Import functions from app.py
        from app import analyze_data_completeness, identify_binary_features
        
        # Load data
        df = pd.read_excel('Duomenys_AI_tikrinimui.xlsx')
        
        # Test completeness analysis
        print("  📊 Testing completeness analysis...")
        groups, df_with_completeness = analyze_data_completeness(df)
        
        print(f"    Found {len(groups)} data groups:")
        for group_name, group_data in groups.items():
            print(f"      {group_name}: {len(group_data)} companies")
        
        # Test binary feature identification
        print("  🔍 Testing binary feature identification...")
        binary_features = identify_binary_features(df)
        print(f"    Found {len(binary_features)} binary features:")
        for feature in binary_features[:5]:  # Show first 5
            print(f"      - {feature}")
        
        print("  ✅ Data analysis functions working correctly!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing data analysis functions: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Company Risk Analysis System - Data Loading Test")
    print("=" * 60)
    
    # Test Excel loading
    excel_ok = test_excel_loading()
    
    if excel_ok:
        # Test data analysis functions
        analysis_ok = test_data_analysis_functions()
        
        if analysis_ok:
            print("\n🎉 All tests passed! The system is ready to use.")
            print("\n📱 You can now:")
            print("  1. Open http://localhost:5001 in your browser")
            print("  2. Upload the Excel file for analysis")
            print("  3. Explore the data analysis features")
        else:
            print("\n⚠️  Excel loading works, but data analysis functions have issues.")
    else:
        print("\n❌ Excel loading failed. Please check the file and dependencies.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
