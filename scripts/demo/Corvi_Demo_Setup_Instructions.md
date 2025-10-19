# Corvi Demo Setup Instructions

## Quick Start Commands

### Run complete setup (this fixes everything)
```powershell
python complete_demo_fix.py --setup
```

### Or just check status
```powershell
python complete_demo_fix.py --status
```

### Or just fix database issues
```powershell
python complete_demo_fix.py --fix-db
```

---

## 🚀 Complete Corvi Demo Setup

This guide will walk you through setting up and running a complete Corvi demo, from service deployment to user creation and experiment execution using the automated setup script.

## 📋 Prerequisites

- **Docker & Docker Compose** installed and running
- **Git** installed
- **Python 3.11+** with pip
- **At least 4GB RAM** available
- **Available ports**: 80, 3000, 5000, 8000, 9000-9002
- **Windows PowerShell** or Command Prompt

## 🎯 One-Command Demo Setup

### 1. Navigate to Demo Directory
```powershell
cd c:\Workspace\AviariumSoftware\Corvi\corvi-saas\scripts\demo
```

### 2. Run Complete Setup
```powershell
python complete_demo_fix.py --setup
```

This single command will:
- ✅ Check Docker is running
- 🛑 Stop any existing services
- 🚀 Start all services fresh
- ⏳ Wait for services to be ready
- 🗄️ Fix database issues automatically
- 🧪 Test API functionality
- 📊 Create demo data files
- 🌐 Open browser to demo

## 📊 What Gets Created

### Demo Files Location
```
c:\Workspace\AviariumSoftware\Corvi\corvi-saas\demo_files\
├── iris_demo.csv           # Classification dataset (150 rows)
└── house_prices_demo.csv   # Regression dataset (200 rows)
```

### Demo User Account
- **Email**: `demo@corvi.ai`
- **Password**: `demo123`
- **Organization**: `Demo Organization`

### Service URLs
- **Main Application**: http://localhost
- **API Documentation**: http://localhost:8000/docs
- **MLflow Tracking**: http://localhost:5000
- **Grafana Monitoring**: http://localhost:3000 (admin/admin)

## 🔍 Verification Commands

### Check Service Status
```powershell
python complete_demo_fix.py --status
```

### Manual Service Check
```powershell
# Check Docker containers
docker ps

# Check specific services
curl http://localhost:8000/api/health
curl http://localhost
```

## 🧪 Demo Workflow

### 1. Access Web Interface
1. Open http://localhost in your browser
2. Login with: `demo@corvi.ai` / `demo123`
3. You should see the main dashboard

### 2. Create Your First Project
1. Click "New Project"
2. Name: "ML Demo Project"
3. Description: "Demo project for testing Corvi"
4. Click "Create"

### 3. Upload Demo Data
1. Go to "Datasets" section
2. Click "Upload Dataset"
3. Upload `demo_files/iris_demo.csv`:
   - Name: "Iris Classification Demo"
   - Target column: "species"
   - Type: Classification
4. Upload `demo_files/house_prices_demo.csv`:
   - Name: "House Prices Demo"
   - Target column: "price"
   - Type: Regression

### 4. Run Classification Experiment
1. Go to "Experiments" section
2. Click "New Experiment"
3. Configure:
   - **Name**: "Iris Species Classification"
   - **Dataset**: "Iris Classification Demo"
   - **Algorithm**: "Random Search"
   - **Model**: "Random Forest Classifier"
   - **Trials**: 15
   - **Objective**: "maximize accuracy"
4. Click "Start Experiment"
5. Monitor progress in real-time

### 5. Run Regression Experiment
1. Create another experiment:
   - **Name**: "House Price Prediction"
   - **Dataset**: "House Prices Demo"
   - **Algorithm**: "Bayesian Optimization"
   - **Model**: "Gradient Boosting Regressor"
   - **Trials**: 20
   - **Objective**: "minimize RMSE"
2. Start and monitor

### 6. View Results
1. Check experiment results in the web interface
2. View detailed tracking in MLflow: http://localhost:5000
3. Monitor system metrics in Grafana: http://localhost:3000

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Services Won't Start
```powershell
# Check Docker is running
docker --version

# Check available ports
netstat -an | findstr :8000

# Restart everything
python complete_demo_fix.py --setup
```

