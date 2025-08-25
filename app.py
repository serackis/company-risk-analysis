from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objs as go
import plotly.utils
import json
import os
from werkzeug.utils import secure_filename
import tempfile
import shutil
from translations import get_text, get_language_name

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variable to store the current dataset
current_data = None
data_groups = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls', 'csv'}

def load_data(file_path):
    """Load data from Excel or CSV file"""
    try:
        if file_path.endswith('.xlsx'):
            # Try different Excel engines for better compatibility
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
            except Exception as e1:
                try:
                    df = pd.read_excel(file_path, engine='xlrd')
                except Exception as e2:
                    # Last resort: try without specifying engine
                    df = pd.read_excel(file_path)
        elif file_path.endswith('.xls'):
            # Handle older Excel format
            df = pd.read_excel(file_path, engine='xlrd')
        else:
            # Handle CSV files
            df = pd.read_csv(file_path)
        
        # Basic data validation
        if df.empty:
            print("Error: File contains no data")
            return None
            
        if len(df.columns) < 2:
            print("Error: File must contain at least 2 columns (companies and features)")
            return None
            
        print(f"Successfully loaded data: {len(df)} rows, {len(df.columns)} columns")
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        print(f"File path: {file_path}")
        print(f"File extension: {file_path.split('.')[-1] if '.' in file_path else 'unknown'}")
        return None

def analyze_data_completeness(df):
    """Analyze data completeness and group companies by available features"""
    # Calculate completeness for each company (row)
    completeness = df.notna().sum(axis=1)
    total_features = len(df.columns)
    completeness_percentage = (completeness / total_features) * 100
    
    # Create a copy of dataframe with completeness info
    df_with_completeness = df.copy()
    df_with_completeness['completeness_percentage'] = completeness_percentage
    df_with_completeness['missing_features'] = total_features - completeness
    
    # Group companies by completeness
    groups = {}
    
    # Group 1: Companies with all features (100% complete)
    complete_companies = df_with_completeness[df_with_completeness['completeness_percentage'] == 100]
    if not complete_companies.empty:
        groups['complete'] = complete_companies
    
    # Group 2: Companies with high completeness (80-99%)
    high_completeness = df_with_completeness[
        (df_with_completeness['completeness_percentage'] >= 80) & 
        (df_with_completeness['completeness_percentage'] < 100)
    ]
    if not high_completeness.empty:
        groups['high_completeness'] = high_completeness
    
    # Group 3: Companies with medium completeness (50-79%)
    medium_completeness = df_with_completeness[
        (df_with_completeness['completeness_percentage'] >= 50) & 
        (df_with_completeness['completeness_percentage'] < 80)
    ]
    if not medium_completeness.empty:
        groups['medium_completeness'] = medium_completeness
    
    # Group 4: Companies with low completeness (<50%)
    low_completeness = df_with_completeness[df_with_completeness['completeness_percentage'] < 50]
    if not low_completeness.empty:
        groups['low_completeness'] = low_completeness
    
    return groups, df_with_completeness

def identify_binary_features(df):
    """Identify binary features in the dataset"""
    binary_features = []
    for col in df.columns:
        if df[col].dtype in ['object', 'string']:
            unique_values = df[col].dropna().unique()
            if len(unique_values) <= 2:
                binary_features.append(col)
        elif df[col].dtype in ['int64', 'float64']:
            unique_values = df[col].dropna().unique()
            if len(unique_values) <= 2:
                binary_features.append(col)
    return binary_features

def cluster_companies(df, group_name, n_clusters=3):
    """Cluster companies within a group based on non-binary features"""
    # Identify binary features
    binary_features = identify_binary_features(df)
    
    # Select only non-binary features for clustering
    numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
    non_binary_features = [col for col in numeric_features if col not in binary_features]
    
    if len(non_binary_features) < 2:
        return None, "Not enough non-binary numeric features for clustering"
    
    # Prepare data for clustering
    clustering_data = df[non_binary_features].fillna(df[non_binary_features].mean())
    
    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=min(n_clusters, len(clustering_data)), random_state=42)
    cluster_labels = kmeans.fit_predict(scaled_data)
    
    # Add cluster labels to dataframe
    df_with_clusters = df.copy()
    df_with_clusters['cluster'] = cluster_labels
    
    # Calculate cluster centers
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    
    return df_with_clusters, cluster_centers, non_binary_features

