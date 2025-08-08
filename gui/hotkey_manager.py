"""
Hotkey Management System for  Macro Recorder
"""
from pynput.keyboard import Listener as KeyboardListener
import threading

class HotkeyManager:
    """Manages global hotkeys for the application"""
    
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
        self.listener = KeyboardListener(on_press=self._on_key_press)
        self.listener.start()
    
    def stop_listening(self):
        """Stop the global hotkey listener"""
        self.active = False
        if self.listener:
            self.listener.stop()
            self.listener = None
    
    def _on_key_press(self, key):
        """Handle key press events with combination support"""
        if not self.active:
            return True
        
        try:
            # Get current modifiers
            current_combination = self._get_current_combination(key)
            
            # Check against all hotkeys
            for hotkey_name, hotkey_combo in self.hotkeys.items():
                if current_combination.lower() == hotkey_combo.lower():
                    self._execute_hotkey_action(hotkey_name)
                    return True
                
        except Exception as e:
            print(f"Hotkey error: {e}")
        
        return True
    
    def _get_current_combination(self, key):
        """Get the current key combination as a string"""
        from pynput import keyboard
        
        modifiers = []
        
        # Check for modifiers - this is a simplified approach
        # In a real implementation, you'd track modifier states
        try:
            # Get the pressed key name
            key_name = self._get_key_name(key)
            
            # For combination keys like "ctrl+3", we need to check if modifiers are held
            # This is a basic implementation - could be enhanced with proper modifier tracking
            
            # Check if this looks like a modifier key
            if key_name.lower() in ['ctrl', 'alt', 'shift', 'cmd']:
                return key_name.lower()
            
            # For now, return just the key name
            # Enhanced combination detection would go here
            return key_name
            
        except:
            return str(key).replace('Key.', '').lower()
    
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
            if hasattr(key, 'char') and key.char:
                return key.char
            elif hasattr(key, 'name'):
                return key.name
            else:
                return str(key).replace('Key.', '')
        except:
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
