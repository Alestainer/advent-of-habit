# Advent of Habit

A minimalist habit tracker that helps you build and maintain daily habits. It automatically appears during your chosen time window (morning or evening) and stays on top of other windows until you've checked off your habits for the day.

## Features

- 🎯 Track up to 3 daily habits
- ⏰ Choose your preferred check-in time (morning 6-11 AM or evening 6-11 PM)
- 📊 Shows completion ratio for the last 21 days (e.g., "15/21" means completed 15 out of the last 21 days)
- 📅 Calendar view to visualize your progress
- 🔝 Stays on top of other windows until minimized
- 🔄 Minimizes to a green checkmark in your menu bar for easy access
- 💾 Automatically saves your progress
- 🎨 Clean, modern interface

## Installation

### Option 1: Run from Repository (Recommended)
1. Clone or download this repository
2. Navigate to the `dist` folder
3. Double-click `Advent of Habit.app`
4. Optional: Move to Applications folder and add to Login Items

### Option 2: Build from Source
1. Ensure you have Python 3.8+ installed
2. Clone this repository:
```bash
git clone https://github.com/alestainer/advent-of-habit.git
cd advent-of-habit
```

3. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Build the app:
```bash
chmod +x build_macos_app.sh
./build_macos_app.sh
```

The app will be created at `dist/Advent of Habit.app`. You can then:
- Run it directly from the `dist` folder
- Move it to your Applications folder
- Add it to Login Items for automatic startup

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
3. Click ✕ to minimize to menu bar
4. Click the green checkmark in the menu bar to show the window again
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

### Menu Bar Options
- Click the green checkmark icon to show the window
- Right-click for additional options:
  - Show Window
  - Quit

## Data Storage

Your data is stored locally at:
```
~/Library/Application Support/Advent of Habit/
├── config.json         # Your habit settings and time preference
└── habit_data.json    # Your daily progress
```

## System Requirements

- macOS 10.15 (Catalina) or newer
- Apple Silicon (M1/M2/M3) or Intel Mac

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Troubleshooting

### App Won't Start
1. Open Terminal
2. Run: `rm -rf ~/Library/Application\ Support/Advent\ of\ Habit`
3. Try launching the app again

### Reset All Data
1. Delete the app from Applications
2. Run: `rm -rf ~/Library/Application\ Support/Advent\ of\ Habit`
3. Reinstall the app

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- Built with PyQt6
- Icons and styling inspired by macOS design guidelines
- Special thanks to the open source community 
