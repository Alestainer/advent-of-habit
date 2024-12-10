#!/bin/bash

# Exit on error
set -e

echo "Installing requirements..."
pip install -r requirements.txt

echo "Converting SVG icon to ICNS..."
mkdir -p icon.iconset
cairosvg app_icon.svg -o icon.iconset/icon_512x512@2x.png -s 2
sips -z 16 16     icon.iconset/icon_512x512@2x.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.iconset/icon_512x512@2x.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.iconset/icon_512x512@2x.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.iconset/icon_512x512@2x.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.iconset/icon_512x512@2x.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.iconset/icon_512x512@2x.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.iconset/icon_512x512@2x.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.iconset/icon_512x512@2x.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.iconset/icon_512x512@2x.png --out icon.iconset/icon_512x512.png
iconutil -c icns icon.iconset
rm -rf icon.iconset

echo "Building macOS app..."
pyinstaller Advent_of_Habit.spec

echo "App bundle created at: dist/Advent of Habits.app" 