def detect_anomalies(df, feature_name):
    """Detect anomalies for a specific feature using IQR method"""
    if feature_name not in df.columns:
        return None
    
    feature_data = df[feature_name].dropna()
    if len(feature_data) == 0:
        return None
    
    Q1 = feature_data.quantile(0.25)
    Q3 = feature_data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    anomalies = df[
        (df[feature_name] < lower_bound) | 
        (df[feature_name] > upper_bound)
    ]
    
    return {
        'anomalies': anomalies,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR
    }

@app.before_request
def before_request():
    """Set language before each request"""
    if 'lang' not in session:
        session['lang'] = 'en'

@app.route('/')
def index():
    """Home page"""
    lang = session.get('lang', 'en')
    return render_template('index.html', lang=lang, get_text=get_text, get_language_name=get_language_name)

@app.route('/language/<lang>')
def change_language(lang):
    """Change language"""
    if lang in ['en', 'lt']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Data upload page"""
    global current_data, data_groups
    lang = session.get('lang', 'en')
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # Load and analyze data
                df = load_data(file_path)
                if df is not None:
                    current_data = df
                    data_groups, _ = analyze_data_completeness(df)
                    session['data_loaded'] = True
                    flash(f'File {filename} uploaded successfully! Data loaded with {len(df)} companies and {len(df.columns)} features.')
                    return redirect(url_for('analysis'))
                else:
                    flash('Error loading data from file. Please check the file format and try again.')
                    # Clean up the failed file
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    return redirect(request.url)
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                # Clean up the failed file
                if 'file_path' in locals() and os.path.exists(file_path):
                    os.remove(file_path)
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload Excel (.xlsx, .xls) or CSV (.csv) files.')
            return redirect(request.url)
    
    return render_template('upload.html', lang=lang, get_text=get_text, get_language_name=get_language_name)

@app.route('/analysis')
def analysis():
    """Data analysis and grouping page"""
    global current_data, data_groups
    lang = session.get('lang', 'en')
    
    if current_data is None:
        flash('No data loaded. Please upload a file first.')
        return redirect(url_for('upload'))
    
    # Get basic statistics
    total_companies = len(current_data)
    total_features = len(current_data.columns)
    
    # Calculate overall completeness
    overall_completeness = (current_data.notna().sum().sum() / (total_companies * total_features)) * 100
    
    # Get feature types
    numeric_features = current_data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = current_data.select_dtypes(include=['object']).columns.tolist()
    
    # Identify binary features
    binary_features = identify_binary_features(current_data)
    non_binary_features = [col for col in numeric_features if col not in binary_features]
    
    return render_template('analysis.html',
                         lang=lang,
                         get_text=get_text,
                         get_language_name=get_language_name,
                         total_companies=total_companies,
                         total_features=total_features,
                         overall_completeness=overall_completeness,
                         data_groups=data_groups,
                         numeric_features=numeric_features,
                         categorical_features=categorical_features,
                         binary_features=binary_features,
                         non_binary_features=non_binary_features)

@app.route('/clustering')
def clustering():
    """Company clustering page"""
    global current_data, data_groups
    lang = session.get('lang', 'en')
    
    if current_data is None:
        flash('No data loaded. Please upload a file first.')
        return redirect(url_for('upload'))
    
    return render_template('clustering.html', lang=lang, get_text=get_text, get_language_name=get_language_name, data_groups=data_groups)

@app.route('/cluster_group/<group_name>')
def cluster_group(group_name):
    """Cluster companies within a specific group"""
    global current_data, data_groups
    
    if current_data is None or data_groups is None:
        return jsonify({'error': 'No data available'})
    
    if group_name not in data_groups:
        return jsonify({'error': 'Group not found'})
    
    group_data = data_groups[group_name]
    
    # Get n_clusters from query parameters
    n_clusters = request.args.get('n_clusters', 3, type=int)
    
    clustered_data, cluster_centers, features_used = cluster_companies(group_data, group_name, n_clusters)
    
    if clustered_data is None:
        return jsonify({'error': features_used})
    
    # Prepare data for visualization
    cluster_summary = []
    for cluster_id in range(len(cluster_centers)):
        companies_in_cluster = clustered_data[clustered_data['cluster'] == cluster_id]
        cluster_summary.append({
            'cluster_id': cluster_id,
            'company_count': len(companies_in_cluster),
            'companies': companies_in_cluster.index.tolist()
        })
    
    return jsonify({
        'success': True,
        'group_name': group_name,
        'total_companies': len(group_data),
        'features_used': features_used,
        'cluster_summary': cluster_summary,
        'cluster_centers': cluster_centers.tolist()
    })

@app.route('/anomaly_detection')
def anomaly_detection():
    """Anomaly detection page"""
    global current_data
    lang = session.get('lang', 'en')
    
    if current_data is None:
        flash('No data loaded. Please upload a file first.')
        return redirect(url_for('upload'))
    
    # Get non-binary numeric features for anomaly detection
    binary_features = identify_binary_features(current_data)
    numeric_features = current_data.select_dtypes(include=[np.number]).columns.tolist()
    non_binary_features = [col for col in numeric_features if col not in binary_features]
    
    return render_template('anomaly_detection.html', lang=lang, get_text=get_text, get_language_name=get_language_name, features=non_binary_features)

@app.route('/detect_anomalies/<feature_name>')
def detect_anomalies_route(feature_name):
    """Detect anomalies for a specific feature"""
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data available'})
    
    anomalies_result = detect_anomalies(current_data, feature_name)
    
    if anomalies_result is None:
        return jsonify({'error': f'Feature {feature_name} not found or has no data'})
    
    # Prepare anomaly data for response
    anomaly_data = {
        'feature_name': feature_name,
        'anomaly_count': len(anomalies_result['anomalies']),
        'total_records': len(current_data[feature_name].dropna()),
        'anomaly_percentage': (len(anomalies_result['anomalies']) / len(current_data[feature_name].dropna())) * 100,
        'statistics': {
            'Q1': float(anomalies_result['Q1']),
            'Q3': float(anomalies_result['Q3']),
            'IQR': float(anomalies_result['IQR']),
            'lower_bound': float(anomalies_result['lower_bound']),
            'upper_bound': float(anomalies_result['upper_bound'])
        },
        'anomalies': anomalies_result['anomalies'].to_dict('records')
    }
    
    return jsonify(anomaly_data)

@app.route('/data_preview')
def data_preview():
    """Data preview page"""
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data available'})
    
    # Return first 100 rows and basic info
    preview_data = current_data.head(100).to_dict('records')
    columns_info = []
    
    for col in current_data.columns:
        col_info = {
            'name': col,
            'dtype': str(current_data[col].dtype),
            'non_null_count': int(current_data[col].notna().sum()),
            'null_count': int(current_data[col].isna().sum()),
            'unique_values': int(current_data[col].nunique())
        }
        
        if current_data[col].dtype in ['int64', 'float64']:
            col_info['min'] = float(current_data[col].min()) if not current_data[col].empty else None
            col_info['max'] = float(current_data[col].max()) if not current_data[col].empty else None
            col_info['mean'] = float(current_data[col].mean()) if not current_data[col].empty else None
        
        columns_info.append(col_info)
    
    return jsonify({
        'preview_data': preview_data,
        'columns_info': columns_info,
        'total_rows': len(current_data),
        'total_columns': len(current_data.columns)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
