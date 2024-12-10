#!/bin/bash

# Exit on error
set -e

echo "Building macOS app for App Store..."
pyinstaller Advent_of_Habits_AppStore.spec --noconfirm

echo "App bundle created at: dist/Advent of Habits.app"
echo "Next steps:"
echo "1. Open Xcode"
echo "2. File -> Open -> Select the .app file"
echo "3. Product -> Archive"
echo "4. Follow the distribution steps in Xcode" 