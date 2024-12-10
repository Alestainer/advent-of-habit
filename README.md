# Advent of Habit

A minimalist habit tracker that helps you build and maintain daily habits. It automatically appears during your chosen time window (morning or evening) and stays on top of other windows until you've checked off your habits for the day.

## Features

- 🎯 Track up to 3 daily habits
- ⏰ Choose your preferred check-in time (morning 6-11 AM or evening 6-11 PM)
- 📊 Shows completion ratio for the last 21 days (e.g., "15/21" means completed 15 out of the last 21 days)
- 📅 Calendar view to visualize your progress
- 🔝 Stays on top of other windows until minimized
- 🔄 Minimizes to system tray/menu bar for easy access
- 💾 Automatically saves your progress
- 🎨 Clean, modern interface
- 💻 Cross-platform support (macOS, Windows, Linux)

## Installation

### Option 1: Run from Repository (Recommended)
1. Clone or download this repository
2. Navigate to the `dist` folder
3. Run the appropriate version for your system:
   - macOS: Double-click `Advent of Habit.app`
   - Windows: Double-click `Advent of Habit.exe` in the `Advent of Habit` folder
   - Linux: Run `advent-of-habit`
4. Optional: Add to startup applications

### Option 2: Build from Source

#### Prerequisites

**Windows:**
1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/windows/)
   - During installation, check "Add Python to PATH"
   - Check "Install pip"
2. Install Git from [git-scm.com](https://git-scm.com/download/win)
3. Install Visual Studio Build Tools with C++ workload (required for some dependencies)
   - Download from [visualstudio.microsoft.com](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Select "Desktop development with C++"

**macOS:**
- Python 3.8+ (via Homebrew or python.org)
- Xcode Command Line Tools

**Linux:**
- Python 3.8+
- Qt development packages:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev qt6-base-dev

# Fedora
sudo dnf install python3-devel qt6-qtbase-devel
```

#### Build Steps

1. Clone this repository:
```bash
git clone https://github.com/yourusername/advent-of-habit.git
cd advent-of-habit
```

2. Create and activate a virtual environment:

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Build the app for your platform:

**Windows:**
```cmd
# Command Prompt
python build_windows.py

# PowerShell
python.exe .\build_windows.py
```

**macOS:**
```bash
chmod +x build_macos_app.sh
./build_macos_app.sh
```

**Linux:**
```bash
python build_linux.py
```

The app will be created in the `dist` directory:
- Windows: `dist/Advent of Habit/Advent of Habit.exe`
- macOS: `dist/Advent of Habit.app`
- Linux: `dist/advent-of-habit/advent-of-habit`

#### Adding to Startup (Optional)

**Windows:**
1. Press `Win + R`
2. Type `shell:startup`
3. Create a shortcut to `Advent of Habit.exe` in this folder

**macOS:**
1. System Settings → Users & Groups → Login Items
2. Click + and select `Advent of Habit.app`

**Linux:**
1. Copy `advent-of-habit.desktop` to `~/.config/autostart/`

## Usage

### First Launch
1. When you first launch the app, you'll see a welcome screen
2. Enter up to 3 habits you want to track
3. Default suggestions are provided (Meditation, Journaling, Exercise)
4. Choose your preferred check-in time:
   - Morning (6-11 AM)
   - Evening (6-11 PM)
5. Click "Start Tracking" to begin

### Daily Usage
1. The app appears automatically during your chosen time window
2. Check off habits as you complete them
3. Click ✕ to minimize to system tray/menu bar
4. Click the icon in the system tray/menu bar to show the window again
5. Progress is saved automatically

### Calendar View
- Switch to the "Calendar" tab to see your progress over time
- Select a habit to view its completion history
- Green dates indicate completed habits
- Red dates indicate missed habits

### Understanding the Numbers
- Each habit shows a ratio like "7/21"
- First number: Days completed in the last 21 days
- Second number: Total days tracked
- This helps you see your consistency over time

### System Tray/Menu Bar Options
- Click the icon to show the window
- Right-click for additional options:
  - Show Window
  - Quit

## Data Storage

Your data is stored locally at:

**Windows:**
```
%APPDATA%\Advent of Habit\
```
- `config.json`: Your habit settings and time preference
- `habit_data.json`: Your daily progress

**macOS:**
```
~/Library/Application Support/Advent of Habit/
```

**Linux:**
```
~/.local/share/advent-of-habit/
```

## System Requirements

**Windows:**
- Windows 10 or newer
- 4GB RAM minimum
- 100MB free disk space
- Python 3.8+ (for building from source)
- Visual Studio Build Tools (for building from source)

**macOS:**
- macOS 10.15 (Catalina) or newer
- 4GB RAM minimum
- 100MB free disk space
- Python 3.8+ (for building from source)

**Linux:**
- Modern Linux distribution (Ubuntu 20.04+, Fedora 34+, etc.)
- X11 or Wayland
- 4GB RAM minimum
- 100MB free disk space
- Python 3.8+ (for building from source)
- Qt6 development packages

## Troubleshooting

### Windows-Specific Issues

#### App Won't Start
1. Check Windows Event Viewer for errors
2. Try running as administrator
3. Verify Microsoft Visual C++ Redistributable is installed
4. Clear app data:
```cmd
rd /s /q "%APPDATA%\Advent of Habit"
```

#### Missing DLL Errors
Install Microsoft Visual C++ Redistributable:
1. Download from [Microsoft's website](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Run the installer
3. Restart your computer

#### Other Issues
1. Delete the app
2. Remove the configuration directory:
```cmd
rd /s /q "%APPDATA%\Advent of Habit"
```
3. Reinstall the app

### macOS-Specific Issues

Try removing the configuration directory:
```bash
rm -rf ~/Library/Application\ Support/Advent\ of\ Habit
```

### Linux-Specific Issues

Try removing the configuration directory:
```bash
rm -rf ~/.local/share/advent-of-habit
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- Built with PyQt6
- Icons and styling inspired by platform design guidelines
- Special thanks to the open source community