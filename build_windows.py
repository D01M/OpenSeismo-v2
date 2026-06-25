"""
Build script for OpenSeismo Lite Windows Desktop Application
Creates a standalone executable using PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n{'='*60}")
    print(f"[BUILD] {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"\n❌ Error: {description} failed")
        return False
    print(f"✅ {description} completed")
    return True

def main():
    print("\n" + "="*60)
    print("OpenSeismo Lite Desktop Application Builder")
    print("="*60)
    
    # Get script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Step 1: Upgrade pip
    if not run_command(
        f'"{sys.executable}" -m pip install --upgrade pip',
        "Upgrading pip"
    ):
        return False
    
    # Step 2: Install dependencies
    if not run_command(
        f'"{sys.executable}" -m pip install -r requirements.txt',
        "Installing dependencies"
    ):
        return False
    
    # Step 3: Install PyInstaller
    if not run_command(
        f'"{sys.executable}" -m pip install pyinstaller',
        "Installing PyInstaller"
    ):
        return False
    
    # Step 4: Build with PyInstaller
    spec_file = str(script_dir / 'openseismo.spec')
    if not run_command(
        f'"{sys.executable}" -m PyInstaller --clean -y "{spec_file}"',
        "Building executable with PyInstaller"
    ):
        return False
    
    # Step 5: Check output
    exe_path = script_dir / 'dist' / 'OpenSeismo Lite.exe'
    if exe_path.exists():
        exe_size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ SUCCESS! Desktop executable created")
        print(f"   Location: {exe_path}")
        print(f"   Size: {exe_size_mb:.1f} MB")
        print(f"\n🚀 Run the application by double-clicking the executable")
        return True
    else:
        print(f"\n❌ ERROR: EXE not found at {exe_path}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
