# 🚀 Quick Start Guide - LogisticSmart

Welcome to LogisticSmart! This guide will help you get up and running in just a few minutes.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [First Run](#first-run)
- [Basic Usage](#basic-usage)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

Before starting, ensure you have:

- **Python 3.10+** installed
- **Git** for cloning the repository
- **Windows 10/11**, **macOS**, or **Linux**
- At least **4GB RAM** and **1GB free disk space**

### Check Python Version
```bash
python --version
# Should show Python 3.10.x or higher
```

## 📦 Installation

### Option 1: Quick Install (Recommended)
```bash
# Clone the repository
git clone https://github.com/NEO-SH1W4/LogisticSmart.git
cd LogisticSmart

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Development Install
```bash
# Clone for development
git clone https://github.com/NEO-SH1W4/LogisticSmart.git
cd LogisticSmart

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install all dependencies including dev tools
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 🎯 First Run

### 1. Start the Application
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Run the application
streamlit run app.py
```

### 2. Access the Application
- Open your browser and go to: `http://localhost:8501`
- You should see the LogisticSmart login screen

### 3. Login
Use these default credentials:
```
Username: admin
Password: admin123
```

> ⚠️ **Security Note**: Change default credentials in production!

## 📊 Basic Usage

### Upload Your First File

1. **Click on "Browse files"** in the sidebar
2. **Select an Excel or CSV file** with delivery data
3. **Wait for processing** - the system will automatically detect columns
4. **Review the detected structure** in the preview

### Expected File Format
Your file should contain columns like:
- **Delivery Date** (required)
- **Deliverer/Driver Name**
- **Status** (delivered, pending, etc.)
- **Destination/City**
- **Product Type**
- **Customer Name**

### Example Data Structure
```csv
Date,Deliverer,Status,City,Product,Customer
2024-01-15,John Smith,delivered,New York,Electronics,ABC Corp
2024-01-15,Jane Doe,pending,Los Angeles,Books,XYZ Inc
2024-01-16,John Smith,delivered,Chicago,Clothing,DEF Ltd
```

## 🎛️ Common Tasks

### Filter Data
1. **Use the sidebar filters** that appear after uploading
2. **Select date ranges** with the date picker
3. **Choose specific deliverers** from the dropdown
4. **Filter by status** (pending, delivered, all)

### Generate Reports
1. **Configure your filters** as needed
2. **View results** in the main dashboard
3. **Click "Export Excel"** to download
4. **Choose format**: Excel, CSV, or PDF

### View Analytics
1. **Navigate to the "Dashboard" tab**
2. **View interactive charts** showing:
   - Deliveries per driver
   - Status distribution
   - Timeline analysis
   - Performance metrics

### Quality Check
1. **Go to "Data Quality" tab**
2. **Review validation results**
3. **Follow recommendations** for data improvement

## 🔐 User Management

### Access Levels
- **👑 Admin**: Full access to all features
- **👤 User**: Upload, analyze, and export data
- **👁️ Visitor**: View-only access to reports

### Change Password
1. Contact an administrator
2. Or modify the authentication settings in `src/auth/authentication.py`

## 🛠️ Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear cache
pip cache purge
```

#### Upload Errors
- **File too large**: Maximum 200MB per file
- **Invalid format**: Use Excel (.xlsx) or CSV (.csv) only
- **Encoding issues**: Save CSV files with UTF-8 encoding

#### Performance Issues
- **Large files**: Try filtering data before upload
- **Memory errors**: Close other applications
- **Slow loading**: Check available disk space

#### Browser Issues
- **Clear browser cache**
- **Try incognito/private mode**
- **Use Chrome or Firefox** (recommended)

### Error Messages

| Error | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "Port already in use" | Use `streamlit run app.py --server.port 8502` |
| "File upload failed" | Check file format and size |
| "Authentication failed" | Verify username and password |

### Getting Help

1. **Check the logs** in the terminal where you started the app
2. **Review error messages** carefully
3. **Check GitHub Issues**: [LogisticSmart Issues](https://github.com/NEO-SH1W4/LogisticSmart/issues)
4. **Create a new issue** with:
   - Your operating system
   - Python version
   - Error message
   - Steps to reproduce

## 📈 Next Steps

### Explore Advanced Features
- **Custom filters** for complex queries
- **Batch processing** for multiple files
- **Scheduled reports** (coming soon)
- **API integration** (roadmap)

### Customize Your Setup
- **Modify themes** in `.streamlit/config.toml`
- **Add custom columns** in data processing
- **Configure authentication** for your organization

### Learn More
- 📖 [Full Documentation](../README.md)
- 🤝 [Contributing Guide](../CONTRIBUTING.md)
- 📋 [Changelog](../CHANGELOG.md)

## 🎯 Tips for Success

### Data Preparation
- **Consistent naming**: Use standard column names
- **Clean data**: Remove empty rows and invalid dates
- **Backup files**: Keep originals before processing

### Performance Optimization
- **Filter first**: Apply filters before complex operations
- **Batch processing**: Upload multiple files separately
- **Regular cleanup**: Clear browser cache periodically

### Best Practices
- **Regular backups**: Export important reports
- **User training**: Train team members on proper usage
- **Data validation**: Always review quality checks

---

## 🆘 Quick Reference

### Essential Commands
```bash
# Start application
streamlit run app.py

# Install dependencies
pip install -r requirements.txt

# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run tests
pytest

# Format code
black . && isort .
```

### Default Login
```
Username: admin
Password: admin123
```

### Supported File Types
- Excel (.xlsx, .xls)
- CSV (.csv)
- Maximum size: 200MB

---

🎉 **Congratulations!** You're now ready to use LogisticSmart for your logistics analysis needs.

For advanced usage and configuration, check our [complete documentation](../README.md).

