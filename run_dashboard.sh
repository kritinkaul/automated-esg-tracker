#!/bin/bash

# ESG Data Tracker - Dashboard Runner
echo "🚀 ESG Data Tracker Dashboard"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "collect_real_data.py" ]; then
    echo "❌ Error: Please run this script from the automated-esg-tracker directory"
    echo "   Current directory: $(pwd)"
    echo "   Expected files: collect_real_data.py, src/visualization/main.py"
    echo ""
    echo "   To fix this, run:"
    echo "   cd /Users/kritinkaul/automated-esg-tracker"
    echo "   ./run_dashboard.sh"
    exit 1
fi

echo "✅ Directory check passed"
echo "📊 Starting Streamlit dashboard..."

# Run the dashboard
streamlit run src/visualization/main.py
