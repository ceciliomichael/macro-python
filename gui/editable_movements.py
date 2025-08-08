"""
Editable Movements Display for  Macro Recorder
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import customtkinter as ctk
from .gui_styles import ThemeManager, StyleHelper
import json

class EditableMovementsDisplay:
    """Editable movements display with row-based editing"""
    
    def __init__(self, parent, recorder):
        self.parent = parent
        self.recorder = recorder
        self.frame = None
        self.tree = None
        self.context_menu = None
        self.selected_item = None
        
    def create(self):
        """Create the editable movements display"""
        self.frame = StyleHelper.create_frame(
            self.parent,
            width=480
        )
        self.frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        self.frame.pack_propagate(False)
        
        # Title
        title = StyleHelper.create_label(
            self.frame,
            text="Macro Events Editor",
            style='heading',
            color=ThemeManager.COLORS['warning']
        )
        title.pack(pady=(15, 10))
        
        # Toolbar
        self._create_toolbar()
        
        # Treeview container
        tree_frame = StyleHelper.create_frame(
            self.frame, 
            fg_color="transparent"
        )
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Create treeview with custom styling
        self._create_treeview(tree_frame)
        
        # Context menu
        self._create_context_menu()
        
        # Initial instructions
        self._show_initial_instructions()
        
        return self.frame
    
    def _create_toolbar(self):
        """Create toolbar with action buttons"""
        toolbar = StyleHelper.create_frame(
            self.frame,
            fg_color="transparent"
        )
        toolbar.pack(fill="x", padx=20, pady=(0, 10))
        
        # Add event button
        add_btn = StyleHelper.create_button(
            toolbar,
            text="➕ Add Event",
            style_type='apply',
            command=self.add_new_event,
            width=100,
            height=25
        )
        add_btn.pack(side="left", padx=(0, 5))
        
        # Clear all button
        clear_btn = StyleHelper.create_button(
            toolbar,
            text="🗑️ Clear All",
            style_type='apply',
            command=self.clear_all_events,
            width=100,
            height=25,
            fg_color=ThemeManager.COLORS['danger']
        )
        clear_btn.pack(side="left", padx=(0, 5))
        
        # Import button
        import_btn = StyleHelper.create_button(
            toolbar,
            text="📥 Import",
            style_type='apply',
            command=self.import_from_recording,
            width=100,
            height=25
        )
        import_btn.pack(side="left", padx=(0, 5))
        
        # Export button
        export_btn = StyleHelper.create_button(
            toolbar,
            text="📤 Export",
            style_type='apply',
            command=self.export_to_recorder,
            width=100,
            height=25
        )
        export_btn.pack(side="left")
    
    def _create_treeview(self, parent):
        """Create the treeview for displaying events"""
        # Create custom style for treeview
        style = ttk.Style()
        style.theme_use('clam')
        
        # Beautiful dark theme styling
        style.configure("Custom.Treeview", 
                       background="#1a1a2e",
                       foreground="#f0f8ff",
                       fieldbackground="#1a1a2e",
                       borderwidth=0,
                       relief="flat",
                       font=('Segoe UI', 11),
                       rowheight=28)
        
        style.configure("Custom.Treeview.Heading",
                       background="#16213e",
                       foreground="#e94560",
                       font=('Segoe UI', 11, 'bold'),
                       relief="flat",
                       borderwidth=1)
        
        style.map("Custom.Treeview",
                 background=[('selected', ThemeManager.COLORS['secondary']),
                           ('focus', '#0f3460')],
                 foreground=[('selected', '#ffffff')])
        
        style.map("Custom.Treeview.Heading",
                 background=[('active', '#0f3460')])
        
        # Create beautiful container with gradient-like effect
        tree_container = StyleHelper.create_frame(parent, corner_radius=10, fg_color="#16213e")
        tree_container.pack(fill="both", expand=True)
        
        # Inner container for padding
        inner_container = tk.Frame(tree_container, bg="#1a1a2e")
        inner_container.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Columns: Type, Details, Timestamp
        self.tree = ttk.Treeview(
            inner_container,
            columns=("type", "details", "timestamp"),
            show="tree headings",
            height=15,
            style="Custom.Treeview"
        )
        
        # Configure columns with better headers
        self.tree.heading("#0", text="🔢 ID")
        self.tree.heading("type", text="🎯 Event Type")
        self.tree.heading("details", text="📝 Details")
        self.tree.heading("timestamp", text="⏰ Time")
        
        self.tree.column("#0", width=60, minwidth=60, anchor="center")
        self.tree.column("type", width=120, minwidth=100, anchor="w")
        self.tree.column("details", width=260, minwidth=200, anchor="w")
        self.tree.column("timestamp", width=80, minwidth=70, anchor="center")
        
        # Beautiful scrollbar
        scrollbar_frame = tk.Frame(inner_container, bg="#1a1a2e", width=15)
        scrollbar_frame.pack(side="right", fill="y")
        
        scrollbar = ttk.Scrollbar(
            scrollbar_frame, 
            orient="vertical", 
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Custom scrollbar styling
        style.configure("Vertical.TScrollbar",
                       background="#16213e",
                       troughcolor="#1a1a2e",
                       borderwidth=0,
                       arrowcolor="#e94560",
                       darkcolor="#16213e",
                       lightcolor="#16213e")
        
        # Pack treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y", padx=(2, 0))
        
        # Bind events with visual feedback
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right click
        self.tree.bind("<Double-1>", self.edit_selected_event)  # Double click
        self.tree.bind("<Motion>", self._on_hover)  # Hover effect
        self.tree.bind("<Leave>", self._on_leave)  # Leave hover
    
    def _on_hover(self, event):
        """Add hover effect"""
        item = self.tree.identify_row(event.y)
        if item and not item.startswith("instruction_"):
            self.tree.configure(cursor="hand2")
    
    def _on_leave(self, event):
        """Remove hover effect"""
        self.tree.configure(cursor="")
    
    def _create_context_menu(self):
        """Create beautiful right-click context menu"""
        self.context_menu = tk.Menu(
            self.frame, 
            tearoff=0, 
            bg="#16213e", 
            fg="#f0f8ff",
            activebackground=ThemeManager.COLORS['secondary'],
            activeforeground="#ffffff",
            selectcolor=ThemeManager.COLORS['primary'],
            font=('Segoe UI', 10),
            borderwidth=0,
            relief="flat"
        )
        
        # Add commands with beautiful icons and styling
        self.context_menu.add_command(
            label="✏️  Edit Event", 
            command=self.edit_selected_event,
            accelerator="Double-click"
        )
        self.context_menu.add_command(
            label="📋  Duplicate Event", 
            command=self.duplicate_selected_event,
            accelerator="Ctrl+D"
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="➕  Insert Above", 
            command=lambda: self.add_new_event(insert_above=True)
        )
        self.context_menu.add_command(
            label="➕  Insert Below", 
            command=lambda: self.add_new_event(insert_below=True)
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="🗑️  Delete Event", 
            command=self.delete_selected_event,
            accelerator="Delete"
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="⬆️  Move Up", 
            command=self.move_event_up,
            accelerator="Ctrl+↑"
        )
        self.context_menu.add_command(
            label="⬇️  Move Down", 
            command=self.move_event_down,
            accelerator="Ctrl+↓"
        )
    
    def show_context_menu(self, event):
        """Show context menu on right click"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.selected_item = item
            self.context_menu.post(event.x_root, event.y_root)
    
    def _show_initial_instructions(self):
        """Show initial instructions in the treeview"""
        instructions = [
            ("info", "Right-click anywhere to add events", "📝 Instructions", "0.0"),
            ("info", "Double-click or right-click to edit", "📝 Instructions", "0.0"),
            ("info", "Import from recording or create custom", "📝 Instructions", "0.0"),
            ("info", "Drag events to reorder (coming soon)", "📝 Instructions", "0.0")
        ]
        
        for i, (event_type, details, category, timestamp) in enumerate(instructions):
            self.tree.insert("", "end", iid=f"instruction_{i}", 
                           text=str(i+1), values=(category, details, timestamp))
    
    def refresh_display(self):
        """Refresh the display with current recorder events"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not hasattr(self.recorder, 'events') or not self.recorder.events:
            self._show_initial_instructions()
            return
        
        # Add events from recorder
        for i, event in enumerate(self.recorder.events):
            event_type = event['type']
            details = self._format_event_details(event)
            timestamp = f"{event['timestamp']:.2f}"
            
            # Color coding by event type
            icon = self._get_event_icon(event_type)
            
            self.tree.insert("", "end", iid=str(i), 
                           text=str(i+1), values=(f"{icon} {event_type}", details, timestamp))
    
    def _format_event_details(self, event):
        """Format event details for display"""
        event_type = event['type']
        
        if event_type == 'mouse_click':
            action = "Press" if event['pressed'] else "Release"
            return f"{action} {event['button']} at ({event['x']}, {event['y']})"
        
        elif event_type == 'mouse_move':
            return f"Move to ({event['x']}, {event['y']})"
        
        elif event_type == 'mouse_scroll':
            return f"Scroll ({event['dx']}, {event['dy']}) at ({event['x']}, {event['y']})"
        
        elif event_type in ['key_press', 'key_release']:
            action = "Press" if event_type == 'key_press' else "Release"
            return f"{action} '{event['key']}'"
        
        elif event_type == 'delay':
            duration = event.get('duration', 0)
            description = event.get('description', '')
            if description:
                return f"Wait {duration}s - {description}"
            else:
                return f"Wait {duration} seconds"
        
        else:
            return str(event)
    
    def _get_event_icon(self, event_type):
        """Get icon for event type"""
        icons = {
            'mouse_click': '🖱️',
            'mouse_move': '↗️',
            'mouse_scroll': '🔄',
            'key_press': '⌨️',
            'key_release': '⌨️',
            'delay': '⏰'
        }
        return icons.get(event_type, '❓')
    
    def edit_selected_event(self, event=None):
        """Edit the selected event"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select an event to edit.")
            return
        
        item_id = selection[0]
        
        # Skip instruction items
        if item_id.startswith("instruction_"):
            self.add_new_event()
            return
        
        try:
            event_index = int(item_id)
            if event_index < len(self.recorder.events):
                event_data = self.recorder.events[event_index]
                self._show_event_editor(event_data, event_index)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid event selected.")
    
    def _show_event_editor(self, event_data, event_index):
        """Show event editor dialog"""
        editor = EventEditorDialog(self.frame, event_data, event_index >= 0)
        if editor.result:
            if event_index >= 0:
                # Update existing event
                self.recorder.events[event_index] = editor.result
            else:
                # Add new event
                self.recorder.events.append(editor.result)
            
            self.refresh_display()
    
    def add_new_event(self, insert_above=False, insert_below=False):
        """Add a new event"""
        # Create default event
        default_event = {
            'type': 'delay',
            'timestamp': 1.0,
            'duration': 1.0,
            'description': 'Wait before next action'
        }
        
        editor = EventEditorDialog(self.frame, default_event, is_new=True)
        if editor.result:
            insert_index = len(self.recorder.events)
            
            if insert_above and self.selected_item:
                try:
                    insert_index = int(self.selected_item)
                except ValueError:
                    pass
            elif insert_below and self.selected_item:
                try:
                    insert_index = int(self.selected_item) + 1
                except ValueError:
                    pass
            
            self.recorder.events.insert(insert_index, editor.result)
            self.refresh_display()
    
    def duplicate_selected_event(self):
        """Duplicate the selected event"""
        selection = self.tree.selection()
        if not selection:
            return
        
        try:
            event_index = int(selection[0])
            if event_index < len(self.recorder.events):
                event_copy = self.recorder.events[event_index].copy()
                self.recorder.events.insert(event_index + 1, event_copy)
                self.refresh_display()
        except (ValueError, IndexError):
            pass
    
    def delete_selected_event(self):
        """Delete the selected event"""
        selection = self.tree.selection()
        if not selection:
            return
        
        try:
            event_index = int(selection[0])
            if event_index < len(self.recorder.events):
                del self.recorder.events[event_index]
                self.refresh_display()
        except (ValueError, IndexError):
            pass
    
    def move_event_up(self):
        """Move selected event up"""
        selection = self.tree.selection()
        if not selection:
            return
        
        try:
            event_index = int(selection[0])
            if event_index > 0 and event_index < len(self.recorder.events):
                # Swap with previous event
                self.recorder.events[event_index], self.recorder.events[event_index-1] = \
                    self.recorder.events[event_index-1], self.recorder.events[event_index]
                self.refresh_display()
                # Keep selection on moved item
                self.tree.selection_set(str(event_index-1))
        except (ValueError, IndexError):
            pass
    
    def move_event_down(self):
        """Move selected event down"""
        selection = self.tree.selection()
        if not selection:
            return
        
        try:
            event_index = int(selection[0])
            if event_index < len(self.recorder.events) - 1:
                # Swap with next event
                self.recorder.events[event_index], self.recorder.events[event_index+1] = \
                    self.recorder.events[event_index+1], self.recorder.events[event_index]
                self.refresh_display()
                # Keep selection on moved item
                self.tree.selection_set(str(event_index+1))
        except (ValueError, IndexError):
            pass
    
    def clear_all_events(self):
        """Clear all events"""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all events?"):
            self.recorder.events = []
            self.refresh_display()
    
    def import_from_recording(self):
        """Import events from the current recording"""
        if hasattr(self.recorder, 'events') and self.recorder.events:
            self.refresh_display()
            messagebox.showinfo("Imported", f"Imported {len(self.recorder.events)} events from recording.")
        else:
            messagebox.showinfo("No Recording", "No recorded events to import. Record some actions first.")
    
    def export_to_recorder(self):
        """Export current events to the recorder"""
        if not hasattr(self.recorder, 'events'):
            self.recorder.events = []
        
        messagebox.showinfo("Exported", f"Exported {len(self.recorder.events)} events to macro recorder.")
    
    # Legacy compatibility methods
    def show_recording_started(self):
        """Legacy method - no action needed for editable display"""
        pass
    
    def start_realtime_updates(self):
        """Legacy method - no action needed for editable display"""
        pass
    
    def stop_realtime_updates(self):
        """Legacy method - no action needed for editable display"""
        pass
    
    def display_movements(self):
        """Legacy method - redirect to refresh_display"""
        self.refresh_display()
    
    def clear_display(self):
        """Clear the display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._show_initial_instructions()
    
    def show_no_macro_message(self):
        """Show message when no macro is available"""
        self.clear_display()
    
    def show_error_message(self, message):
        """Show an error message"""
        # Could add a status bar or tooltip here in the future
        messagebox.showerror("Error", message)
    
    def show_status_message(self, message):
        """Show a status message"""
        # Could add a status bar here in the future
        pass


class EventEditorDialog:
    """Dialog for editing individual events"""
    
    def __init__(self, parent, event_data, is_new=False):
        self.parent = parent
        self.event_data = event_data.copy()
        self.is_new = is_new
        self.result = None
        
        self.dialog = None
        self.entries = {}
        
        self._create_dialog()
    
    def _create_dialog(self):
        """Create a sleek, professional event editor dialog"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Event Editor" if not self.is_new else "New Event")
        self.dialog.geometry("500x400")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Configure window
        self.dialog.focus()
        
        # Main container
        container = ctk.CTkFrame(self.dialog, corner_radius=0)
        container.pack(fill="both", expand=True)
        
        # Header section
        header = ctk.CTkFrame(container, height=80, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Title and icon
        title_container = ctk.CTkFrame(header, fg_color="transparent")
        title_container.pack(expand=True, fill="both", padx=20, pady=15)
        
        # Event type icon (will be updated dynamically)
        self.dialog_icon = ctk.CTkLabel(
            title_container,
            text="🎯",
            font=ctk.CTkFont(size=32)
        )
        self.dialog_icon.pack(side="left", padx=(0, 15))
        
        # Title and description
        text_container = ctk.CTkFrame(title_container, fg_color="transparent")
        text_container.pack(side="left", fill="both", expand=True)
        
        title = ctk.CTkLabel(
            text_container,
            text="Event Editor" if not self.is_new else "Create New Event",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        title.pack(anchor="w")
        
        self.dialog_subtitle = ctk.CTkLabel(
            text_container,
            text="Configure event properties",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        self.dialog_subtitle.pack(anchor="w", pady=(2, 0))
        
        # Content area with scrollable frame
        content_frame = ctk.CTkScrollableFrame(
            container,
            height=220,
            corner_radius=0
        )
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Event type selection (simplified)
        self._create_simple_type_selection(content_frame)
        
        # Dynamic fields container
        self.fields_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.fields_container.pack(fill="x", pady=(15, 0))
        
        self._update_fields()
        
        # Bottom button bar
        self._create_modern_buttons(container)
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def _create_simple_type_selection(self, parent):
        """Create simplified event type selection"""
        type_frame = ctk.CTkFrame(parent, fg_color="transparent")
        type_frame.pack(fill="x")
        
        ctk.CTkLabel(
            type_frame, 
            text="Event Type", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(0, 8))
        
        self.type_var = ctk.StringVar(value=self.event_data.get('type', 'delay'))
        
        # Create radio-style buttons for event types
        self.type_buttons = {}
        type_options = [
            ("delay", "⏰ Delay", "Add a wait/pause between actions"),
            ("mouse_click", "🖱️ Mouse Click", "Click at specific coordinates"),
            ("mouse_move", "↗️ Mouse Move", "Move cursor to position"),
            ("key_press", "⌨️ Key Press", "Press a keyboard key"),
            ("key_release", "⌨️ Key Release", "Release a keyboard key"),
            ("mouse_scroll", "🔄 Mouse Scroll", "Scroll mouse wheel")
        ]
        
        for i, (value, label, description) in enumerate(type_options):
            btn_frame = ctk.CTkFrame(type_frame, fg_color="transparent")
            btn_frame.pack(fill="x", pady=2)
            
            radio_btn = ctk.CTkRadioButton(
                btn_frame,
                text=f"{label} - {description}",
                variable=self.type_var,
                value=value,
                command=self._on_type_change,
                font=ctk.CTkFont(size=12)
            )
            radio_btn.pack(anchor="w")
            self.type_buttons[value] = radio_btn
    
    def _on_type_change(self, selected_type=None):
        """Handle event type change"""
        event_type = self.type_var.get()
        self.event_data['type'] = event_type
        
        # Update dialog icon and subtitle
        icons = {
            'delay': '⏰',
            'mouse_click': '🖱️',
            'mouse_move': '↗️',
            'key_press': '⌨️',
            'key_release': '⌨️',
            'mouse_scroll': '🔄'
        }
        
        descriptions = {
            'delay': 'Configure wait time between actions',
            'mouse_click': 'Set click position and button',
            'mouse_move': 'Set cursor movement target',
            'key_press': 'Configure keyboard key press',
            'key_release': 'Configure keyboard key release',
            'mouse_scroll': 'Set scroll direction and amount'
        }
        
        self.dialog_icon.configure(text=icons.get(event_type, '🎯'))
        self.dialog_subtitle.configure(text=descriptions.get(event_type, 'Configure event properties'))
        
        self._update_fields()
    
    def _update_fields(self):
        """Update fields based on selected event type"""
        # Clear existing fields
        for widget in self.fields_container.winfo_children():
            widget.destroy()
        self.entries = {}
        
        event_type = self.type_var.get()
        
        # Create fields container with nice styling
        fields_frame = ctk.CTkFrame(self.fields_container, fg_color="transparent")
        fields_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(
            fields_frame, 
            text="Properties", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(0, 10))
        
        # Common fields
        self._add_modern_field(fields_frame, "timestamp", "Timestamp (seconds)", "float", "When this event occurs")
        
        # Type-specific fields
        if event_type in ['mouse_click', 'mouse_move', 'mouse_scroll']:
            self._add_modern_field(fields_frame, "x", "X Position", "int", "Horizontal pixel coordinate")
            self._add_modern_field(fields_frame, "y", "Y Position", "int", "Vertical pixel coordinate")
            
            if event_type == 'mouse_click':
                self._add_modern_field(fields_frame, "button", "Mouse Button", "choice", "Which button to click", ["left", "right", "middle"])
                self._add_modern_field(fields_frame, "pressed", "Action", "choice", "Press or release the button", ["Press", "Release"])
            
            elif event_type == 'mouse_scroll':
                self._add_modern_field(fields_frame, "dx", "Horizontal Scroll", "int", "Scroll amount left/right")
                self._add_modern_field(fields_frame, "dy", "Vertical Scroll", "int", "Scroll amount up/down")
        
        elif event_type in ['key_press', 'key_release']:
            self._add_modern_field(fields_frame, "key", "Key", "string", "Keyboard key to press/release")
        
        elif event_type == 'delay':
            self._add_modern_field(fields_frame, "duration", "Wait Duration (seconds)", "float", "How long to wait")
            self._add_modern_field(fields_frame, "description", "Description (optional)", "string", "What this delay is for")
    
    def _add_field(self, field_name, label, field_type, choices=None):
        """Add a field to the dialog"""
        field_frame = ctk.CTkFrame(self.fields_frame, fg_color="transparent")
        field_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(field_frame, text=label).pack(anchor="w")
        
        current_value = self.event_data.get(field_name, "")
        
        if field_type == "choice" and choices:
            var = ctk.StringVar()
            if field_name == "pressed":
                var.set("Press" if current_value else "Release")
            else:
                var.set(str(current_value))
            
            widget = ctk.CTkComboBox(field_frame, variable=var, values=choices)
            self.entries[field_name] = (var, "choice")
        
        else:
            var = ctk.StringVar(value=str(current_value))
            widget = ctk.CTkEntry(field_frame, textvariable=var)
            self.entries[field_name] = (var, field_type)
        
        widget.pack(fill="x", pady=(5, 0))
    
    def _add_modern_field(self, parent, field_name, label, field_type, help_text, choices=None):
        """Add a modern styled field with help text"""
        field_container = ctk.CTkFrame(parent, fg_color="transparent")
        field_container.pack(fill="x", pady=(0, 15))
        
        # Label with help text
        label_frame = ctk.CTkFrame(field_container, fg_color="transparent")
        label_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(
            label_frame,
            text=label,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            label_frame,
            text=f"({help_text})",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        ).pack(side="right")
        
        # Input field
        current_value = self.event_data.get(field_name, "")
        
        if field_type == "choice" and choices:
            var = ctk.StringVar()
            if field_name == "pressed":
                var.set("Press" if current_value else "Release")
            else:
                var.set(str(current_value))
            
            widget = ctk.CTkComboBox(
                field_container, 
                variable=var, 
                values=choices,
                width=200
            )
            self.entries[field_name] = (var, "choice")
        
        else:
            var = ctk.StringVar(value=str(current_value))
            widget = ctk.CTkEntry(
                field_container, 
                textvariable=var,
                width=200,
                font=ctk.CTkFont(size=12)
            )
            self.entries[field_name] = (var, field_type)
        
        widget.pack(anchor="w")
    
    def _create_modern_buttons(self, parent):
        """Create modern dialog buttons"""
        button_bar = ctk.CTkFrame(parent, height=60, corner_radius=0)
        button_bar.pack(fill="x", side="bottom")
        button_bar.pack_propagate(False)
        
        button_container = ctk.CTkFrame(button_bar, fg_color="transparent")
        button_container.pack(side="right", padx=20, pady=15)
        
        cancel_btn = ctk.CTkButton(
            button_container,
            text="Cancel",
            command=self._cancel,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            border_color=("gray20", "gray60"),
            width=100,
            height=32,
            hover_color=("gray80", "gray30")
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = ctk.CTkButton(
            button_container,
            text="Save Event",
            command=self._save,
            width=120,
            height=32,
            font=ctk.CTkFont(weight="bold")
        )
        save_btn.pack(side="right")
    
    def _save(self):
        """Save the event"""
        try:
            # Build event data
            result = {'type': self.type_var.get()}
            
            for field_name, (var, field_type) in self.entries.items():
                value = var.get()
                
                if field_type == "int":
                    result[field_name] = int(value)
                elif field_type == "float":
                    result[field_name] = float(value)
                elif field_type == "choice" and field_name == "pressed":
                    result[field_name] = value == "Press"
                else:
                    result[field_name] = value
            
            self.result = result
            self.dialog.destroy()
        
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please check your input values:\n{str(e)}")
    
    def _cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()

