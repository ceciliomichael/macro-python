import time
import json
import threading
from datetime import datetime
from pynput import mouse, keyboard
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener

class MacroRecorder:
    def __init__(self):
        self.events = []
        self.recording = False
        self.playing = False
        self.start_time = None
        
        # Event listeners
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # Playback control
        self.playback_thread = None
        self.should_stop = False
    
    def start_recording(self):
        """Start recording mouse and keyboard events"""
        if self.recording:
            return
        
        self.recording = True
        self.events = []
        self.start_time = time.time()
        
        # Start mouse listener
        self.mouse_listener = MouseListener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        
        # Start keyboard listener
        self.keyboard_listener = KeyboardListener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
        print("Recording started...")
    
    def stop_recording(self):
        """Stop recording events"""
        if not self.recording:
            return
        
        self.recording = False
        
        # Stop listeners
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        # Remove last 2 seconds of events to avoid capturing stop action
        self.remove_last_seconds(2.0)
        
        print(f"Recording stopped. Captured {len(self.events)} events.")
    
    def remove_last_seconds(self, seconds):
        """Remove events from the last N seconds of recording"""
        if not self.events:
            return
        
        # Get the timestamp of the last event
        last_timestamp = self.events[-1]['timestamp']
        cutoff_timestamp = last_timestamp - seconds
        
        # Filter out events after the cutoff
        original_count = len(self.events)
        self.events = [event for event in self.events if event['timestamp'] <= cutoff_timestamp]
        
        removed_count = original_count - len(self.events)
        if removed_count > 0:
            print(f"Removed {removed_count} events from last {seconds} seconds")
    
    def on_mouse_move(self, x, y):
        """Record mouse movement events"""
        if self.recording:
            timestamp = time.time() - self.start_time
            event = {
                'type': 'mouse_move',
                'timestamp': timestamp,
                'x': x,
                'y': y
            }
            self.events.append(event)
    
    def on_mouse_click(self, x, y, button, pressed):
        """Record mouse click events"""
        if self.recording:
            timestamp = time.time() - self.start_time
            event = {
                'type': 'mouse_click',
                'timestamp': timestamp,
                'x': x,
                'y': y,
                'button': button.name,
                'pressed': pressed
            }
            self.events.append(event)
    
    def on_mouse_scroll(self, x, y, dx, dy):
        """Record mouse scroll events"""
        if self.recording:
            timestamp = time.time() - self.start_time
            event = {
                'type': 'mouse_scroll',
                'timestamp': timestamp,
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy
            }
            self.events.append(event)
    
    def on_key_press(self, key):
        """Record key press events"""
        if self.recording:
            timestamp = time.time() - self.start_time
            key_name = self.get_key_name(key)
            event = {
                'type': 'key_press',
                'timestamp': timestamp,
                'key': key_name
            }
            self.events.append(event)
    
    def on_key_release(self, key):
        """Record key release events"""
        if self.recording:
            timestamp = time.time() - self.start_time
            key_name = self.get_key_name(key)
            event = {
                'type': 'key_release',
                'timestamp': timestamp,
                'key': key_name
            }
            self.events.append(event)
            
            # Stop recording on Esc key (optional safety feature)
            if key == Key.esc:
                self.stop_recording()
                return False
    
    def get_key_name(self, key):
        """Convert key object to string representation"""
        try:
            return key.char
        except AttributeError:
            return str(key).replace('Key.', '')
    
    def play_macro_with_trigger(self, trigger_key, repeat_interval=60, loop=False, status_callback=None):
        """Play recorded macro when trigger key is pressed"""
        if not self.events:
            print("No events to play")
            return
        
        self.playing = True
        self.should_stop = False
        
        if status_callback:
            status_callback(f"Waiting for trigger key '{trigger_key}' - Press in  to start!")
        
        # Set up trigger listener
        def on_trigger_press(key):
            try:
                if hasattr(key, 'char') and key.char and key.char.lower() == trigger_key.lower():
                    return self.start_macro_playback(repeat_interval, loop, status_callback)
                elif hasattr(key, 'name') and key.name.lower() == trigger_key.lower():
                    return self.start_macro_playback(repeat_interval, loop, status_callback)
                elif str(key).replace('Key.', '').lower() == trigger_key.lower():
                    return self.start_macro_playback(repeat_interval, loop, status_callback)
            except:
                pass
            return True
        
        # Start trigger listener
        trigger_listener = KeyboardListener(on_press=on_trigger_press)
        trigger_listener.start()
        
        # Wait for trigger or stop signal
        while self.playing and not self.should_stop:
            time.sleep(0.1)
        
        # Clean up
        trigger_listener.stop()
        if status_callback:
            status_callback("Macro playback stopped")
    
    def start_macro_playback(self, repeat_interval, loop, status_callback):
        """Start the actual macro playback immediately after trigger"""
        if status_callback:
            status_callback("Trigger detected! Starting macro immediately...")
        
        # Start the macro playback immediately
        self.play_macro(repeat_interval, loop, status_callback)
        return False  # Stop the trigger listener
    
    def play_macro(self, repeat_interval=60, loop=False, status_callback=None):
        """Play recorded macro with optional looping"""
        if not self.events:
            print("No events to play")
            return
        
        self.playing = True
        self.should_stop = False
        
        iteration = 1
        
        try:
            while self.playing and not self.should_stop:
                if status_callback:
                    status_callback(f"Playing macro - Iteration {iteration}")
                
                # Play the sequence once
                self.play_sequence()
                
                if not loop:
                    break
                
                iteration += 1
                
                # Wait for the specified interval before repeating
                if status_callback:
                    status_callback(f"Waiting {repeat_interval}s before next iteration...")
                
                # Break the wait into smaller chunks to check for stop signal
                wait_time = 0
                while wait_time < repeat_interval and self.playing and not self.should_stop:
                    time.sleep(0.1)
                    wait_time += 0.1
                
        except Exception as e:
            print(f"Error during playback: {e}")
        finally:
            self.playing = False
            if status_callback:
                status_callback("Macro playback stopped")
    
    def play_sequence(self):
        """Play the recorded sequence once"""
        if not self.events:
            return
        
        # Initialize controllers
        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()
        
        # Track pressed keys to ensure they're released
        pressed_keys = set()
        pressed_buttons = set()
        
        start_time = time.time()
        
        for event in self.events:
            if self.should_stop or not self.playing:
                break
            
            # Wait for the correct timing
            target_time = start_time + event['timestamp']
            current_time = time.time()
            
            if target_time > current_time:
                time.sleep(target_time - current_time)
            
            # Execute the event
            try:
                if event['type'] == 'mouse_move':
                    mouse_controller.position = (event['x'], event['y'])
                
                elif event['type'] == 'mouse_click':
                    mouse_controller.position = (event['x'], event['y'])
                    button = getattr(Button, event['button'])
                    
                    if event['pressed']:
                        mouse_controller.press(button)
                        pressed_buttons.add(button)
                    else:
                        mouse_controller.release(button)
                        pressed_buttons.discard(button)
                
                elif event['type'] == 'mouse_scroll':
                    mouse_controller.position = (event['x'], event['y'])
                    mouse_controller.scroll(event['dx'], event['dy'])
                
                elif event['type'] == 'key_press':
                    key = self.string_to_key(event['key'])
                    keyboard_controller.press(key)
                    pressed_keys.add(key)
                
                elif event['type'] == 'key_release':
                    key = self.string_to_key(event['key'])
                    keyboard_controller.release(key)
                    pressed_keys.discard(key)
                
                elif event['type'] == 'delay':
                    # Handle delay events - wait for the specified duration
                    duration = event.get('duration', 1.0)
                    description = event.get('description', '')
                    if description:
                        print(f"⏰ Delay: {duration}s - {description}")
                    else:
                        print(f"⏰ Waiting {duration} seconds...")
                    
                    # Break the delay into smaller chunks to check for stop signal
                    wait_time = 0
                    while wait_time < duration and self.playing and not self.should_stop:
                        time.sleep(0.1)
                        wait_time += 0.1
                    
            except Exception as e:
                print(f"Error executing event: {e}")
                continue
        
        # Ensure all keys and buttons are released after sequence
        for key in pressed_keys:
            try:
                keyboard_controller.release(key)
            except:
                pass
        
        for button in pressed_buttons:
            try:
                mouse_controller.release(button)
            except:
                pass
    
    def string_to_key(self, key_string):
        """Convert string representation back to key object"""
        # Handle special keys
        special_keys = {
            'alt': Key.alt,
            'alt_l': Key.alt_l,
            'alt_r': Key.alt_r,
            'backspace': Key.backspace,
            'caps_lock': Key.caps_lock,
            'cmd': Key.cmd,
            'cmd_l': Key.cmd_l,
            'cmd_r': Key.cmd_r,
            'ctrl': Key.ctrl,
            'ctrl_l': Key.ctrl_l,
            'ctrl_r': Key.ctrl_r,
            'delete': Key.delete,
            'down': Key.down,
            'end': Key.end,
            'enter': Key.enter,
            'esc': Key.esc,
            'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3, 'f4': Key.f4,
            'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8,
            'f9': Key.f9, 'f10': Key.f10, 'f11': Key.f11, 'f12': Key.f12,
            'home': Key.home,
            'left': Key.left,
            'page_down': Key.page_down,
            'page_up': Key.page_up,
            'right': Key.right,
            'shift': Key.shift,
            'shift_l': Key.shift_l,
            'shift_r': Key.shift_r,
            'space': Key.space,
            'tab': Key.tab,
            'up': Key.up
        }
        
        if key_string in special_keys:
            return special_keys[key_string]
        else:
            # Regular character
            return key_string
    
    def stop_all(self):
        """Stop all recording and playback operations"""
        self.should_stop = True
        self.playing = False
        self.stop_recording()
    
    def save_macro(self, filename):
        """Save recorded events to a JSON file"""
        try:
            data = {
                'events': self.events,
                'created_at': datetime.now().isoformat(),
                'total_events': len(self.events),
                'duration': self.events[-1]['timestamp'] if self.events else 0
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Macro saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving macro: {e}")
            return False
    
    def load_macro(self, filename):
        """Load events from a JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.events = data.get('events', [])
            print(f"Macro loaded from {filename} - {len(self.events)} events")
            return True
        except Exception as e:
            print(f"Error loading macro: {e}")
            return False
    
    def get_macro_info(self):
        """Get information about the current macro"""
        if not self.events:
            return "No macro loaded"
        
        duration = self.events[-1]['timestamp'] if self.events else 0
        return f"{len(self.events)} events, {duration:.2f} seconds duration"
