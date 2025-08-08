"""
Modular GUI Components for  Macro Recorder
"""
import customtkinter as ctk
from .gui_styles import ThemeManager, StyleHelper

class TitleSection:
    """Title and status section component"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.status_label = None
        
    def create(self):
        """Create the title section"""
        self.frame = StyleHelper.create_frame(
            self.parent, 
            fg_color="transparent"
        )
        self.frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title
        title_label = StyleHelper.create_label(
            self.frame,
            text="🎮  Macro Recorder",
            style='title',
            color=ThemeManager.COLORS['primary']
        )
        title_label.pack(pady=10)
        
        # Status display
        self.status_label = StyleHelper.create_label(
            self.frame,
            text="Ready to record",
            style='heading',
            color=ThemeManager.COLORS['secondary']
        )
        self.status_label.pack(pady=(0, 10))
        
        return self.frame

class ControlButtonsSection:
    """Control buttons section component"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = None
        self.record_btn = None
        self.play_btn = None
        self.stop_btn = None
        
    def create(self):
        """Create the control buttons section"""
        self.frame = StyleHelper.create_frame(self.parent)
        self.frame.pack(fill="x", padx=20, pady=10)
        
        # Section title
        control_title = StyleHelper.create_label(
            self.frame,
            text="Controls",
            style='heading',
            color=ThemeManager.COLORS['accent']
        )
        control_title.pack(pady=(15, 10))
        
        # Buttons frame
        buttons_frame = StyleHelper.create_frame(
            self.frame, 
            fg_color="transparent"
        )
        buttons_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Record button
        self.record_btn = StyleHelper.create_button(
            buttons_frame,
            text="● Record",
            style_type='record',
            command=self.controller.toggle_recording
        )
        self.record_btn.pack(side="left", padx=(0, 10))
        
        # Play button
        self.play_btn = StyleHelper.create_button(
            buttons_frame,
            text="▶ Play", 
            style_type='play',
            command=self.controller.play_macro
        )
        self.play_btn.pack(side="left", padx=(0, 10))
        
        # Stop button
        self.stop_btn = StyleHelper.create_button(
            buttons_frame,
            text="⏹ Stop",
            style_type='stop',
            command=self.controller.stop_all
        )
        self.stop_btn.pack(side="left")
        
        return self.frame

