import os
import sys
import subprocess

def install_if_missing(package):
    """Install a package if it's not already installed"""
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} installed successfully!")

# Install required packages if missing
required_packages = ['streamlit', 'pandas', 'openpyxl', 'plotly']
for package in required_packages:
    install_if_missing(package)

# Now that we're sure all packages are installed, import them
import streamlit
import pandas
import plotly

def main():
    """Run the Streamlit dashboard"""
    print("Starting LNC Implementation Dashboard...")
    dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lnc_dashboard.py")
    subprocess.call([sys.executable, "-m", "streamlit", "run", dashboard_path])

if __name__ == "__main__":
    main()
