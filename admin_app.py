#!/usr/bin/env python3
"""
AI Automation Platform - Admin Control Panel
A command-line interface to manage the AI Automation Platform
"""

import os
import sys
import time
import subprocess
import signal
import psutil
import requests
import json
from datetime import datetime
from pathlib import Path

class PlatformAdmin:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_port = 8000
        self.frontend_port = 3000
        self.redis_port = 6379
        self.processes = {}
        
    def print_banner(self):
        """Print the admin app banner"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                AI Automation Platform - Admin Panel           ║
║                                                              ║
║  🚀 Manage your AI Automation Platform from one place       ║
║  📊 Monitor services, start/stop components                ║
║  🔧 Configure and maintain your platform                   ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def check_services(self):
        """Check the status of all services"""
        print("\n🔍 Checking service status...")
        
        services = {
            "Backend (FastAPI)": f"http://localhost:{self.backend_port}",
            "Frontend (React)": f"http://localhost:{self.frontend_port}",
            "Redis": f"localhost:{self.redis_port}"
        }
        
        for service_name, endpoint in services.items():
            status = self.check_service_status(endpoint, service_name)
            print(f"  {service_name}: {status}")
    
    def check_service_status(self, endpoint, service_name):
        """Check if a service is running"""
        try:
            if "redis" in service_name.lower():
                # Check Redis process
                for proc in psutil.process_iter(['pid', 'name']):
                    if 'redis' in proc.info['name'].lower():
                        return "✅ Running"
                return "❌ Not running"
            else:
                # Check HTTP service
                response = requests.get(f"{endpoint}/health", timeout=5)
                if response.status_code == 200:
                    return "✅ Running"
                else:
                    return "⚠️  Responding but not healthy"
        except requests.exceptions.ConnectionError:
            return "❌ Not running"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def start_backend(self):
        """Start the backend server"""
        print("\n🚀 Starting backend server...")
        
        # Check if backend is already running
        if self.is_backend_running():
            print("  ⚠️  Backend is already running!")
            return
        
        try:
            # Activate virtual environment and start backend
            cmd = [
                "bash", "-c", 
                f"cd {self.project_root} && source venv/bin/activate && uvicorn backend.main:app --host 0.0.0.0 --port {self.backend_port}"
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            self.processes['backend'] = process
            print("  ✅ Backend started successfully!")
            print(f"  📍 API available at: http://localhost:{self.backend_port}")
            print(f"  📚 API docs at: http://localhost:{self.backend_port}/docs")
            
        except Exception as e:
            print(f"  ❌ Failed to start backend: {e}")
    
    def start_frontend(self):
        """Start the frontend server"""
        print("\n🚀 Starting frontend server...")
        
        # Check if frontend is already running
        if self.is_frontend_running():
            print("  ⚠️  Frontend is already running!")
            return
        
        try:
            # Start React development server
            cmd = [
                "bash", "-c", 
                f"cd {self.project_root} && npm start"
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            self.processes['frontend'] = process
            print("  ✅ Frontend started successfully!")
            print(f"  📍 Available at: http://localhost:{self.frontend_port}")
            
        except Exception as e:
            print(f"  ❌ Failed to start frontend: {e}")
    
    def start_redis(self):
        """Start Redis server"""
        print("\n🚀 Starting Redis server...")
        
        try:
            # Check if Redis is already running
            for proc in psutil.process_iter(['pid', 'name']):
                if 'redis' in proc.info['name'].lower():
                    print("  ⚠️  Redis is already running!")
                    return
            
            # Start Redis
            subprocess.run(["sudo", "service", "redis-server", "start"], check=True)
            print("  ✅ Redis started successfully!")
            
        except subprocess.CalledProcessError:
            print("  ❌ Failed to start Redis. Trying to install...")
            try:
                subprocess.run(["sudo", "apt", "install", "-y", "redis-server"], check=True)
                subprocess.run(["sudo", "service", "redis-server", "start"], check=True)
                print("  ✅ Redis installed and started successfully!")
            except Exception as e:
                print(f"  ❌ Failed to install/start Redis: {e}")
        except Exception as e:
            print(f"  ❌ Failed to start Redis: {e}")
    
    def is_backend_running(self):
        """Check if backend is running"""
        try:
            response = requests.get(f"http://localhost:{self.backend_port}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def is_frontend_running(self):
        """Check if frontend is running"""
        try:
            response = requests.get(f"http://localhost:{self.frontend_port}", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def stop_backend(self):
        """Stop the backend server"""
        print("\n🛑 Stopping backend server...")
        
        try:
            # Kill processes using the backend port
            subprocess.run(["fuser", "-k", f"{self.backend_port}/tcp"], 
                         capture_output=True, text=True)
            print("  ✅ Backend stopped successfully!")
        except Exception as e:
            print(f"  ❌ Failed to stop backend: {e}")
    
    def stop_frontend(self):
        """Stop the frontend server"""
        print("\n🛑 Stopping frontend server...")
        
        try:
            # Kill React development server
            subprocess.run(["pkill", "-f", "react-scripts"], 
                         capture_output=True, text=True)
            print("  ✅ Frontend stopped successfully!")
        except Exception as e:
            print(f"  ❌ Failed to stop frontend: {e}")
    
    def stop_redis(self):
        """Stop Redis server"""
        print("\n🛑 Stopping Redis server...")
        
        try:
            subprocess.run(["sudo", "service", "redis-server", "stop"], check=True)
            print("  ✅ Redis stopped successfully!")
        except Exception as e:
            print(f"  ❌ Failed to stop Redis: {e}")
    
    def restart_all(self):
        """Restart all services"""
        print("\n🔄 Restarting all services...")
        self.stop_all()
        time.sleep(2)
        self.start_all()
    
    def start_all(self):
        """Start all services"""
        print("\n🚀 Starting all services...")
        self.start_redis()
        time.sleep(2)
        self.start_backend()
        time.sleep(3)
        self.start_frontend()
        time.sleep(3)
        self.check_services()
    
    def stop_all(self):
        """Stop all services"""
        print("\n🛑 Stopping all services...")
        self.stop_backend()
        self.stop_frontend()
        self.stop_redis()
    
    def show_logs(self, service="backend"):
        """Show logs for a specific service"""
        print(f"\n📋 Showing logs for {service}...")
        
        if service == "backend":
            # Show backend logs
            try:
                subprocess.run(["tail", "-f", "/var/log/syslog"], 
                             text=True, check=True)
            except KeyboardInterrupt:
                print("\n  ⏹️  Log viewing stopped")
            except Exception as e:
                print(f"  ❌ Error showing logs: {e}")
        else:
            print(f"  ❌ Log viewing for {service} not implemented yet")
    
    def show_admin_info(self):
        """Show admin user information"""
        print("\n👤 Admin User Information:")
        print("  Username: admin")
        print("  Email: admin@ai-automation.com")
        print("  Password: admin123")
        print("  Role: Administrator")
        print("  Status: Active")
        print("\n🔗 Access URLs:")
        print(f"  Frontend: http://localhost:{self.frontend_port}")
        print(f"  Backend API: http://localhost:{self.backend_port}")
        print(f"  API Docs: http://localhost:{self.backend_port}/docs")
    
    def show_system_info(self):
        """Show system information"""
        print("\n💻 System Information:")
        
        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        print(f"  CPU Usage: {cpu_percent}%")
        print(f"  Memory Usage: {memory.percent}%")
        print(f"  Available Memory: {memory.available / (1024**3):.1f} GB")
        
        # Disk usage
        disk = psutil.disk_usage('/')
        print(f"  Disk Usage: {disk.percent}%")
        print(f"  Available Disk: {disk.free / (1024**3):.1f} GB")
        
        # Network
        network = psutil.net_io_counters()
        print(f"  Network Bytes Sent: {network.bytes_sent / (1024**2):.1f} MB")
        print(f"  Network Bytes Received: {network.bytes_recv / (1024**2):.1f} MB")
    
    def show_menu(self):
        """Show the main menu"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                        ADMIN MENU                            ║
