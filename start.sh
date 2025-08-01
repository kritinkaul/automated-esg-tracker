#!/bin/bash

# Quick start script for ESG Data Tracker
echo "🚀 ESG Data Tracker Quick Start"
echo "================================"

# Check if we're in the right directory
if [ ! -f "collect_real_data.py" ]; then
    echo "❌ Error: Please run this from the project directory"
    echo "   Run: cd /Users/kritinkaul/automated-esg-tracker"
    echo "   Then: ./start.sh"
    exit 1
fi

echo "✅ Project directory confirmed"
echo "🎯 Starting interactive menu..."
echo ""

python3 run_esg_tracker.py
