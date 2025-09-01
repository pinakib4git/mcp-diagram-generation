#!/usr/bin/env python3
"""Simple script to run the Streamlit MCP demo app"""

import subprocess
import sys
import os

def run_streamlit_app():
    """Run the Streamlit app"""
    try:
        # Change to project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
        
    except KeyboardInterrupt:
        print("\nApp stopped by user")
    except Exception as e:
        print(f"Error running app: {e}")

if __name__ == "__main__":
    run_streamlit_app()