╠══════════════════════════════════════════════════════════════╣
║  1. 📊 Check Service Status                                 ║
║  2. 🚀 Start All Services                                   ║
║  3. 🛑 Stop All Services                                    ║
║  4. 🔄 Restart All Services                                 ║
║  5. 🚀 Start Backend Only                                   ║
║  6. 🚀 Start Frontend Only                                  ║
║  7. 🛑 Stop Backend Only                                    ║
║  8. 🛑 Stop Frontend Only                                   ║
║  9. 👤 Show Admin Info                                      ║
║  10. 💻 Show System Info                                    ║
║  11. 📋 Show Logs                                           ║
║  12. 🧹 Clean Up (Kill all processes)                      ║
║  0. 🚪 Exit                                                 ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def run(self):
        """Run the admin app"""
        self.print_banner()
        
        while True:
            self.show_menu()
            
            try:
                choice = input("Enter your choice (0-12): ").strip()
                
                if choice == "0":
                    print("\n👋 Goodbye! Exiting admin panel...")
                    break
                elif choice == "1":
                    self.check_services()
                elif choice == "2":
                    self.start_all()
                elif choice == "3":
                    self.stop_all()
                elif choice == "4":
                    self.restart_all()
                elif choice == "5":
                    self.start_backend()
                elif choice == "6":
                    self.start_frontend()
                elif choice == "7":
                    self.stop_backend()
                elif choice == "8":
                    self.stop_frontend()
                elif choice == "9":
                    self.show_admin_info()
                elif choice == "10":
                    self.show_system_info()
                elif choice == "11":
                    service = input("Enter service name (backend/frontend): ").strip()
                    self.show_logs(service)
                elif choice == "12":
                    print("\n🧹 Cleaning up all processes...")
                    self.stop_all()
                    subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True)
                    subprocess.run(["pkill", "-f", "react-scripts"], capture_output=True)
                    print("  ✅ All processes cleaned up!")
                else:
                    print("❌ Invalid choice. Please try again.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Exiting admin panel...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")

if __name__ == "__main__":
    admin = PlatformAdmin()
    admin.run()