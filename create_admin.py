#!/usr/bin/env python3
"""
Admin User Creation Script
Automatically creates an admin user for the AI Automation Platform
"""

import os
import sys
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import User, Base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_admin_user():
    """Create an admin user with default credentials"""
    
    # Default admin credentials
    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "admin@ai-automation.com"
    ADMIN_PASSWORD = "admin123"  # Change this in production!
    
    # Database connection
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ubuntu:ubuntu@localhost:5432/ai_automation_db")
    
    try:
        # Create engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        
        # Check if admin user already exists
        existing_user = db.query(User).filter(User.username == ADMIN_USERNAME).first()
        
        if existing_user:
            print(f"✅ Admin user '{ADMIN_USERNAME}' already exists!")
            print(f"   User ID: {existing_user.id}")
            print(f"   Is Admin: {existing_user.is_admin}")
            print(f"   Email: {existing_user.email}")
            
            # Make sure the user is an admin
            if not existing_user.is_admin:
                existing_user.is_admin = True
                db.commit()
                print(f"   ✅ Updated user '{ADMIN_USERNAME}' to admin status")
            
            db.close()
            return
        
        # Create new admin user
        hashed_password = get_password_hash(ADMIN_PASSWORD)
        
        admin_user = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            hashed_password=hashed_password,
            is_active=True,
            is_admin=True,
            created_at=datetime.now()
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"   Username: {ADMIN_USERNAME}")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"   User ID: {admin_user.id}")
        print(f"   Is Admin: {admin_user.is_admin}")
        print("\n⚠️  IMPORTANT: Change the default password in production!")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your DATABASE_URL in .env file")
        print("3. Ensure the database 'ai_automation_db' exists")
        sys.exit(1)

def test_admin_login():
    """Test the admin login functionality"""
    print("\n🔐 Testing admin login...")
    
    import requests
    
    try:
        # Test login
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Admin login successful!")
            print(f"   Access Token: {token_data['access_token'][:50]}...")
            
            # Test admin endpoint
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            users_response = requests.get("http://localhost:8000/api/auth/users", headers=headers)
            
            if users_response.status_code == 200:
                print("✅ Admin endpoint access successful!")
                users = users_response.json()
                print(f"   Found {len(users)} users in system")
            else:
                print(f"❌ Admin endpoint access failed: {users_response.status_code}")
                
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("   Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error testing admin login: {str(e)}")

if __name__ == "__main__":
    print("🚀 AI Automation Platform - Admin User Creation")
    print("=" * 50)
    
    # Create admin user
    create_admin_user()
    
    # Test login
    test_admin_login()
    
    print("\n" + "=" * 50)
    print("📋 Admin User Summary:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Email: admin@ai-automation.com")
    print("   Role: Administrator")
    print("\n🔗 Access URLs:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("\n⚠️  SECURITY REMINDER:")
    print("   Change the default password in production!")
    print("   Update the email address if needed!")