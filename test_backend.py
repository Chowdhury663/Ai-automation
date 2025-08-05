#!/usr/bin/env python3
"""
Test script to check backend startup
"""

import sys
import os
import asyncio

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.main import app
    print("✅ Backend app imported successfully")
    
    # Test if we can create the app
    print("✅ App creation successful")
    
    # Test database connection
    from backend.database import engine
    print("✅ Database engine created")
    
    # Test AI manager
    from backend.core.ai_manager import AIManager
    print("✅ AI Manager imported")
    
    print("✅ All imports successful - backend should work!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()