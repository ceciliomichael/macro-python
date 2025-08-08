"""
Advanced Hotkey Management System for  Macro Recorder
Supports combination keys like CTRL+3, ALT+F1, etc.
"""
from pynput.keyboard import Listener as KeyboardListener, Key
import threading
import time

class AdvancedHotkeyManager:
    """Advanced hotkey manager with combination key support"""
    
    def __init__(self, gui_controller):
        self.gui_controller = gui_controller
        self.listener = None
        self.hotkeys = {
            'start_recording': 'f9',
            'stop_recording': 'f10', 
            'trigger_play': 'f1',
            'stop_playing': 'f11'
        }
        self.active = False
        
        # Track modifier states
        self.modifiers_pressed = {
            'ctrl': False,
            'alt': False,
            'shift': False,
            'cmd': False
        }
        
        # Track recent key combinations
        self.recent_combinations = []
        self.combination_timeout = 0.5  # seconds
    
    def set_hotkeys(self, start_rec, stop_rec, trigger, stop_play):
        """Update hotkey configuration"""
        self.hotkeys = {
            'start_recording': start_rec.lower(),
            'stop_recording': stop_rec.lower(),
            'trigger_play': trigger.lower(),
            'stop_playing': stop_play.lower()
        }
    
    def start_listening(self):
        """Start the global hotkey listener"""
        if self.listener:
            self.stop_listening()
        
        self.active = True
        self.listener = KeyboardListener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.listener.start()
    
    def stop_listening(self):
        """Stop the global hotkey listener"""
        self.active = False
        if self.listener:
            self.listener.stop()
            self.listener = None
    
    def _on_key_press(self, key):
        """Handle key press events"""
        if not self.active:
            return True
        
        try:
            # Update modifier states
            self._update_modifier_state(key, True)
            
            # Get current combination
            combination = self._get_active_combination(key)
            
            if combination:
                # Check against configured hotkeys
                for hotkey_name, hotkey_combo in self.hotkeys.items():
                    if self._combinations_match(combination, hotkey_combo):
                        self._execute_hotkey_action(hotkey_name)
                        return True
                
        except Exception as e:
            print(f"Hotkey error: {e}")
        
        return True
    
    def _on_key_release(self, key):
        """Handle key release events"""
        if not self.active:
            return True
        
        try:
            # Update modifier states
            self._update_modifier_state(key, False)
        except Exception as e:
            print(f"Hotkey release error: {e}")
        
        return True
    
    def _update_modifier_state(self, key, pressed):
        """Update the state of modifier keys"""
        key_name = self._get_key_name(key).lower()
        
        if key_name in ['ctrl', 'ctrl_l', 'ctrl_r'] or key == Key.ctrl or key == Key.ctrl_l or key == Key.ctrl_r:
            self.modifiers_pressed['ctrl'] = pressed
        elif key_name in ['alt', 'alt_l', 'alt_r'] or key == Key.alt or key == Key.alt_l or key == Key.alt_r:
            self.modifiers_pressed['alt'] = pressed
        elif key_name in ['shift', 'shift_l', 'shift_r'] or key == Key.shift or key == Key.shift_l or key == Key.shift_r:
            self.modifiers_pressed['shift'] = pressed
        elif key_name in ['cmd', 'cmd_l', 'cmd_r'] or key == Key.cmd or key == Key.cmd_l or key == Key.cmd_r:
            self.modifiers_pressed['cmd'] = pressed
    
    def _get_active_combination(self, key):
        """Get the currently active key combination"""
        key_name = self._get_key_name(key).lower()
        
        # Skip if this is just a modifier key press
        if key_name in ['ctrl', 'ctrl_l', 'ctrl_r', 'alt', 'alt_l', 'alt_r', 'shift', 'shift_l', 'shift_r', 'cmd', 'cmd_l', 'cmd_r']:
            return None
        
        # Build combination string
        combination_parts = []
        
        if self.modifiers_pressed['ctrl']:
            combination_parts.append('ctrl')
        if self.modifiers_pressed['alt']:
            combination_parts.append('alt')
        if self.modifiers_pressed['shift']:
            combination_parts.append('shift')
        if self.modifiers_pressed['cmd']:
            combination_parts.append('cmd')
        
        # Add the main key
        combination_parts.append(key_name)
        
        combination = '+'.join(combination_parts)
        return combination
    
    def _combinations_match(self, actual, configured):
        """Check if two key combinations match"""
        # Normalize both combinations
        actual_parts = [part.strip().lower() for part in actual.split('+')]
        configured_parts = [part.strip().lower() for part in configured.split('+')]
        
        # Sort modifiers for comparison
        actual_modifiers = sorted([part for part in actual_parts if part in ['ctrl', 'alt', 'shift', 'cmd']])
        configured_modifiers = sorted([part for part in configured_parts if part in ['ctrl', 'alt', 'shift', 'cmd']])
        
        # Get main keys
        actual_main = [part for part in actual_parts if part not in ['ctrl', 'alt', 'shift', 'cmd']]
        configured_main = [part for part in configured_parts if part not in ['ctrl', 'alt', 'shift', 'cmd']]
        
        # Compare
        match = (actual_modifiers == configured_modifiers and 
                actual_main == configured_main)
        
        return match
    
    def _execute_hotkey_action(self, hotkey_name):
        """Execute the appropriate action for a hotkey"""
        if hotkey_name == 'start_recording':
            if not self.gui_controller.is_recording and not self.gui_controller.is_playing:
                self.gui_controller.root.after(0, self.gui_controller.start_recording)
        
        elif hotkey_name == 'stop_recording':
            if self.gui_controller.is_recording:
                self.gui_controller.root.after(0, self.gui_controller.stop_recording)
        
        elif hotkey_name == 'trigger_play':
            if (not self.gui_controller.is_playing and 
                not self.gui_controller.is_recording and 
                self.gui_controller.recorder.events):
                self.gui_controller.root.after(0, self.gui_controller.start_auto_playback)
        
        elif hotkey_name == 'stop_playing':
            if self.gui_controller.is_playing:
                self.gui_controller.root.after(0, self.gui_controller.stop_all)
    
    def _get_key_name(self, key):
        """Extract string name from a key object"""
        try:
            # First try to get the character representation
            if hasattr(key, 'char') and key.char:
                return key.char
            
            # Then try to get the name attribute
            elif hasattr(key, 'name'):
                return key.name
            
            # Handle special cases for number keys and other characters
            else:
                key_str = str(key)
                
                # Handle format like <49> (ASCII codes)
                if key_str.startswith('<') and key_str.endswith('>'):
                    try:
                        ascii_code = int(key_str[1:-1])
                        # Convert ASCII code to character
                        if 32 <= ascii_code <= 126:  # Printable ASCII range
                            return chr(ascii_code)
                    except ValueError:
                        pass
                
                # Clean up Key. prefix
                return key_str.replace('Key.', '')
                
        except Exception as e:
            return str(key).replace('Key.', '')
    
    def get_status_text(self):
        """Get formatted status text for display"""
        return (f"Hotkeys: {self.hotkeys['start_recording']}(rec) "
                f"{self.hotkeys['stop_recording']}(stop) "
                f"{self.hotkeys['trigger_play']}(play) "
                f"{self.hotkeys['stop_playing']}(stop play)")
    
    def validate_hotkeys(self):
        """Validate that all hotkeys are set"""
        return all(key.strip() for key in self.hotkeys.values())
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_listening()
    
    @staticmethod
    def parse_hotkey_string(hotkey_string):
        """Parse a hotkey string like 'ctrl+3' into components"""
        if not hotkey_string:
            return [], None
        
        parts = [part.strip().lower() for part in hotkey_string.split('+')]
        modifiers = [part for part in parts if part in ['ctrl', 'alt', 'shift', 'cmd']]
        main_keys = [part for part in parts if part not in ['ctrl', 'alt', 'shift', 'cmd']]
        
        return modifiers, main_keys[0] if main_keys else None
    
    @staticmethod
    def format_hotkey_display(hotkey_string):
        """Format a hotkey string for display"""
        if not hotkey_string:
            return ""
        
        parts = [part.strip() for part in hotkey_string.split('+')]
        
        # Capitalize and format
        formatted_parts = []
        for part in parts:
            if part.lower() == 'ctrl':
                formatted_parts.append('Ctrl')
            elif part.lower() == 'alt':
                formatted_parts.append('Alt')
            elif part.lower() == 'shift':
                formatted_parts.append('Shift')
            elif part.lower() == 'cmd':
                formatted_parts.append('Cmd')
            else:
                formatted_parts.append(part.upper())
        
        return ' + '.join(formatted_parts)
