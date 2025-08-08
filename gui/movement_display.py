"""
Movement Display Manager for  Macro Recorder
"""
import threading

class MovementDisplayManager:
    """Manages the display and formatting of recorded movements"""
    
    def __init__(self, text_widget, recorder):
        self.text_widget = text_widget
        self.recorder = recorder
        self.is_updating = False
    
    def start_realtime_updates(self):
        """Start real-time updates during recording"""
        if not self.is_updating:
            self.is_updating = True
            self._update_loop()
    
    def stop_realtime_updates(self):
        """Stop real-time updates"""
        self.is_updating = False
    
    def _update_loop(self):
        """Continuous update loop for real-time display"""
        if self.is_updating and hasattr(self.recorder, 'events'):
            self.display_movements()
            threading.Timer(0.5, self._update_loop).start()
    
    def display_movements(self):
        """Display recorded movements in the text area"""
        if not hasattr(self.recorder, 'events') or not self.recorder.events:
            return
        
        # Clear current content
        self.text_widget.delete("1.0", "end")
        
        # Generate and display content
        content = self._generate_movement_content()
        self.text_widget.insert("1.0", content)
        
        # Scroll to top
        self.text_widget.see("1.0")
    
    def _generate_movement_content(self):
        """Generate formatted content for movement display"""
        events = self.recorder.events
        
        # Header
        header = f"📊 Macro Summary: {len(events)} events\n"
        if events:
            duration = events[-1]['timestamp']
            header += f"⏱️ Duration: {duration:.2f} seconds\n\n"
        
        # Event details
        event_details = self._format_events(events)
        
        # Summary statistics
        summary = self._generate_summary(events)
        
        return header + event_details + summary
    
    def _format_events(self, events):
        """Format individual events for display"""
        formatted_events = []
        
        for event in events:
            event_type = event['type']
            timestamp = event['timestamp']
            
            if event_type == 'mouse_click':
                button = event['button']
                action = "Press" if event['pressed'] else "Release"
                formatted_events.append(
                    f"🖱️ {action} {button} at ({event['x']}, {event['y']}) - {timestamp:.2f}s"
                )
            
            elif event_type == 'mouse_scroll':
                formatted_events.append(
                    f"🔄 Scroll ({event['dx']}, {event['dy']}) at ({event['x']}, {event['y']}) - {timestamp:.2f}s"
                )
            
            elif event_type in ['key_press', 'key_release']:
                action = "Press" if event_type == 'key_press' else "Release"
                key = event['key']
                formatted_events.append(
                    f"⌨️ {action} '{key}' - {timestamp:.2f}s"
                )
        
        return "\n".join(formatted_events) + "\n\n" if formatted_events else ""
    
    def _generate_summary(self, events):
        """Generate summary statistics"""
        if not events:
            return ""
        
        # Count different event types
        mouse_moves = sum(1 for e in events if e['type'] == 'mouse_move')
        clicks = sum(1 for e in events if e['type'] == 'mouse_click')
        key_events = sum(1 for e in events if e['type'] in ['key_press', 'key_release'])
        
        summary_lines = []
        
        if mouse_moves > 0:
            summary_lines.append(f"📍 Total mouse movements: {mouse_moves}")
        
        summary_lines.append(f"🖱️ Total clicks: {clicks}")
        summary_lines.append(f"⌨️ Total key events: {key_events}")
        summary_lines.append("\n✨ Macro ready for playback!")
        
        return "\n".join(summary_lines)
    
    def clear_display(self):
        """Clear the movement display"""
        self.text_widget.delete("1.0", "end")
    
    def show_recording_started(self):
        """Show recording started message"""
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", "Recording started...\n\n")
    
    def show_no_macro_message(self):
        """Show message when no macro is available"""
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", "No macro recorded yet. Press F9 to start recording!")
    
    def show_error_message(self, message):
        """Show an error message in the display"""
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", f"❌ Error: {message}")
    
    def show_status_message(self, message):
        """Show a status message in the display"""
        current_content = self.text_widget.get("1.0", "end")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", f"📢 {message}\n\n{current_content}")
        self.text_widget.see("1.0")
