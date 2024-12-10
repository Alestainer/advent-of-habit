# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../launch_habit_tracker.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt6.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Advent of Habits',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity='Apple Development',  # Change this to your identity
    entitlements_file='entitlements.plist',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Advent of Habits',
)

app = BUNDLE(
    coll,
    name='Advent of Habits.app',
    bundle_identifier='com.adventofhabits.tracker',  # Change this to your bundle ID
    info_plist={
        'LSMinimumSystemVersion': '10.15',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': True,
        'NSSupportsAutomaticGraphicsSwitching': True,
        'CFBundleName': 'Advent of Habits',
        'CFBundleDisplayName': 'Advent of Habits',
        'CFBundlePackageType': 'APPL',
        'NSHumanReadableCopyright': '© 2024 Your Name',
        'LSApplicationCategoryType': 'public.app-category.lifestyle',
        'NSCalendarsUsageDescription': 'This app does not use your calendar.',
        'NSCameraUsageDescription': 'This app does not use your camera.',
        'NSMicrophoneUsageDescription': 'This app does not use your microphone.',
        'NSPhotoLibraryUsageDescription': 'This app does not use your photos.',
    }
) 