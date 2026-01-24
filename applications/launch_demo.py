#!/usr/bin/env python3
"""
Auto-launcher for contract translation demo
Starts the Flask API server and opens demo.html in browser

Environment Variables:
- USE_MODULAR_CORE: Set to 'false' to use legacy agentic_implementation.py (default: 'true')
  Example: USE_MODULAR_CORE=false python launch_demo.py
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Get the workspace root (parent of where this script is)
workspace_root = Path(__file__).parent.absolute()

# Check which implementation to use
use_modular = os.getenv('USE_MODULAR_CORE', 'true').lower() not in ('false', '0', 'no')
impl_mode = "Modular Core Package" if use_modular else "Legacy Monolithic"

print("\n" + "="*70)
print("IBM Agentics - Smart Contract Translator (Research Edition)")
print("   Dataset-Driven Quality Evaluation")
print(f"   Implementation: {impl_mode}")
print("="*70 + "\n")

# Ensure required packages are installed
print("Checking dependencies...")
required_packages = {
    'flask': 'flask',
    'flask_cors': 'flask-cors',
    'fastmcp': 'fastmcp',
    'agentics': 'agentics',
    'PyPDF2': 'PyPDF2',
    'pydantic': 'pydantic'
}

for import_name, pip_name in required_packages.items():
    try:
        __import__(import_name)
        print(f"   {pip_name}")
    except ImportError:
        print(f"   Installing {pip_name}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pip_name, '-q'])
        print(f"   {pip_name} installed")

print("\nAll dependencies ready!\n")

# Add paths - make sure they're absolute
mcp_dir = workspace_root / "mcp"
contract_translator_dir = workspace_root / "contract-translator"
demo_file = contract_translator_dir / "demo.html"

print("Workspace Paths:")
print(f"   Root: {workspace_root}")
print(f"   Demo: {demo_file}")

# Check if demo.html and sampler.html exist
sampler_file = contract_translator_dir / "sampler.html"

if not demo_file.exists():
    print(f"\nError: demo.html not found at {demo_file}")
    sys.exit(1)

if not sampler_file.exists():
    print(f"\nWarning: sampler.html not found at {sampler_file}")
    print("   Dataset browser will not be available.\n")
else:
    print(f"   Demo files found (demo.html + sampler.html)\n")

# Start HTTP server for demo.html in background thread
print("Starting servers...\n")

class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress the default HTTP server logging
        pass

def start_http_server():
    os.chdir(str(contract_translator_dir))
    server = HTTPServer(('localhost', 8000), QuietHTTPRequestHandler)
    server.serve_forever()

http_thread = threading.Thread(daemon=True, target=start_http_server)
http_thread.start()

print("   [1/3] HTTP server starting on http://localhost:8000")

# Start the translation API in background
print(f"   [2/3] Translation API starting on http://localhost:5000 ({impl_mode})\n")
try:
    # Pass environment variable to child process
    env = os.environ.copy()
    env['USE_MODULAR_CORE'] = 'true' if use_modular else 'false'
    
    # Use Popen to start in FOREGROUND so we can see logs
    chatbot_process = subprocess.Popen(
        [sys.executable, str(mcp_dir / "chatbot_api.py")],
        cwd=str(workspace_root),
        env=env
    )
    
    # Wait for HTTP server to be ready before opening browser
    print("Waiting for servers to initialize")
    
    import socket
    def wait_for_server(host, port, timeout=10):
        """Wait until server is accepting connections"""
        start = time.time()
        while time.time() - start < timeout:
            try:
                with socket.create_connection((host, port), timeout=1):
                    return True
            except (socket.error, ConnectionRefusedError):
                time.sleep(0.2)
        return False
    
    # Wait for HTTP server (port 8000)
    if wait_for_server('localhost', 8000, timeout=5):
        print("   HTTP server ready on port 8000")
    else:
        print("   HTTP server slow to start, continuing anyway...")
    
    # Wait for Flask API (port 5000) to be ready
    if wait_for_server('localhost', 5000, timeout=10):
        print("   Flask API ready on port 5000")
    else:
        print("   Flask API slow to start, continuing anyway...")
    
    print("\n   [3/3] Opening demo pages in browser\n")
    demo_url = "http://localhost:8000/demo.html"
    sampler_url = "http://localhost:8000/sampler.html"
    
    try:
        webbrowser.open(demo_url)
        print(f"   Demo opened: {demo_url}")
        time.sleep(1)  # Small delay between opens
        webbrowser.open(sampler_url)
        print(f"   Sampler opened: {sampler_url}\n")
    except Exception as e:
        print(f"   Could not open browser automatically")
        print(f"   → Please open manually:")
        print(f"      Demo: {demo_url}")
        print(f"      Sampler: {sampler_url}\n")
    
    print("="*70)
    print("DEMO IS READY!")
    print("="*70)
    print("\nWhat's running:")
    print("   • Translation Demo: http://localhost:8000/demo.html")
    print("   • Dataset Browser: http://localhost:8000/sampler.html")
    print(f"   • Translation API: http://localhost:5000 ({impl_mode})")
    if not use_modular:
        print("\nUsing LEGACY implementation. Set USE_MODULAR_CORE=true to use new modular core.")
    else:
        print("\nUsing MODULAR core package. Set USE_MODULAR_CORE=false to use legacy version.")
    print("\nResearch Workflow:")
    print("   1. Browse dataset: http://localhost:8000/sampler.html")
    print("   2. Click 'Open in Demo' to load a contract")
    print("   3. Or paste text directly at: http://localhost:8000/demo.html")
    print("   4. Translate & evaluate generated Solidity contracts")
    print("\nDataset: requirement_fsm_code.jsonl (21,976 contracts)")
    print("\nLogs below (Ctrl+C to stop):\n")
    
    # Keep the process alive
    chatbot_process.wait()

except KeyboardInterrupt:
    print("\n\nShutting down...")
    chatbot_process.terminate()
    try:
        chatbot_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        chatbot_process.kill()
    print("Server stopped")
    sys.exit(0)
except Exception as e:
    print(f"Failed to start translation API: {e}")
    sys.exit(1)
