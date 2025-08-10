#!/usr/bin/env python3
"""
Build script to create a standalone .exe for the  Macro Recorder
"""

import os
import subprocess
import sys
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        print("✅ PyInstaller installed successfully")

def create_spec_file():
    """Create a custom .spec file for better control over the build"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pynput.mouse._win32',
        'pynput.keyboard._win32',
        'pynput._util.win32',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
        'tkinter.simpledialog',
        'customtkinter',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'gui',
        'gui.gui_styles',
        'gui.components',
        'gui.hotkey_manager',
        'gui.movement_display',
        'gui.editable_movements',
        'scheduler',
        'tkinter',
        'tkinter.ttk'
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MacroRecorder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
'''
    
    with open('macro_recorder.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Created custom .spec file")

def build_exe():
    """Build the .exe file using PyInstaller"""
    print("🔨 Building .exe file...")
    
    # Create the spec file first
    create_spec_file()
    
    # Build using the spec file
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'macro_recorder.spec'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        print(f"📁 .exe file location: {os.path.join('dist', 'MacroRecorder.exe')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_icon():
    """Create a simple icon file (optional)"""
    # This is optional - you can add an icon later
    print("💡 Tip: You can add an icon by:")
    print("   1. Create or find a .ico file")
    print("   2. Update the icon=None line in the .spec file")
    print("   3. Run this script again")

def cleanup():
    """Clean up build files"""
    print("🧹 Cleaning up build files...")
    import shutil
    
    # Remove build directory
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("   ✅ Removed build directory")
    
    # Keep dist directory but mention it
    if os.path.exists('dist'):
        print("   📁 Kept dist directory with your .exe file")

def main():
    """Main build process"""
    print("🎮  Macro Recorder - .exe Builder")
    print("=" * 50)
    
    # Check if required files exist
    required_files = ['main.py', 'macro_recorder.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file not found: {file}")
            return False
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build the .exe
    if build_exe():
        cleanup()
        print("\n🎉 SUCCESS!")
        print("=" * 50)
        print("Your .exe file is ready:")
        print(f"📁 Location: {os.path.abspath(os.path.join('dist', 'MacroRecorder.exe'))}")
        print("\n📋 Next steps:")
        print("   1. Test the .exe file")
        print("   2. Share the entire 'dist' folder if needed")
        print("   3. The .exe is completely standalone!")
        return True
    else:
        print("\n❌ Build failed. Check the error messages above.")
        return False

if __name__ == "__main__":
    main()
