import os
import subprocess
import sys

def build_linux_app():
    print("Building Linux app...")
    
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run PyInstaller with Linux-specific settings
    subprocess.run([
        'pyinstaller',
        '--noconfirm',
        '--clean',
        '--windowed',
        '--name=advent-of-habit',
        '--add-data=images:images',
        'habit_tracker.py'
    ], check=True)
    
    # Make the binary executable
    binary_path = os.path.join('dist', 'advent-of-habit', 'advent-of-habit')
    if os.path.exists(binary_path):
        os.chmod(binary_path, 0o755)
    
    print("Linux executable created at: dist/advent-of-habit/advent-of-habit")

if __name__ == '__main__':
    build_linux_app() 