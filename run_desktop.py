"""
OpenSeismo Lite Desktop Launcher
Entry point for Windows executable (PyInstaller)
Launches the Flask server and opens the application in the default browser
"""

import subprocess
import webbrowser
import time
import sys
import os
import socket
from pathlib import Path

# Global lock file for preventing multiple instances
LOCK_FILE = None


def get_lock_file():
    """Get the lock file path"""
    temp_dir = Path(os.environ.get('TEMP', '/tmp'))
    return temp_dir / 'OpenSeismoLite.lock'


def acquire_lock():
    """Try to acquire a lock to prevent multiple launches"""
    global LOCK_FILE
    LOCK_FILE = get_lock_file()
    
    # Check if lock file exists and if process is still running
    if LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, 'r') as f:
                old_pid = f.read().strip()
                # On Windows, checking PID is unreliable, use file age instead
                import time as time_module
                file_age = time_module.time() - LOCK_FILE.stat().st_mtime
                if file_age > 10:  # If lock is older than 10 seconds, consider it stale
                    LOCK_FILE.unlink()
        except:
            pass
    
    # Try to create lock file
    if not LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, 'w') as f:
                f.write(str(os.getpid()))
            return True
        except:
            return False
    
    return False


def is_port_in_use(port, timeout=1):
    """Check if a port is already in use"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex(('127.0.0.1', port))
            return result == 0
    except:
        return False


def main():
    """Launch the Flask server and open browser"""
    
    port = 5000
    url = f"http://localhost:{port}"
    
    # Try to acquire lock to prevent multiple instances
    if not acquire_lock():
        print("OpenSeismo Lite is already running.")
        print(f"Connecting to {url}")
        time.sleep(1)
        webbrowser.open(url)
        return
    
    try:
        # Check if server is already running
        if is_port_in_use(port):
            print(f"OpenSeismo Lite is already running on {url}")
            webbrowser.open(url)
            return
        
        print("Starting OpenSeismo Lite...")
        print(f"Launching server on {url}")
        
        # Import and run the Flask app
        from openseismo.app import run_app
        from openseismo.config import FLASK_HOST, FLASK_PORT
        
        # Open browser after a short delay to let server start
        def open_browser():
            time.sleep(2)
            webbrowser.open(url)
        
        # Start browser in background thread
        import threading
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Start Flask server (blocking)
        run_app(host=FLASK_HOST, port=FLASK_PORT, debug=False)
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up lock file
        if LOCK_FILE and LOCK_FILE.exists():
            try:
                LOCK_FILE.unlink()
            except:
                pass


if __name__ == '__main__':
    main()
