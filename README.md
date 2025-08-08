# Macro Recorder - AFK Helper

A professional Python-based macro recorder with an advanced GUI designed to help prevent AFK kicks by automating repetitive actions with precision timing control.

## ✨ Features

### 🎮 **Core Functionality**
- 🖱️ **Full Input Recording**: Captures mouse movements, clicks, scrolling, and keyboard input
- 🔄 **Loop Functionality**: Automatically repeat recorded actions at configurable intervals
- 💾 **Save/Load Macros**: Store your macros as JSON files for reuse
- 🛡️ **Safety Features**: Easy stop controls, ESC key emergency stop, auto-removes last 2 seconds from recordings

### 🎨 **Professional Interface**
- **Modern Dark Theme**: Beautiful interface with sophisticated color palettes
- **Resizable Window**: Adaptive layout that remembers your preferred size
- **Responsive Design**: Multi-threaded for smooth operation during recording/playback

### ⌨️ **Advanced Hotkey System**
- **Combination Keys**: Support for CTRL+1, ALT+F1, SHIFT+SPACE, etc.
- **Global Hotkeys**: Work from anywhere, even when app is minimized
- **Customizable**: Set any key combination for recording, playback, and stopping
- **Settings Persistence**: All hotkeys automatically saved and restored

### 📝 **Professional Macro Editor**
- **Row-Based Editing**: View and edit each recorded action individually
- **Right-Click Context Menu**: Edit, duplicate, insert, delete, move events
- **Event Types**: Mouse clicks, movements, scrolling, key presses, and delays
- **Delay Events**: Add precise timing controls between actions
- **Real-Time Editing**: Modify macros without re-recording

### 💾 **Settings Management**
- **Auto-Save**: All settings automatically preserved between sessions
- **JSON Configuration**: Easy to backup and share settings
- **Window State**: Remembers size, position, and preferences

## 🚀 Installation

### Option 1: Standalone .exe (Recommended)
1. **Download** the latest release or build from source
2. **Build .exe**: Double-click `build.bat` or run `python build_exe.py`
3. **Run**: Find `MacroRecorder.exe` in the `dist` folder
4. **No Python Required** on target computer!

### Option 2: Run from Python (Developers)
1. **Clone** this repository
2. **Install Python** 3.7+ with pip
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run**: `python main.py`

## 📖 Usage Guide

### Quick Start

1. **Launch Application**
   - Double-click `MacroRecorder.exe` or run `python main.py`
   - Window automatically loads your saved settings

2. **Set Up Hotkeys**
   - Configure combination keys like `ctrl+1` for recording
   - Set `ctrl+4` for instant macro playback
   - All hotkeys saved automatically

3. **Record Actions**
   - **Method A**: Click "● Record" button
   - **Method B**: Press your recording hotkey from anywhere
   - Perform actions in your application
   - Press stop hotkey or click "⏹ Stop Recording"

4. **Edit Your Macro** (New!)
   - View recorded events in the professional table editor
   - Right-click any row to edit, duplicate, or add delays
   - Insert custom delay events for precise timing
   - Create complex sequences with perfect control

5. **Play Macro**
   - Press your trigger hotkey for instant playback
   - Or use "▶ Play" button for trigger mode
   - Macro loops automatically based on your settings

### 🛠️ Advanced Features

#### Professional Macro Editor
- **Table View**: All events displayed in organized rows
- **Event Types**: 
  - ⏰ **Delay**: Wait specified seconds between actions
  - 🖱️ **Mouse Click**: Click at specific coordinates
  - ↗️ **Mouse Move**: Move cursor to position  
  - ⌨️ **Key Press/Release**: Keyboard actions
  - 🔄 **Mouse Scroll**: Scroll wheel events

#### Right-Click Context Menu
- **✏️ Edit Event**: Modify position, timing, or action type
- **📋 Duplicate Event**: Copy events for variations
- **➕ Insert Above/Below**: Add events at specific positions
- **🗑️ Delete Event**: Remove unwanted actions
- **⬆️⬇️ Move Up/Down**: Reorder event sequence

#### Event Editor Dialog
- **Radio Button Selection**: Clear event type selection
- **Dynamic Fields**: Properties update based on event type
- **Help Text**: Contextual descriptions for all fields
- **Professional Design**: Modern interface with proper validation

#### Combination Hotkeys
- **Examples**: `ctrl+1`, `alt+f1`, `shift+space`, `ctrl+shift+r`
- **Global Operation**: Work from any application
- **Smart Detection**: Proper modifier key tracking
- **Display Formatting**: Shows "Ctrl + 1" in status