#### 2. Database Connection Issues
```powershell
# Fix database specifically
python complete_demo_fix.py --fix-db

# Check database logs
docker logs infra-postgres-1
```

#### 3. API Not Responding
```powershell
# Check API container
docker logs infra-api-1

# Test API health
curl http://localhost:8000/api/health
```

#### 4. Frontend Not Loading
```powershell
# Check nginx logs
docker logs infra-nginx-1

# Restart frontend
docker compose -f ../../infra/docker-compose.yml restart frontend nginx
```

#### 5. Python Dependencies Missing
```powershell
# Install required packages
pip install requests pandas numpy

# Or install all at once
pip install -r requirements.txt
```

### Manual Service Management

#### Stop All Services
```powershell
cd ../../
docker compose -f infra/docker-compose.yml down -v
```

#### Start All Services
```powershell
docker compose -f infra/docker-compose.yml up -d --build
```

#### Check Service Logs
```powershell
# All services
docker compose -f infra/docker-compose.yml logs

# Specific service
docker logs infra-api-1
docker logs infra-postgres-1
docker logs infra-frontend-1
```

## 📁 File Structure Reference

```
c:\Workspace\AviariumSoftware\Corvi\corvi-saas\
├── scripts\demo\
│   ├── complete_demo_fix.py                  # 🔧 Main setup script
│   └── Corvi_Demo_Setup_Instructions.md      # 📚 This file
├── infra\
│   └── docker-compose.yml                    # 🐳 Service definitions
├── demo_files\                               # 📊 Generated demo data
│   ├── iris_demo.csv
│   └── house_prices_demo.csv
└── ...other project files
```

## 🎯 Success Criteria

A successful demo should show:

- ✅ **User Registration/Login**: Working authentication
- ✅ **Data Upload**: CSV file upload and validation
- ✅ **Project Creation**: Organizing experiments
- ✅ **Experiment Configuration**: Setting up ML experiments
- ✅ **Real-time Monitoring**: Live progress tracking
- ✅ **Results Visualization**: Performance metrics and plots
- ✅ **MLflow Integration**: Detailed experiment tracking
- ✅ **Multi-service Architecture**: All components working together

## 🕐 Demo Timeline

### Quick Demo (10 minutes)
1. **Setup** (2 min): Run `complete_demo_fix.py --setup`
2. **Login** (1 min): Access web interface
3. **Upload Data** (2 min): Upload demo CSV files
4. **Start Experiment** (2 min): Configure and launch
5. **Show Results** (3 min): Real-time monitoring and MLflow

### Full Demo (30 minutes)
1. **Introduction** (3 min): Architecture overview
2. **Setup** (3 min): Live setup demonstration
3. **User Management** (3 min): Registration and login
4. **Data Management** (5 min): Upload and data preview
5. **Experiment Setup** (5 min): Configuration options
6. **Live Monitoring** (8 min): Real-time tracking
7. **Results Analysis** (3 min): Performance analysis and export

## 🔄 Reset Demo Environment

To start fresh:

```powershell
# Complete reset
python complete_demo_fix.py --setup

# Or manual reset
cd ../../
docker compose -f infra/docker-compose.yml down -v
docker volume prune -f
rm -rf demo_files/
python scripts/demo/complete_demo_fix.py --setup
```

## 📞 Support

If you encounter issues:

1. **Check the status**: `python complete_demo_fix.py --status`
2. **Review logs**: `docker compose -f ../../infra/docker-compose.yml logs`
3. **Restart services**: `python complete_demo_fix.py --setup`
4. **Check this guide**: Look for your specific issue in troubleshooting
5. **Contact support**: Provide the output of status check and error logs

## 🎉 You're Ready!

After running the setup script successfully, your Corvi demo environment is fully operational. You can now:

- **Demonstrate the complete ML workflow**
- **Show real-time experiment tracking**
- **Highlight the intuitive web interface**
- **Showcase integration capabilities**
- **Present scalable architecture**

**Access your demo at: http://localhost**

**Demo credentials: demo@corvi.ai / demo123**

---

*For advanced configuration, API usage, or production deployment, please refer to the main project documentation.*