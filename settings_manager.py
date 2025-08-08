"""
Settings Manager for  Macro Recorder
Handles saving and loading of application settings including hotkeys
"""
import json
import os
from datetime import datetime

class SettingsManager:
    """Manages application settings persistence"""
    
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "hotkeys": {
                "start_recording": "f9",
                "stop_recording": "f10",
                "trigger_play": "f1", 
                "stop_playing": "f11"
            },
            "ui": {
                "window_geometry": "1000x700",
                "trigger_key": "F1",
                "repeat_interval": "60",
                "loop_continuously": True
            },
            "last_saved": None
        }
        self.current_settings = self.default_settings.copy()
        
    def load_settings(self):
        """Load settings from file, return default if file doesn't exist"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                
                # Merge with defaults to handle new settings
                self.current_settings = self._merge_settings(self.default_settings, loaded_settings)
                print(f"✅ Settings loaded from {self.settings_file}")
                return self.current_settings
            else:
                print(f"📄 No settings file found, using defaults")
                return self.default_settings.copy()
                
        except Exception as e:
            print(f"❌ Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self, settings=None):
        """Save current settings to file"""
        try:
            if settings:
                self.current_settings = settings
            
            # Add timestamp
            self.current_settings["last_saved"] = datetime.now().isoformat()
            
            with open(self.settings_file, 'w') as f:
                json.dump(self.current_settings, f, indent=2)
            
            print(f"💾 Settings saved to {self.settings_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving settings: {e}")
            return False
    
    def _merge_settings(self, defaults, loaded):
        """Merge loaded settings with defaults to handle new keys"""
        merged = defaults.copy()
        
        for key, value in loaded.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key].update(value)
            else:
                merged[key] = value
                
        return merged
    
    def get_hotkeys(self):
        """Get hotkey settings"""
        return self.current_settings.get("hotkeys", self.default_settings["hotkeys"])
    
    def set_hotkeys(self, start_rec, stop_rec, trigger, stop_play):
        """Update hotkey settings"""
        self.current_settings["hotkeys"] = {
            "start_recording": start_rec,
            "stop_recording": stop_rec,
            "trigger_play": trigger,
            "stop_playing": stop_play
        }
    
    def get_ui_settings(self):
        """Get UI settings"""
        return self.current_settings.get("ui", self.default_settings["ui"])
    
    def set_ui_settings(self, geometry=None, trigger_key=None, interval=None, loop=None):
        """Update UI settings"""
        ui_settings = self.current_settings.get("ui", {})
        
        if geometry:
            ui_settings["window_geometry"] = geometry
        if trigger_key:
            ui_settings["trigger_key"] = trigger_key
        if interval:
            ui_settings["repeat_interval"] = interval
        if loop is not None:
            ui_settings["loop_continuously"] = loop
            
        self.current_settings["ui"] = ui_settings
    
    def get_setting(self, category, key, default=None):
        """Get a specific setting value"""
        return self.current_settings.get(category, {}).get(key, default)
    
    def set_setting(self, category, key, value):
        """Set a specific setting value"""
        if category not in self.current_settings:
            self.current_settings[category] = {}
        self.current_settings[category][key] = value
    
    def auto_save_enabled(self):
        """Check if auto-save is enabled"""
        return self.get_setting("general", "auto_save", True)
    
    def export_settings(self, export_file):
        """Export settings to a different file"""
        try:
            with open(export_file, 'w') as f:
                json.dump(self.current_settings, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error exporting settings: {e}")
            return False
    
    def import_settings(self, import_file):
        """Import settings from a file"""
        try:
            with open(import_file, 'r') as f:
                imported_settings = json.load(f)
            
            self.current_settings = self._merge_settings(self.default_settings, imported_settings)
            return True
        except Exception as e:
            print(f"❌ Error importing settings: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.current_settings = self.default_settings.copy()
        print("🔄 Settings reset to defaults")
    
    def get_settings_info(self):
        """Get information about current settings"""
        return {
            "file_exists": os.path.exists(self.settings_file),
            "file_path": os.path.abspath(self.settings_file),
            "last_saved": self.current_settings.get("last_saved"),
            "hotkeys_count": len(self.current_settings.get("hotkeys", {})),
            "settings_count": sum(len(v) if isinstance(v, dict) else 1 for v in self.current_settings.values())
        }
