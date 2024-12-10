import os
import subprocess
import sys

def build_windows_app():
    print("Building Windows app...")
    
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run PyInstaller with Windows-specific spec file
    subprocess.run([
        'pyinstaller',
        '--noconfirm',
        '--clean',
        '--windowed',
        '--name=Advent of Habit',
        '--icon=images/icon.ico',
        '--add-data=images;images',
        'habit_tracker.py'
    ], check=True)
    
    print("Windows executable created at: dist/Advent of Habit/Advent of Habit.exe")

if __name__ == '__main__':
    build_windows_app() 