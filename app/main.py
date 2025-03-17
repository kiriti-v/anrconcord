import uvicorn
import subprocess
import sys
import os
import time
import threading
import socket
from app.utils.logger import logger
from app.utils.config import API_HOST, API_PORT, DASHBOARD_PORT

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_api():
    """Start the FastAPI server"""
    if is_port_in_use(API_PORT):
        logger.info(f"API server already running on port {API_PORT}")
        return
        
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    # Use subprocess instead of direct uvicorn.run to avoid threading issues
    subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.api.main:app",
        "--host", API_HOST,
        "--port", str(API_PORT),
        "--reload"
    ])

def start_dashboard():
    """Start the Streamlit dashboard"""
    if is_port_in_use(DASHBOARD_PORT):
        logger.info(f"Dashboard already running on port {DASHBOARD_PORT}")
        return
        
    logger.info(f"Starting Streamlit dashboard on port {DASHBOARD_PORT}")
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard", "app.py")
    subprocess.run([
        "streamlit", "run", dashboard_path,
        "--server.port", str(DASHBOARD_PORT),
        "--server.address", "0.0.0.0"
    ])

def main():
    """Main entry point for the application"""
    logger.info("Starting Emerging Artist Discovery Tool")
    
    # Start API using subprocess
    start_api()
    
    # Give the API time to start
    time.sleep(2)
    
    # Start dashboard in the main thread
    start_dashboard()

if __name__ == "__main__":
    main() 