class SettingsPanel:
    """Settings panel component"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = None
        self.trigger_var = None
        self.start_hotkey_var = None
        self.stop_hotkey_var = None
        self.stop_play_hotkey_var = None
        self.interval_var = None
        self.loop_var = None
        
    def create(self):
        """Create the settings panel"""
        self.frame = StyleHelper.create_frame(
            self.parent, 
            width=480
        )
        self.frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.frame.pack_propagate(False)
        
        # Title
        settings_title = StyleHelper.create_label(
            self.frame,
            text="Settings",
            style='heading',
            color=ThemeManager.COLORS['warning']
        )
        settings_title.pack(pady=(15, 10))
        
        # Trigger input
        self._create_trigger_section()
        
        # Hotkeys section
        self._create_hotkeys_section()
        
        # Repeat interval
        self._create_interval_section()
        
        # Loop checkbox
        self._create_loop_section()
        
        # File operations
        self._create_file_section()
        
        return self.frame
    
    def _create_trigger_section(self):
        """Create trigger key input section"""
        trigger_frame = StyleHelper.create_frame(
            self.frame, 
            fg_color="transparent"
        )
        trigger_frame.pack(fill="x", padx=20, pady=10)
        
        trigger_label = StyleHelper.create_label(
            trigger_frame,
            text="Start Trigger (key to start playback):",
            anchor="w"
        )
        trigger_label.pack(fill="x", pady=(0, 5))
        
        self.trigger_var = ctk.StringVar(value="F1")
        self.trigger_entry = StyleHelper.create_entry(
            trigger_frame,
            placeholder="e.g., F1, space, ctrl",
            width=250
        )
        self.trigger_entry.configure(textvariable=self.trigger_var)
        self.trigger_entry.pack(fill="x")
    
    def _create_hotkeys_section(self):
        """Create recording hotkeys section"""
        hotkey_frame = StyleHelper.create_frame(
            self.frame, 
            fg_color="transparent"
        )
        hotkey_frame.pack(fill="x", padx=20, pady=10)
        
        hotkey_label = StyleHelper.create_label(
            hotkey_frame,
            text="Recording Hotkeys:",
            style='subheading',
            anchor="w"
        )
        hotkey_label.pack(fill="x", pady=(0, 5))
        
        # Hotkey format hint
        hint_label = StyleHelper.create_label(
            hotkey_frame,
            text="e.g., ctrl+s, alt+f4",
            style='small',
            anchor='w'
        )
        hint_label.pack(fill="x", pady=(0, 10))
        
        # Start recording hotkey
        self._create_hotkey_input(
            hotkey_frame, 
            "Start Recording:", 
            "F9",
            lambda: self.start_hotkey_var
        )
        
        # Stop recording hotkey  
        self._create_hotkey_input(
            hotkey_frame,
            "Stop Recording:",
            "F10", 
            lambda: self.stop_hotkey_var
        )
        
        # Stop playing hotkey
        self._create_hotkey_input(
            hotkey_frame,
            "Stop Playing:",
            "F11",
            lambda: self.stop_play_hotkey_var
        )
        
        # Apply hotkeys button
        apply_btn = StyleHelper.create_button(
            hotkey_frame,
            text="🔧 Apply Hotkeys",
            style_type='apply',
            command=self.controller.apply_hotkeys
        )
        apply_btn.pack(pady=(5, 0))
    
    def _create_hotkey_input(self, parent, label_text, default_value, var_getter):
        """Create a single hotkey input row"""
        hotkey_input_frame = StyleHelper.create_frame(
            parent, 
            fg_color="transparent"
        )
        hotkey_input_frame.pack(fill="x", pady=(0, 5))
        
        label = StyleHelper.create_label(
            hotkey_input_frame,
            text=label_text,
            style='small',
            anchor="w",
            width=120
        )
        label.pack(side="left", padx=(0, 10))
        
        if label_text == "Start Recording:":
            self.start_hotkey_var = ctk.StringVar(value=default_value)
            var = self.start_hotkey_var
        elif label_text == "Stop Recording:":
            self.stop_hotkey_var = ctk.StringVar(value=default_value)
            var = self.stop_hotkey_var
        else:  # Stop Playing
            self.stop_play_hotkey_var = ctk.StringVar(value=default_value)
            var = self.stop_play_hotkey_var
        
        entry = StyleHelper.create_entry(
            hotkey_input_frame,
            placeholder=default_value,
            width=100,
            height=30
        )
        entry.configure(textvariable=var, font=ThemeManager.get_font('small'))
        entry.pack(side="left")
    
    def _create_interval_section(self):
        """Create repeat interval section"""
        interval_frame = StyleHelper.create_frame(
            self.frame, 
            fg_color="transparent"
        )
        interval_frame.pack(fill="x", padx=20, pady=10)
        
        interval_label = StyleHelper.create_label(
            interval_frame,
            text="Repeat Interval (seconds):",
            anchor="w"
        )
        interval_label.pack(fill="x", pady=(0, 5))
        
        self.interval_var = ctk.StringVar(value="60")
        self.interval_entry = StyleHelper.create_entry(
            interval_frame,
            placeholder="60",
            width=250
        )
        self.interval_entry.configure(textvariable=self.interval_var)
        self.interval_entry.pack(fill="x")
    
    def _create_loop_section(self):
        """Create loop checkbox section"""
        self.loop_var = ctk.BooleanVar(value=True)
        self.loop_checkbox = StyleHelper.create_checkbox(
            self.frame,
            text="Loop continuously (for AFK prevention)",
            variable=self.loop_var
        )
        self.loop_checkbox.pack(padx=20, pady=10, anchor="w")
    
    def _create_file_section(self):
        """Create file operations section"""
        file_frame = StyleHelper.create_frame(
            self.frame, 
            fg_color="transparent"
        )
        file_frame.pack(fill="x", padx=20, pady=15)
        
        save_btn = StyleHelper.create_button(
            file_frame,
            text="💾 Save Macro",
            style_type='file',
            command=self.controller.save_macro
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        load_btn = StyleHelper.create_button(
            file_frame,
            text="📂 Load Macro", 
            style_type='file',
            command=self.controller.load_macro
        )
        load_btn.pack(side="left")

class MovementsPanel:
    """Movements display panel component"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.movements_text = None
        
    def create(self):
        """Create the movements panel"""
        self.frame = StyleHelper.create_frame(
            self.parent,
            width=480
        )
        self.frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        self.frame.pack_propagate(False)
        
        # Title
        movements_title = StyleHelper.create_label(
            self.frame,
            text="Recorded Movements",
            style='heading',
            color=ThemeManager.COLORS['warning']
        )
        movements_title.pack(pady=(15, 10))
        
        # Text area
        movements_frame = StyleHelper.create_frame(
            self.frame, 
            fg_color="transparent"
        )
        movements_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.movements_text = StyleHelper.create_textbox(
            movements_frame,
            height=300
        )
        self.movements_text.pack(fill="both", expand=True)
        
        # Add initial instructions
        self._add_initial_instructions()
        
        return self.frame
    
    def _add_initial_instructions(self):
        """Add initial instruction text"""
        initial_text = """Ready to record movements!

Instructions:
1. Set all hotkeys (F9/F10/F1/F11) and click 'Apply'
2. Press F9 anywhere to start recording
3. Perform your actions in 
4. Press F10 to stop recording
5. Press F1 in  for INSTANT macro playback!
6. Press F11 to stop playing

Features:
• Automatic trigger - no need to click Play!
• Global hotkeys for hands-free operation
• Instant macro start when triggered
• Stop playing hotkey for quick control
• Auto-removes last 2 seconds
• Fixed key holding issues
• Real-time movement display"""
        
        self.movements_text.insert("1.0", initial_text)