#### Settings Persistence
- **Automatic Saving**: No manual save required
- **settings.json**: Stores in application directory
- **Includes**: Hotkeys, window size, intervals, all preferences
- **Version Safe**: Merges new settings with existing configuration

### 🎯 AFK Prevention Setup

1. **Record Movement Pattern**:
   - Record a simple movement sequence (walk forward, turn, etc.)
   - Keep sequence 10-30 seconds for reliability

2. **Add Timing Delays**:
   - Right-click in editor → "Add Event" → "Delay"
   - Set 60-120 second delays between action sequences
   - Add descriptions like "Wait before next movement"

3. **Configure Loop Settings**:
   - Enable "Loop continuously"
   - Set appropriate repeat interval
   - Test thoroughly before extended use

4. **Set Trigger Hotkey**:
   - Use something like `ctrl+4` for easy access
   - Press from game for instant AFK prevention
   - Use stop hotkey when returning

## 📁 File Structure

```
macro-python/
├── main.py                          # Main application entry point
├── macro_recorder.py                # Core recording/playback engine
├── settings_manager.py              # Settings persistence system
├── build_exe.py                     # Standalone .exe builder
├── build.bat                        # Windows build helper
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
├── gui/                             # GUI components package
│   ├── __init__.py                 # Package initialization
│   ├── gui_styles.py               # Theme and styling system
│   ├── components.py               # UI component modules
│   ├── hotkey_manager.py           # Basic hotkey management
│   ├── advanced_hotkey_manager.py  # Combination key support
│   ├── movement_display.py         # Legacy display manager
│   └── editable_movements.py       # Professional macro editor
├── settings.json                    # Auto-generated user settings
└── dist/                           # Generated .exe location
    └── MacroRecorder.exe           # Standalone executable
```

## 🔧 Technical Details

### Dependencies
- **pynput**: Cross-platform input capture and simulation
- **customtkinter**: Modern GUI framework with dark theme
- **tkinter**: Built-in Python GUI (base framework)
- **threading**: Non-blocking operation support
- **json**: Settings and macro file format

### Supported Input Events
- **Mouse**: Position, left/right/middle clicks, scroll wheel
- **Keyboard**: All standard keys, function keys, modifiers
- **Special**: Arrow keys, space, enter, tab, escape
- **Combinations**: Multi-key combinations with modifiers
- **Timing**: Precise delay control between events

### File Formats
- **Macros**: JSON with event arrays, timestamps, metadata
- **Settings**: JSON with hotkeys, UI preferences, user config
- **Cross-Platform**: Compatible across Windows, macOS, Linux

## 🛠️ Troubleshooting

### Common Issues

**Combination hotkeys not working**:
- Ensure proper format: `ctrl+1`, `alt+f2`, `shift+space`
- Check if other software is using the same combination
- Try different key combinations
- Restart application to refresh hotkey system

**Settings not saving**:
- Check file permissions in application directory
- Ensure `settings.json` is not read-only
- Run as administrator if needed
- Check disk space availability

**Macro editor not responding**:
- Right-click empty space to add events
- Double-click instruction rows to create new events
- Import from recording first, then edit
- Clear all events and start fresh if corrupted

**Permission errors**:
- **Windows**: Run as administrator
- **macOS**: Grant accessibility permissions in System Preferences
- **Linux**: Install required input group permissions

### Performance Optimization
- Use delay events instead of long empty periods
- Keep macro sequences focused and concise
- Test with shorter loops before long sessions
- Close unnecessary applications during recording

## ⚠️ Important Notes

🔒 **Security**: Never record macros containing passwords or sensitive data

🎯 **Application Agnostic**: Works with any application accepting input

⚖️ **Legal Use**: Ensure compliance with application terms of service

🧪 **Testing**: Always test macros thoroughly before extended use

## 🎉 What's New

### Latest Updates
- ✅ **Resizable Interface**: Window size automatically saved
- ✅ **Combination Hotkeys**: Full support for ctrl+key, alt+key, etc.
- ✅ **Settings Persistence**: All preferences automatically saved
- ✅ **Professional Macro Editor**: Row-based editing with context menus
- ✅ **Delay Events**: Add precise timing between actions
- ✅ **Event Editor Dialog**: Modern interface for creating custom events
- ✅ **Debug Output Removed**: Clean, production-ready operation

### Coming Soon
- 🔄 Drag-and-drop event reordering
- 📊 Macro playback statistics
- 🎯 Template macro library
- 📱 Compact view mode

## 📞 Support

Need help? Check these resources:

1. **Read this README** thoroughly
2. **Test with simple macros** first
3. **Check file permissions** and administrator access
4. **Verify hotkey conflicts** with other software
5. **Review settings.json** for configuration issues

---

**Professional Macro Recording Made Simple! 🎮✨**
