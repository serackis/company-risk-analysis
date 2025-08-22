# 🚀 Company Risk Analysis System - Setup Instructions

## ✅ System Status: READY TO USE!

Your Company Risk Analysis System has been successfully created and is running. Here's everything you need to know:

## 🌐 Access the Application

**URL**: http://localhost:5001

The web application is currently running and accessible in your browser.

## 📊 Your Data File

The system has been tested with your existing Excel file:
- **File**: `Duomenys_AI_tikrinimui.xlsx`
- **Companies**: 7,052
- **Features**: 30
- **Data Types**: 28 numeric, 2 categorical
- **Overall Completeness**: 62.2%

## 🎯 What You Can Do Now

### 1. **Home Page** (`/`)
- Overview of all system features
- Quick access to all functionality
- System information and requirements

### 2. **Data Upload** (`/upload`)
- Upload your Excel file (already tested and working)
- File validation and progress tracking
- Support for .xlsx and .csv formats

### 3. **Data Analysis** (`/analysis`)
- View data overview and statistics
- See company groupings by data completeness
- Explore feature types and data quality
- Interactive data preview

### 4. **Company Clustering** (`/clustering`)
- Cluster companies within each data completeness group
- Use K-means clustering algorithm
- Configurable number of clusters (2-5)
- Visual cluster analysis

### 5. **Anomaly Detection** (`/anomaly_detection`)
- Identify statistical outliers in your data
- Use IQR method for anomaly detection
- Risk assessment by feature
- Detailed statistical analysis

## 🔧 How to Use the System

### Step 1: Upload Your Data
1. Go to http://localhost:5001/upload
2. Select your Excel file (`Duomenys_AI_tikrinimui.xlsx`)
3. Click "Upload and Analyze"
4. Wait for processing to complete

### Step 2: Explore Data Analysis
1. Navigate to the Analysis page
2. Review data completeness and company groupings
3. Examine feature types and data quality
4. Use the data preview to understand your data

### Step 3: Perform Clustering
1. Go to the Clustering page
2. Select a data completeness group
3. Choose number of clusters
4. Analyze clustering results and visualizations

### Step 4: Detect Anomalies
1. Visit the Anomaly Detection page
2. Select a numeric feature to analyze
3. Review outlier detection results
4. Identify potential risk factors

## 🛠️ Technical Details

### Backend
- **Framework**: Flask (Python)
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Port**: 5001 (to avoid conflicts with AirPlay on macOS)

### Frontend
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Responsive Design**: Mobile-friendly interface

### Data Processing
- **File Support**: Excel (.xlsx) and CSV (.csv)
- **Data Types**: Automatic detection of numeric/categorical
- **Missing Values**: Handled automatically
- **Binary Features**: Identified and excluded from clustering

## 📁 Project Structure

```
company-risk-analysis/
├── app.py                 # Main Flask application
├── run.py                 # Startup script
├── requirements.txt       # Python dependencies
├── README.md             # Comprehensive documentation
├── SETUP_INSTRUCTIONS.md # This file
├── test_data_loading.py  # Data testing script
├── Duomenys_AI_tikrinimui.xlsx # Your data file
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── upload.html      # Upload page
│   ├── analysis.html    # Analysis page
│   ├── clustering.html  # Clustering page
│   └── anomaly_detection.html # Anomaly detection
├── static/               # Static files
│   ├── css/style.css    # Custom styles
│   └── js/main.js       # JavaScript utilities
└── uploads/              # Upload directory (auto-created)
```

## 🚀 Starting the System

### Option 1: Use the startup script
```bash
python3 run.py
```

### Option 2: Run directly
```bash
python3 app.py
```

### Option 3: Use Flask development server
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5001
```

## 🔍 Testing Your Data

Run the test script to verify everything is working:
```bash
python3 test_data_loading.py
```

## 📊 Understanding Your Data

Based on the analysis, your dataset contains:
- **7,052 companies** with various levels of data completeness
- **30 features** including financial, employment, and risk indicators
- **Mixed data quality** - some companies have complete data, others have gaps
- **Risk indicators** - many binary features for risk assessment

## 🎯 Key Features for Your Use Case

### 1. **Data Completeness Analysis**
- Automatically groups companies by available data
- Helps identify which companies are suitable for different types of analysis

### 2. **Intelligent Clustering**
- Groups similar companies within each data completeness level
- Uses only non-binary numeric features for meaningful clustering
- Helps identify company segments and patterns

### 3. **Risk Factor Detection**
- Identifies statistical anomalies in your data
- Helps spot potential data quality issues or extreme values
- Supports risk assessment and decision making

## 🚨 Troubleshooting

### Port Already in Use
If you get "Address already in use" error:
- The system is already running
- Access it at http://localhost:5001
- Or change the port in `app.py`

### File Upload Issues
- Ensure file is .xlsx or .csv format
- Check file size (max 16MB)
- Verify file is not corrupted

### Data Analysis Problems
- Check that your Excel file has proper headers
- Ensure first row contains column names
- Verify data types are consistent within columns

## 🔮 Next Steps

1. **Explore the Interface**: Navigate through all pages to understand the system
2. **Upload Your Data**: Use the upload page to process your Excel file
3. **Analyze Results**: Review data completeness and company groupings
4. **Perform Clustering**: Group companies by similarity within data groups
5. **Detect Anomalies**: Identify outliers and potential risk factors
6. **Export Results**: Use the system to generate insights for decision making

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the comprehensive README.md
3. Check the browser console for JavaScript errors
4. Verify all dependencies are installed correctly

---

**🎉 Congratulations! Your Company Risk Analysis System is ready to use.**

**Access it now at: http://localhost:5001**
