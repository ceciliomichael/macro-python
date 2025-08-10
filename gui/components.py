"""
Modular GUI Components for  Macro Recorder
"""
import customtkinter as ctk
from tkinter import ttk, messagebox
import uuid
from datetime import datetime
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
        # Scheduler state
        self.scheduler_enabled_var = None
        self.schedules = []
        self.scheduler_tree = None
        
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
        
        # Tabs for features
        tabview = ctk.CTkTabview(self.frame)
        tabview.pack(fill="both", expand=True, padx=12, pady=10)
        general_tab = tabview.add("General")
        hotkeys_tab = tabview.add("Hotkeys")
        scheduler_tab = tabview.add("Scheduler")
        
        # General tab
        self._create_trigger_section(general_tab)
        self._create_interval_section(general_tab)
        self._create_loop_section(general_tab)
        self._create_file_section(general_tab)
        
        # Hotkeys tab
        self._create_hotkeys_section(hotkeys_tab)
        
        # Scheduler tab
        self._create_scheduler_section(scheduler_tab)
        
        return self.frame
    
    def _create_trigger_section(self, parent):
        """Create trigger key input section"""
        trigger_frame = StyleHelper.create_frame(
            parent, 
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
    
    def _create_hotkeys_section(self, parent):
        """Create recording hotkeys section"""
        hotkey_frame = StyleHelper.create_frame(
            parent, 
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
    
    def _create_interval_section(self, parent):
        """Create repeat interval section"""
        interval_frame = StyleHelper.create_frame(
            parent, 
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
    
    def _create_loop_section(self, parent):
        """Create loop checkbox section"""
        self.loop_var = ctk.BooleanVar(value=True)
        self.loop_checkbox = StyleHelper.create_checkbox(
            parent,
            text="Loop continuously (for AFK prevention)",
            variable=self.loop_var
        )
        self.loop_checkbox.pack(padx=20, pady=10, anchor="w")
    
    def _create_file_section(self, parent):
        """Create file operations section"""
        file_frame = StyleHelper.create_frame(
            parent, 
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

    # ---------------- Scheduler UI ---------------- #
    def _create_scheduler_section(self, parent):
        section = StyleHelper.create_frame(parent, fg_color="transparent")
        section.pack(fill="both", expand=False, padx=20, pady=(10, 15))
        
        title = StyleHelper.create_label(
            section,
            text="Scheduler",
            style='subheading',
            anchor="w"
        )
        title.pack(fill="x", pady=(0, 8))
        
        # Enable toggle
        self.scheduler_enabled_var = ctk.BooleanVar(value=False)
        enable_row = StyleHelper.create_frame(section, fg_color="transparent")
        enable_row.pack(fill="x", pady=(0, 10))
        enable_chk = StyleHelper.create_checkbox(
            enable_row, text="Enable scheduled autoplay", variable=self.scheduler_enabled_var
        )
        enable_chk.pack(side="left")
        
        # Buttons
        btn_row = StyleHelper.create_frame(section, fg_color="transparent")
        btn_row.pack(fill="x", pady=(0, 8))
        StyleHelper.create_button(
            btn_row, text="➕ Add", style_type='apply', command=self._on_add_schedule, width=90, height=28
        ).pack(side="left", padx=(0, 6))
        StyleHelper.create_button(
            btn_row, text="✏️ Edit", style_type='apply', command=self._on_edit_schedule, width=90, height=28
        ).pack(side="left", padx=(0, 6))
        StyleHelper.create_button(
            btn_row, text="🗑️ Delete", style_type='apply', command=self._on_delete_schedule, width=90, height=28,
            fg_color=ThemeManager.COLORS['danger']
        ).pack(side="left")
        StyleHelper.create_button(
            btn_row, text="Apply Scheduler", style_type='apply', command=self._apply_scheduler, width=140, height=28
        ).pack(side="right")
        
        # Table
        table_container = StyleHelper.create_frame(section)
        table_container.pack(fill="both", expand=False)
        
        self.scheduler_tree = ttk.Treeview(
            table_container,
            columns=("type", "detail", "next"),
            show="headings",
            height=6
        )
        self.scheduler_tree.heading("type", text="Type")
        self.scheduler_tree.heading("detail", text="Detail")
        self.scheduler_tree.heading("next", text="Next Run")
        self.scheduler_tree.column("type", width=90, anchor="center")
        self.scheduler_tree.column("detail", width=240, anchor="w")
        self.scheduler_tree.column("next", width=120, anchor="center")
        self.scheduler_tree.pack(fill="x", expand=False, padx=8, pady=8)
        
        self.refresh_scheduler_table()
    
    def set_scheduler_state(self, enabled, schedules):
        self.scheduler_enabled_var.set(bool(enabled))
        self.schedules = list(schedules or [])
        self.refresh_scheduler_table()
    
    def get_scheduler_state(self):
        return bool(self.scheduler_enabled_var.get()), list(self.schedules)
    
    def refresh_scheduler_table(self):
        if not self.scheduler_tree:
            return
        for iid in self.scheduler_tree.get_children():
            self.scheduler_tree.delete(iid)
        # Compute next runs using controller scheduler if available
        for s in self.schedules:
            detail = self._format_schedule_detail(s)
            next_run = None
            try:
                next_dt = self.controller.scheduler._compute_next_run(s)
                next_run = next_dt.strftime("%Y-%m-%d %H:%M:%S") if next_dt else "—"
            except Exception:
                next_run = "—"
            self.scheduler_tree.insert("", "end", iid=s.get("id", str(uuid.uuid4())), values=(s.get("type"), detail, next_run))
    
    def _format_schedule_detail(self, s):
        st = s.get("type")
        if st == "once":
            return f"Once at {s.get('datetime','')}"
        if st == "daily":
            return f"Daily at {s.get('time','')}"
        if st == "weekly":
            days = s.get('days') or []
            return f"Weekly {s.get('time','')} on {','.join(str(d) for d in days)}"
        if st == "interval":
            return f"Every {s.get('interval_seconds', 0)}s"
        return "—"
    
    def _on_add_schedule(self):
        new_sched = self._open_schedule_dialog()
        if new_sched:
            self.schedules.append(new_sched)
            self.refresh_scheduler_table()
    
    def _on_edit_schedule(self):
        sel = self.scheduler_tree.selection()
        if not sel:
            messagebox.showinfo("No selection", "Select a schedule to edit.")
            return
        iid = sel[0]
        idx = next((i for i, s in enumerate(self.schedules) if s.get('id') == iid), None)
        if idx is None:
            return
        edited = self._open_schedule_dialog(self.schedules[idx])
        if edited:
            # preserve id
            edited['id'] = self.schedules[idx].get('id', edited.get('id'))
            self.schedules[idx] = edited
            self.refresh_scheduler_table()
    
    def _on_delete_schedule(self):
        sel = self.scheduler_tree.selection()
        if not sel:
            return
        iid = sel[0]
        self.schedules = [s for s in self.schedules if s.get('id') != iid]
        self.refresh_scheduler_table()
    
    def _apply_scheduler(self):
        if hasattr(self.controller, 'save_settings'):
            self.controller.save_settings()
            self.controller.update_status("Scheduler settings applied")
    
    def _open_schedule_dialog(self, existing=None):
        dlg = ctk.CTkToplevel(self.frame)
        dlg.title("Schedule")
        dlg.geometry("420x360")
        dlg.transient(self.frame)
        dlg.grab_set()
        container = ctk.CTkFrame(dlg)
        container.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Type
        ctk.CTkLabel(container, text="Type").pack(anchor="w")
        type_var = ctk.StringVar(value=(existing.get('type') if existing else 'once'))
        type_cb = ctk.CTkComboBox(container, values=["once", "daily", "weekly", "interval"], variable=type_var, width=160)
        type_cb.pack(anchor="w", pady=(4, 10))
        
        # Stacked inputs
        time_var = ctk.StringVar(value=(existing.get('time') if existing else "08:00"))
        datetime_var = ctk.StringVar(value=(existing.get('datetime') if existing else datetime.now().strftime("%Y-%m-%d %H:%M")))
        interval_var = ctk.StringVar(value=(str(existing.get('interval_seconds')) if existing and existing.get('interval_seconds') is not None else "300"))
        allow_overlap_var = ctk.BooleanVar(value=(bool(existing.get('allow_overlap')) if existing else False))
        days_vars = [ctk.BooleanVar(value=False) for _ in range(7)]
        if existing and existing.get('days'):
            for d in existing['days']:
                try:
                    days_vars[int(d)].set(True)
                except Exception:
                    pass
        
        # Once
        once_frame = StyleHelper.create_frame(container, fg_color="transparent")
        ctk.CTkLabel(once_frame, text="Date & Time (YYYY-MM-DD HH:MM)").pack(anchor="w")
        once_entry = ctk.CTkEntry(once_frame, textvariable=datetime_var, width=240)
        once_entry.pack(anchor="w", pady=(4, 8))
        
        # Daily
        daily_frame = StyleHelper.create_frame(container, fg_color="transparent")
        ctk.CTkLabel(daily_frame, text="Time (HH:MM or HH:MM:SS)").pack(anchor="w")
        daily_entry = ctk.CTkEntry(daily_frame, textvariable=time_var, width=180)
        daily_entry.pack(anchor="w", pady=(4, 8))
        
        # Weekly
        weekly_frame = StyleHelper.create_frame(container, fg_color="transparent")
        ctk.CTkLabel(weekly_frame, text="Time (HH:MM)").pack(anchor="w")
        weekly_entry = ctk.CTkEntry(weekly_frame, textvariable=time_var, width=180)
        weekly_entry.pack(anchor="w", pady=(4, 6))
        days_row = StyleHelper.create_frame(weekly_frame, fg_color="transparent")
        days_row.pack(fill="x")
        day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, lbl in enumerate(day_labels):
            ctk.CTkCheckBox(days_row, text=lbl, variable=days_vars[i]).pack(side="left", padx=(0, 4))
        
        # Interval
        interval_frame = StyleHelper.create_frame(container, fg_color="transparent")
        ctk.CTkLabel(interval_frame, text="Interval (seconds)").pack(anchor="w")
        interval_entry = ctk.CTkEntry(interval_frame, textvariable=interval_var, width=120)
        interval_entry.pack(anchor="w", pady=(4, 8))
        
        # Common: overlap
        overlap_chk = ctk.CTkCheckBox(container, text="Allow overlap while playing", variable=allow_overlap_var)
        overlap_chk.pack(anchor="w", pady=(6, 6))
        
        # Switch visible section based on type
        def update_visibility(*_):
            for f in (once_frame, daily_frame, weekly_frame, interval_frame):
                f.pack_forget()
            t = type_var.get()
            if t == 'once':
                once_frame.pack(fill="x")
            elif t == 'daily':
                daily_frame.pack(fill="x")
            elif t == 'weekly':
                weekly_frame.pack(fill="x")
            elif t == 'interval':
                interval_frame.pack(fill="x")
        update_visibility()
        type_cb.configure(command=lambda _v: update_visibility())
        
        # Buttons
        btn_bar = StyleHelper.create_frame(container, fg_color="transparent")
        btn_bar.pack(fill="x", pady=(10, 0))
        result_holder = {"value": None}
        
        def on_save():
            try:
                sched = {
                    'id': existing.get('id') if existing else str(uuid.uuid4()),
                    'type': type_var.get(),
                    'enabled': True,
                    'allow_overlap': bool(allow_overlap_var.get()),
                }
                t = type_var.get()
                if t == 'once':
                    sched['datetime'] = datetime_var.get().strip()
                elif t == 'daily':
                    sched['time'] = time_var.get().strip()
                elif t == 'weekly':
                    sched['time'] = time_var.get().strip()
                    sched['days'] = [i for i, v in enumerate(days_vars) if v.get()]
                elif t == 'interval':
                    sched['interval_seconds'] = int(interval_var.get().strip())
                result_holder['value'] = sched
                dlg.destroy()
            except Exception as e:
                messagebox.showerror("Invalid input", str(e))
        
        def on_cancel():
            result_holder['value'] = None
            dlg.destroy()
        
        ctk.CTkButton(btn_bar, text="Cancel", command=on_cancel, fg_color="transparent", border_width=2,
                      border_color=("gray20", "gray60"), width=100).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btn_bar, text="Save", command=on_save, width=100).pack(side="right")
        
        dlg.wait_window()
        return result_holder['value']

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
