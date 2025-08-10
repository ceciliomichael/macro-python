import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
from datetime import datetime
from macro_recorder import MacroRecorder
from gui import (
    ThemeManager, 
    TitleSection, 
    ControlButtonsSection, 
    SettingsPanel, 
    MovementsPanel,
    HotkeyManager,
    MovementDisplayManager,
    EditableMovementsDisplay
)
from gui.advanced_hotkey_manager import AdvancedHotkeyManager
from settings_manager import SettingsManager
from scheduler import MacroScheduler

class MacroRecorderGUI:
    def __init__(self, root):
        self.root = root
        
        # Configure theme
        ThemeManager.setup_theme()
        
        # Window configuration
        self.root.title(" Macro Recorder - AFK Helper")
        self.root.geometry("1000x700")
        self.root.minsize(1250, 900)  # Minimum size
        self.root.resizable(True, True)
        
        # Initialize core components
        self.recorder = MacroRecorder()
        self.is_recording = False
        self.is_playing = False
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Initialize managers
        self.hotkey_manager = AdvancedHotkeyManager(self)
        self.movement_display = None  # Will be initialized after GUI creation
        self.scheduler = MacroScheduler(self)
        
        # GUI components
        self.title_section = None
        self.control_section = None
        self.settings_panel = None
        self.movements_panel = None
        
        # Create GUI elements
        self.create_widgets()
        
        # Initialize movement display manager (legacy compatibility)
        self.movement_display = self.movements_panel  # Use the editable display directly
        
        # Load and apply saved settings
        self.load_settings()
        
        # Setup hotkeys after GUI is created
        self.setup_hotkeys()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create and arrange all GUI widgets using modular components"""
        
        # Main container
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create title section
        self.title_section = TitleSection(main_frame)
        self.title_section.create()
        self.status_label = self.title_section.status_label
        
        # Create control buttons section
        self.control_section = ControlButtonsSection(main_frame, self)
        self.control_section.create()
        self.record_btn = self.control_section.record_btn
        self.play_btn = self.control_section.play_btn
        self.stop_btn = self.control_section.stop_btn
        
        # Content container for panels
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create settings panel
        self.settings_panel = SettingsPanel(content_frame, self)
        self.settings_panel.create()
        
        # Create editable movements panel
        self.movements_panel = EditableMovementsDisplay(content_frame, self.recorder)
        self.movements_panel.create()
        
        # Set up convenient references for backwards compatibility
        self._setup_widget_references()
    
    def _setup_widget_references(self):
        """Set up convenient references to widgets for backwards compatibility"""
        # Settings panel references
        self.trigger_var = self.settings_panel.trigger_var
        self.start_hotkey_var = self.settings_panel.start_hotkey_var
        self.stop_hotkey_var = self.settings_panel.stop_hotkey_var
        self.stop_play_hotkey_var = self.settings_panel.stop_play_hotkey_var
        self.interval_var = self.settings_panel.interval_var
        self.loop_var = self.settings_panel.loop_var
        
        # Movements panel references (legacy compatibility)
        # Note: movements_text doesn't exist in EditableMovementsDisplay
        # self.movements_text = None  # Not needed with new editable display
    
    def toggle_recording(self):
        """Toggle macro recording on/off"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording user actions"""
        self.is_recording = True
        self.record_btn.configure(text="⏹ Stop Recording", fg_color=ThemeManager.COLORS['primary_hover'])
        self.status_label.configure(text="Recording... Perform actions in ", text_color=ThemeManager.COLORS['primary'])
        
        # Start recording in separate thread
        record_thread = threading.Thread(target=self.recorder.start_recording)
        record_thread.daemon = True
        record_thread.start()
    
    def stop_recording(self):
        """Stop recording user actions"""
        self.is_recording = False
        self.recorder.stop_recording()
        self.record_btn.configure(text="● Record", fg_color=ThemeManager.COLORS['primary'])
        self.status_label.configure(text=f"Recording stopped. {len(self.recorder.events)} events captured", text_color=ThemeManager.COLORS['secondary'])
        
        # Refresh the editable movements display
        self.movement_display.refresh_display()
    
    def play_macro(self):
        """Start playing recorded macro with trigger key (old method)"""
        if not self.recorder.events:
            messagebox.showwarning("No Macro", "Please record a macro first!")
            return
        
        if self.is_playing:
            return
        
        try:
            interval = float(self.interval_var.get())
        except ValueError:
            messagebox.showerror("Invalid Interval", "Please enter a valid number for interval")
            return
        
        trigger_key = self.trigger_var.get().strip()
        if not trigger_key:
            messagebox.showerror("No Trigger", "Please enter a trigger key!")
            return
        
        self.is_playing = True
        self.play_btn.configure(text="⏸ Playing...", fg_color="#45B7AB")
        self.status_label.configure(text=f"Waiting for trigger key '{trigger_key}' in ...", text_color="#FFD93D")
        
        # Start playback with trigger in separate thread
        play_thread = threading.Thread(
            target=self.recorder.play_macro_with_trigger,
            args=(trigger_key, interval, self.loop_var.get(), self.update_status)
        )
        play_thread.daemon = True
        play_thread.start()
    
    def start_auto_playback(self):
        """Start playing macro automatically when trigger key is pressed"""
        if not self.recorder.events:
            self.status_label.configure(
                text="No macro recorded! Press F9 to record first.", 
                text_color=ThemeManager.COLORS['danger']
            )
            return
        
        if self.is_playing:
            return
        
        try:
            interval = float(self.interval_var.get())
        except ValueError:
            self.status_label.configure(
                text="Invalid interval setting!", 
                text_color=ThemeManager.COLORS['danger']
            )
            return
        
        self.is_playing = True
        self.play_btn.configure(text="⏸ Playing...", fg_color=ThemeManager.COLORS['secondary_hover'])
        self.status_label.configure(
            text="Trigger detected! Starting macro immediately...", 
            text_color=ThemeManager.COLORS['warning']
        )
        
        # Start direct playback in separate thread
        play_thread = threading.Thread(
            target=self.recorder.play_macro,
            args=(interval, self.loop_var.get(), self.update_status)
        )
        play_thread.daemon = True
        play_thread.start()
    
    def stop_all(self):
        """Stop all recording and playback"""
        self.is_recording = False
        self.is_playing = False
        self.recorder.stop_all()
        
        # Note: No need to stop updates with editable display
        
        self.record_btn.configure(text="● Record", fg_color=ThemeManager.COLORS['primary'])
        self.play_btn.configure(text="▶ Play", fg_color=ThemeManager.COLORS['secondary'])
        self.status_label.configure(
            text="All operations stopped - Ready for new commands", 
            text_color=ThemeManager.COLORS['secondary']
        )
    
    def save_macro(self):
        """Save current macro to file"""
        if not self.recorder.events:
            messagebox.showwarning("No Macro", "Please record a macro first!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self.recorder.save_macro(filename)
            messagebox.showinfo("Saved", f"Macro saved to {filename}")
    
    def load_macro(self):
        """Load macro from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.recorder.load_macro(filename):
                self.status_label.configure(
                    text=f"Loaded macro with {len(self.recorder.events)} events", 
                    text_color=ThemeManager.COLORS['secondary']
                )
                self.movement_display.refresh_display()
                messagebox.showinfo("Loaded", f"Macro loaded from {filename}")
            else:
                messagebox.showerror("Error", "Failed to load macro file")
    
    def update_status(self, message):
        """Update status label thread-safely"""
        self.root.after(0, lambda: self.status_label.configure(
            text=message, 
            text_color=ThemeManager.COLORS['warning']
        ))
    
    def load_settings(self):
        """Load saved settings from file"""
        try:
            settings = self.settings_manager.load_settings()
            
            # Apply hotkey settings
            hotkeys = settings.get("hotkeys", {})
            if hotkeys:
                self.start_hotkey_var.set(hotkeys.get("start_recording", "f9"))
                self.stop_hotkey_var.set(hotkeys.get("stop_recording", "f10"))
                self.trigger_var.set(hotkeys.get("trigger_play", "f1"))
                self.stop_play_hotkey_var.set(hotkeys.get("stop_playing", "f11"))
            
            # Apply UI settings
            ui_settings = settings.get("ui", {})
            if ui_settings:
                self.interval_var.set(ui_settings.get("repeat_interval", "60"))
                self.loop_var.set(ui_settings.get("loop_continuously", True))
                
                # Apply window geometry if saved
                geometry = ui_settings.get("window_geometry")
                if geometry and geometry != "1000x700":
                    self.root.geometry(geometry)
            
            # Apply scheduler settings
            scheduler_settings = settings.get("scheduler", {})
            enabled = scheduler_settings.get("enabled", False)
            schedules = scheduler_settings.get("schedules", [])
            self.scheduler.set_schedules(schedules)
            self.scheduler.set_enabled(enabled)
            if hasattr(self.settings_panel, 'set_scheduler_state'):
                self.settings_panel.set_scheduler_state(enabled, schedules)
            
            print("✅ Settings loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading settings: {e}")
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            # Update hotkey settings
            self.settings_manager.set_hotkeys(
                self.start_hotkey_var.get(),
                self.stop_hotkey_var.get(), 
                self.trigger_var.get(),
                self.stop_play_hotkey_var.get()
            )
            
            # Update UI settings
            geometry = self.root.geometry()
            self.settings_manager.set_ui_settings(
                geometry=geometry,
                trigger_key=self.trigger_var.get(),
                interval=self.interval_var.get(),
                loop=self.loop_var.get()
            )
            
            # Update scheduler settings
            if hasattr(self.settings_panel, 'get_scheduler_state'):
                sched_enabled, schedules = self.settings_panel.get_scheduler_state()
                self.settings_manager.set_scheduler_settings(sched_enabled, schedules)
                # Also update live scheduler
                self.scheduler.set_schedules(schedules)
                self.scheduler.set_enabled(sched_enabled)
            
            # Save to file
            success = self.settings_manager.save_settings()
            if success:
                self.status_label.configure(
                    text="✅ Settings saved successfully",
                    text_color=ThemeManager.COLORS['success']
                )
            else:
                self.status_label.configure(
                    text="❌ Failed to save settings",
                    text_color=ThemeManager.COLORS['danger']
                )
            
        except Exception as e:
            print(f"❌ Error saving settings: {e}")
            self.status_label.configure(
                text="❌ Error saving settings",
                text_color=ThemeManager.COLORS['danger']
            )
    

    
    def setup_hotkeys(self):
        """Set up global hotkeys for recording"""
        self.apply_hotkeys()
    
    def apply_hotkeys(self):
        """Apply the current hotkey settings"""
        start_key = self.start_hotkey_var.get().strip()
        stop_key = self.stop_hotkey_var.get().strip()
        trigger_key = self.trigger_var.get().strip()
        stop_play_key = self.stop_play_hotkey_var.get().strip()
        
        if not start_key or not stop_key or not trigger_key or not stop_play_key:
            self.status_label.configure(
                text="Please enter valid hotkeys", 
                text_color=ThemeManager.COLORS['danger']
            )
            return
        
        # Update hotkey manager with new settings
        self.hotkey_manager.set_hotkeys(start_key, stop_key, trigger_key, stop_play_key)
        self.hotkey_manager.start_listening()
        
        # Auto-save settings when hotkeys are applied
        self.save_settings()
        
        # Update status
        self.status_label.configure(
            text=f"Hotkeys applied: {AdvancedHotkeyManager.format_hotkey_display(start_key)}(rec) {AdvancedHotkeyManager.format_hotkey_display(trigger_key)}(play)",
            text_color=ThemeManager.COLORS['success']
        )
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_all()
        
        # Save settings on exit
        self.save_settings()
        
        # Cleanup managers
        if self.hotkey_manager:
            self.hotkey_manager.cleanup()
        if self.scheduler:
            self.scheduler.stop()
        
        self.root.destroy()

def main():
    root = ctk.CTk()
    app = MacroRecorderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
