"""
GUI Styles and Theme Configuration for  Macro Recorder
"""
import customtkinter as ctk

class ThemeManager:
    """Manages the application theme and color schemes"""
    
    # Color scheme
    COLORS = {
        'primary': "#FF6B9D",
        'primary_hover': "#FF5582", 
        'secondary': "#4ECDC4",
        'secondary_hover': "#45B7AB",
        'accent': "#A8E6CF",
        'accent_hover': "#95D4B8",
        'warning': "#FFD93D",
        'danger': "#FF6B9D",
        'success': "#A8E6CF",
        'text_dark': "#2C3E50",
        'purple': "#6C63FF",
        'purple_hover': "#5A52E8",
        'orange': "#FF9500",
        'orange_hover': "#E6850E"
    }
    
    # Font configurations
    FONTS = {
        'title': ('Segoe UI', 28, 'bold'),
        'heading': ('Segoe UI', 18, 'bold'), 
        'subheading': ('Segoe UI', 14, 'bold'),
        'body': ('Segoe UI', 14, 'normal'),
        'small': ('Segoe UI', 12, 'normal'),
        'tiny': ('Segoe UI', 11, 'normal'),
        'code': ('Consolas', 11, 'normal')
    }
    
    @classmethod
    def setup_theme(cls):
        """Initialize CustomTkinter theme"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    @classmethod
    def get_font(cls, font_name, size=None, weight=None):
        """Get a configured font"""
        base_font = cls.FONTS.get(font_name, cls.FONTS['body'])
        family, base_size, base_weight = base_font
        
        return ctk.CTkFont(
            family=family,
            size=size or base_size,
            weight=weight or base_weight
        )
    
    @classmethod
    def get_button_style(cls, style_type):
        """Get predefined button styles"""
        styles = {
            'record': {
                'fg_color': cls.COLORS['primary'],
                'hover_color': cls.COLORS['primary_hover'],
                'font': cls.get_font('body', weight='bold'),
                'corner_radius': 20,
                'width': 150,
                'height': 40
            },
            'play': {
                'fg_color': cls.COLORS['secondary'],
                'hover_color': cls.COLORS['secondary_hover'],
                'font': cls.get_font('body', weight='bold'),
                'corner_radius': 20,
                'width': 150,
                'height': 40
            },
            'stop': {
                'fg_color': cls.COLORS['accent'],
                'hover_color': cls.COLORS['accent_hover'],
                'text_color': cls.COLORS['text_dark'],
                'font': cls.get_font('body', weight='bold'),
                'corner_radius': 20,
                'width': 150,
                'height': 40
            },
            'file': {
                'fg_color': cls.COLORS['purple'],
                'hover_color': cls.COLORS['purple_hover'],
                'font': cls.get_font('small'),
                'corner_radius': 15,
                'width': 140,
                'height': 35
            },
            'apply': {
                'fg_color': cls.COLORS['orange'],
                'hover_color': cls.COLORS['orange_hover'],
                'font': cls.get_font('tiny'),
                'corner_radius': 15,
                'width': 120,
                'height': 30
            }
        }
        return styles.get(style_type, {})

class StyleHelper:
    """Helper class for consistent styling across the application"""
    
    @staticmethod
    def create_frame(parent, corner_radius=10, fg_color=None, **kwargs):
        """Create a consistently styled frame"""
        return ctk.CTkFrame(
            parent,
            corner_radius=corner_radius,
            fg_color=fg_color,
            **kwargs
        )
    
    @staticmethod
    def create_label(parent, text, style='body', color=None, **kwargs):
        """Create a consistently styled label"""
        font = ThemeManager.get_font(style)
        return ctk.CTkLabel(
            parent,
            text=text,
            font=font,
            text_color=color,
            **kwargs
        )
    
    @staticmethod
    def create_entry(parent, placeholder=None, width=200, height=35, **kwargs):
        """Create a consistently styled entry"""
        entry_kwargs = {
            'placeholder_text': placeholder,
            'height': height,
            'font': ThemeManager.get_font('body'),
            **kwargs
        }
        
        # Only add width if it's not None
        if width is not None:
            entry_kwargs['width'] = width
            
        return ctk.CTkEntry(parent, **entry_kwargs)
    
    @staticmethod
    def create_button(parent, text, style_type, command=None, **kwargs):
        """Create a consistently styled button"""
        style = ThemeManager.get_button_style(style_type)
        style.update(kwargs)  # Allow override of style properties
        
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            **style
        )
    
    @staticmethod
    def create_checkbox(parent, text, variable=None, **kwargs):
        """Create a consistently styled checkbox"""
        return ctk.CTkCheckBox(
            parent,
            text=text,
            variable=variable,
            font=ThemeManager.get_font('body'),
            checkbox_width=20,
            checkbox_height=20,
            **kwargs
        )
    
    @staticmethod
    def create_textbox(parent, **kwargs):
        """Create a consistently styled textbox"""
        return ctk.CTkTextbox(
            parent,
            font=ThemeManager.get_font('code'),
            wrap="word",
            **kwargs
        )
