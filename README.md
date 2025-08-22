# Company Risk Analysis System

A comprehensive web-based multi-page system for analyzing company data, identifying risk factors, and performing advanced clustering and anomaly detection.

## 🚀 Features

### Core Functionality
- **Multi-format Data Support**: Upload Excel (.xlsx) and CSV files
- **Data Completeness Analysis**: Automatic assessment of data quality and completeness
- **Intelligent Company Grouping**: Groups companies based on available features
- **Advanced Clustering**: K-means clustering within data completeness groups
- **Anomaly Detection**: Statistical outlier detection using IQR method
- **Interactive Visualizations**: Charts and graphs for data exploration

### Pages
1. **Home**: Overview and quick access to all features
2. **Data Upload**: File upload with validation and progress tracking
3. **Data Analysis**: Data overview, completeness assessment, and company groupings
4. **Clustering**: Company clustering within each data completeness group
5. **Anomaly Detection**: Statistical anomaly detection for risk assessment

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Charts**: Chart.js for interactive visualizations
- **Styling**: Bootstrap 5 with custom CSS
- **Icons**: Font Awesome

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)

## 🚀 Installation

### Option 1: Virtual Environment (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd company-risk-analysis
   ```

2. **Set up virtual environment**:
   ```bash
   # macOS/Linux
   chmod +x setup_venv.sh
   ./setup_venv.sh
   
   # Windows
   setup_venv.bat
   
   # Cross-platform
   python3 setup_venv.py
   ```

3. **Run the application**:
   ```bash
   # Use the virtual environment launcher
   python run_venv.py
   
   # Or manually activate and run
   source company_risk_env/bin/activate  # macOS/Linux
   # OR
   company_risk_env\Scripts\activate.bat  # Windows
   python app.py
   ```

4. **Access the web application**:
   Open your browser and navigate to `http://localhost:5001`

### Option 2: Direct Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd company-risk-analysis
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the web application**:
   Open your browser and navigate to `http://localhost:5001`

**Note**: We recommend using the virtual environment approach for better dependency management and isolation.

## 📊 Data Format Requirements

### Supported Formats
- **Excel**: .xlsx files
- **CSV**: Comma-separated values

### Data Structure
- **Companies**: Each row represents a company
- **Features**: Each column represents a feature/attribute
- **Headers**: First row should contain column names
- **Data Types**: Supports numeric and categorical data
- **Missing Values**: Automatically handled by the system

### Example Data Structure
| Company Name | Revenue | Employees | Industry | Risk Score | Location |
|--------------|---------|-----------|----------|------------|----------|
| Company A    | 1000000 | 50        | Tech     | 0.3        | Vilnius  |
| Company B    | 2500000 | 120       | Mfg      | 0.7        | Kaunas   |
| Company C    | 500000  | 25        | Services | 0.2        | Klaipeda |

## 🔍 How It Works

### 1. Data Upload & Processing
- Upload Excel or CSV files
- Automatic data type detection
- Data validation and error checking
- Progress tracking during processing

### 2. Data Completeness Analysis
- Calculates completeness percentage for each company
- Groups companies by data availability:
  - **Complete** (100%): All features available
  - **High Completeness** (80-99%): Most features available
  - **Medium Completeness** (50-79%): Moderate data availability
  - **Low Completeness** (<50%): Limited data available

### 3. Company Clustering
- Uses K-means clustering algorithm
- Only non-binary numeric features for meaningful clustering
- Configurable number of clusters (2-5)
- Automatic feature selection and data preprocessing

### 4. Anomaly Detection
- **Method**: Interquartile Range (IQR)
- **Process**: 
  - Calculate Q1 (25th percentile) and Q3 (75th percentile)
  - Compute IQR = Q3 - Q1
  - Identify outliers: values < Q1 - 1.5×IQR or > Q3 + 1.5×IQR
- **Output**: Statistical summary and outlier list

## 📈 Usage Guide

### Getting Started
1. **Upload Data**: Go to the Upload page and select your company data file
2. **Review Analysis**: Check the Data Analysis page for data overview and groupings
3. **Perform Clustering**: Use the Clustering page to group similar companies
4. **Detect Anomalies**: Identify outliers and potential risks using Anomaly Detection

### Best Practices
- Ensure data quality before upload
- Use descriptive column headers
- Remove unnecessary formatting from Excel files
- Check for consistent data types within columns
- Validate data completeness requirements

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=development
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Flask Configuration
- **Debug Mode**: Enabled by default for development
- **Host**: 0.0.0.0 (accessible from any network)
- **Port**: 5000
- **File Upload Limit**: 16MB

## 📁 Project Structure

```
company-risk-analysis/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── VENV_GUIDE.md         # Virtual environment guide
├── setup_venv.py         # Cross-platform virtual environment setup
├── setup_venv.sh         # Unix/Linux/macOS setup script
├── setup_venv.bat        # Windows setup script
├── run_venv.py           # Virtual environment launcher
├── run.py                 # Direct application launcher
├── test_data_loading.py  # Data testing script
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── upload.html       # Data upload page
│   ├── analysis.html     # Data analysis page
│   ├── clustering.html   # Clustering page
│   └── anomaly_detection.html # Anomaly detection page
├── static/                # Static files
│   ├── css/
│   │   └── style.css     # Custom CSS styles
│   └── js/
│       └── main.js       # Main JavaScript utilities
├── company_risk_env/      # Virtual environment (created by setup)
└── uploads/               # Uploaded files (created automatically)
```

## 🧪 Testing

### Manual Testing
1. Start the application
2. Navigate through all pages
3. Upload a sample data file
4. Test all functionality:
   - Data analysis
   - Clustering
   - Anomaly detection

### Sample Data
Use the included `Duomenys_AI_tikrinimui.xlsx` file for testing, or create your own sample data following the format requirements.

## 🚨 Troubleshooting

### Common Issues

1. **File Upload Errors**:
   - Check file format (.xlsx or .csv)
   - Ensure file size < 16MB
   - Verify file is not corrupted

2. **Clustering Issues**:
   - Ensure sufficient non-binary numeric features
   - Check data quality and completeness
   - Verify data types are correct

3. **Anomaly Detection Problems**:
   - Confirm feature contains numeric data
   - Check for sufficient data points
   - Verify no extreme outliers affecting calculations

### Error Messages
- **"No data loaded"**: Upload a file first
- **"Invalid file type"**: Use .xlsx or .csv files
- **"File too large"**: Reduce file size below 16MB
- **"Not enough features"**: Ensure sufficient numeric data

## 🔒 Security Considerations

- File upload validation and sanitization
- Secure file handling
- Input validation and sanitization
- Session management
- CSRF protection (Flask-WTF recommended for production)

## 🚀 Deployment

### Production Deployment
1. **Environment Setup**:
   ```bash
   export FLASK_ENV=production
   export FLASK_SECRET_KEY=your-production-secret-key
   ```

2. **WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Reverse Proxy** (Nginx recommended):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

## 🔮 Future Enhancements

- **Advanced Analytics**: Machine learning models for risk prediction
- **Data Export**: Export analysis results in various formats
- **User Authentication**: Multi-user support with role-based access
- **API Endpoints**: RESTful API for external integrations
- **Real-time Updates**: WebSocket support for live data updates
- **Mobile Responsiveness**: Enhanced mobile experience
- **Data Visualization**: More chart types and interactive features
- **Batch Processing**: Support for multiple file uploads
- **Data Validation**: Enhanced data quality checks
- **Reporting**: Automated report generation

---

**Note**: This system is designed for educational and business analysis purposes. Always validate results and use appropriate data handling practices for sensitive information.
