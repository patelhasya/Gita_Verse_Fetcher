import customtkinter as ctk
import requests
import json
import sys
import os
from tkinter import messagebox

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GitaVerseApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🕉️ Bhagavad Gita - Divine Wisdom")
        self.window.geometry("1100x800")
        self.window.configure(fg_color="#0f0f23")
        self.window.minsize(900, 700)
        
        # Color palette
        self.colors = {
            'primary': '#ff6b35',
            'secondary': '#4ecdc4',
            'accent': '#ffd700',
            'bg_primary': '#0f0f23',
            'bg_secondary': '#1a1a2e',
            'bg_tertiary': '#16213e',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'text_muted': '#888888',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336'
        }
        
        self.setup_ui()
        self.center_window()
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self):
        # Main container
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create header section
        self.create_header(main_container)
        
        # Create input section
        self.create_input_section(main_container)
        
        # Create popular verses section
        self.create_popular_verses_section(main_container)
        
        # Create results section
        self.create_results_section(main_container)
        
        # Create footer
        self.create_footer(main_container)
        
    def create_header(self, parent):
        # Header with enhanced styling
        header_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_secondary'], 
                                   corner_radius=20, height=120)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Main title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🕉️ BHAGAVAD GITA", 
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(pady=(15, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="✨ Discover the Eternal Wisdom of Lord Krishna ✨",
            font=ctk.CTkFont(size=16, weight="normal"),
            text_color=self.colors['secondary']
        )
        subtitle_label.pack()
        
        # Decorative line
        line_frame = ctk.CTkFrame(header_frame, height=3, fg_color=self.colors['primary'])
        line_frame.pack(fill="x", padx=100, pady=(10, 0))
        
    def create_input_section(self, parent):
        # Input section
        input_card = ctk.CTkFrame(parent, fg_color=self.colors['bg_secondary'], 
                                 corner_radius=20, height=180)
        input_card.pack(fill="x", pady=(0, 20))
        input_card.pack_propagate(False)
        
        # Input label
        input_label = ctk.CTkLabel(
            input_card, 
            text="📚 Enter Verse Reference", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['text_primary']
        )
        input_label.pack(pady=(20, 5))
        
        # Format instruction
        format_label = ctk.CTkLabel(
            input_card, 
            text="Format: chapter.verse (e.g., 2.47) • Chapters 1-18 available", 
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_muted']
        )
        format_label.pack(pady=(0, 15))
        
        # Input container
        input_container = ctk.CTkFrame(input_card, fg_color="transparent")
        input_container.pack()
        
        # Input field
        self.verse_entry = ctk.CTkEntry(
            input_container,
            placeholder_text="Enter verse (e.g., 2.47)",
            width=250,
            height=45,
            font=ctk.CTkFont(size=20),
            justify="center",
            corner_radius=15,
            border_width=2,
            border_color=self.colors['secondary']
        )
        self.verse_entry.pack(side="left", padx=(0, 15))
        self.verse_entry.bind("<Return>", lambda e: self.fetch_verse())
        self.verse_entry.bind("<KeyPress>", self.on_key_press)
        
        # Fetch button
        self.fetch_button = ctk.CTkButton(
            input_container,
            text="🔍 FETCH VERSE",
            command=self.fetch_verse,
            width=180,
            height=45,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['success'],
            corner_radius=15,
            border_width=2,
            border_color=self.colors['accent']
        )
        self.fetch_button.pack(side="left")
        
    def create_popular_verses_section(self, parent):
        # Popular verses section
        popular_card = ctk.CTkFrame(parent, fg_color=self.colors['bg_secondary'], 
                                   corner_radius=20, height=120)
        popular_card.pack(fill="x", pady=(0, 20))
        popular_card.pack_propagate(False)
        
        # Header
        popular_header = ctk.CTkLabel(
            popular_card, 
            text="⭐ POPULAR VERSES", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['accent']
        )
        popular_header.pack(pady=(15, 10))
        
        # Buttons container
        buttons_container = ctk.CTkFrame(popular_card, fg_color="transparent")
        buttons_container.pack()
        
        # Popular verse buttons
        popular_verses = [
            ("2.47", "Karma Yoga", self.colors['primary']),
            ("18.66", "Surrender", self.colors['secondary']),
            ("9.26", "Devotion", self.colors['warning']),
            ("4.7", "Divine Incarnation", self.colors['success']),
            ("2.13", "Soul's Journey", "#9c27b0")
        ]
        
        for i, (verse, description, color) in enumerate(popular_verses):
            btn_frame = ctk.CTkFrame(buttons_container, fg_color="transparent")
            btn_frame.pack(side="left", padx=8)
            
            btn = ctk.CTkButton(
                btn_frame,
                text=f"{verse}\n{description}",
                command=lambda v=verse: self.set_and_fetch_verse(v),
                width=90,
                height=50,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=color,
                hover_color=self.colors['bg_tertiary'],
                corner_radius=12
            )
            btn.pack()
            
    def create_results_section(self, parent):
        # Results section
        results_container = ctk.CTkFrame(parent, fg_color="transparent")
        results_container.pack(fill="both", expand=True)
        
        # Verse reference display
        self.reference_frame = ctk.CTkFrame(results_container, fg_color=self.colors['bg_tertiary'], 
                                          corner_radius=15, height=60)
        self.reference_frame.pack(fill="x", pady=(0, 15))
        self.reference_frame.pack_propagate(False)
        
        self.reference_label = ctk.CTkLabel(
            self.reference_frame,
            text="Select a verse to begin your spiritual journey...",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['accent']
        )
        self.reference_label.pack(expand=True)
        
        # Content container with two columns
        content_frame = ctk.CTkFrame(results_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Left column - Sanskrit
        left_column = ctk.CTkFrame(content_frame, fg_color=self.colors['bg_secondary'], 
                                  corner_radius=15)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Sanskrit header - FIXED: Simple frame without complex corner_radius
        sanskrit_header = ctk.CTkFrame(left_column, fg_color=self.colors['secondary'], 
                                     height=45)
        sanskrit_header.pack(fill="x", padx=5, pady=(5, 0))
        sanskrit_header.pack_propagate(False)
        
        ctk.CTkLabel(
            sanskrit_header,
            text="📜 संस्कृत (Sanskrit)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['bg_primary']
        ).pack(expand=True)
        
        # Sanskrit content
        sanskrit_content_frame = ctk.CTkScrollableFrame(left_column, fg_color=self.colors['bg_primary'])
        sanskrit_content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.sanskrit_text = ctk.CTkLabel(
            sanskrit_content_frame,
            text="",
            font=ctk.CTkFont(size=26),
            text_color=self.colors['text_primary'],
            wraplength=450,
            justify="center"
        )
        self.sanskrit_text.pack(pady=20, padx=10)
        
        # Right column - English
        right_column = ctk.CTkFrame(content_frame, fg_color=self.colors['bg_secondary'], 
                                   corner_radius=15)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # English header - FIXED: Simple frame without complex corner_radius
        english_header = ctk.CTkFrame(right_column, fg_color=self.colors['primary'], 
                                    height=45)
        english_header.pack(fill="x", padx=5, pady=(5, 0))
        english_header.pack_propagate(False)
        
        ctk.CTkLabel(
            english_header,
            text="🌟 English Translation",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(expand=True)
        
        # English content
        english_content_frame = ctk.CTkScrollableFrame(right_column, fg_color=self.colors['bg_primary'])
        english_content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.english_text = ctk.CTkLabel(
            english_content_frame,
            text="",
            font=ctk.CTkFont(size=26, weight="normal"),
            text_color=self.colors['text_secondary'],
            wraplength=450,
            justify="left"
        )
        self.english_text.pack(pady=20, padx=10)
        
    def create_footer(self, parent):
        # Status footer
        footer_frame = ctk.CTkFrame(parent, fg_color=self.colors['bg_tertiary'], 
                                  corner_radius=15, height=50)
        footer_frame.pack(fill="x", pady=(15, 0))
        footer_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            footer_frame,
            text="🙏 Ready to explore the wisdom of the Gita...",
            font=ctk.CTkFont(size=13),
            text_color=self.colors['text_muted']
        )
        self.status_label.pack(expand=True)
        
    def on_key_press(self, event):
        # Visual feedback on typing
        self.verse_entry.configure(border_color=self.colors['accent'])
        self.window.after(2000, lambda: self.verse_entry.configure(border_color=self.colors['secondary']))
        
    def set_and_fetch_verse(self, verse):
        self.verse_entry.delete(0, "end")
        self.verse_entry.insert(0, verse)
        self.fetch_verse()
        
    def fetch_verse(self):
        verse_ref = self.verse_entry.get().strip()
        
        if not verse_ref:
            self.show_error("Please enter a verse reference")
            return
            
        if '.' not in verse_ref:
            self.show_error("Please use format: chapter.verse (e.g., 2.47)")
            return
            
        try:
            chapter_num, verse_num = map(int, verse_ref.split('.'))
            
            if chapter_num < 1 or chapter_num > 18:
                self.show_error("Chapter must be between 1-18")
                return
                
            self.update_status(f"🔍 Fetching sacred verse {chapter_num}.{verse_num}...")
            self.fetch_button.configure(state="disabled", text="⏳ LOADING...", 
                                       fg_color=self.colors['text_muted'])
            self.window.update()
            
            sanskrit, english = self.get_gita_verse(chapter_num, verse_num)
            
            if sanskrit and english:
                self.display_verse(chapter_num, verse_num, sanskrit, english)
                self.update_status("✨ Divine wisdom received! May it illuminate your path 🙏")
            else:
                self.show_error("Could not fetch the verse. Please try again.")
                
        except ValueError:
            self.show_error("Please enter valid numbers (e.g., 2.47)")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
        finally:
            self.fetch_button.configure(state="normal", text="🔍 FETCH VERSE", 
                                       fg_color=self.colors['primary'])
            
    def get_gita_verse(self, chapter, verse):
        try:
            url = f"https://bhagavad-gita3.p.rapidapi.com/v2/chapters/{chapter}/verses/{verse}/"
            
            headers = {
                'x-rapidapi-key': "c8df389391mshade9381c8a69b98p1def25jsne98b66085d6d",
                'x-rapidapi-host': "bhagavad-gita3.p.rapidapi.com"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                verse_data = response.json()
                
                sanskrit = verse_data.get('text', 'Sanskrit text not available')
                english = 'Translation not found'
                
                for translation in verse_data.get('translations', []):
                    if (isinstance(translation, dict) and 
                        translation.get('language') == 'english' and 
                        translation.get('description')):
                        english = translation['description']
                        break
                
                return sanskrit, english
            else:
                return None, None
                
        except Exception:
            return None, None
            
    def display_verse(self, chapter, verse, sanskrit, english):
        # Display with chapter names
        chapter_names = {
            1: "Arjuna's Dilemma", 2: "Sankhya Yoga", 3: "Karma Yoga", 4: "Jnana Yoga",
            5: "Renunciation of Action", 6: "Dhyana Yoga", 7: "Knowledge of the Absolute",
            8: "Attaining the Supreme", 9: "Royal Knowledge", 10: "Divine Manifestations",
            11: "Universal Form", 12: "Devotion", 13: "Nature & Enjoyer", 14: "Three Modes",
            15: "Supreme Person", 16: "Divine & Demonic", 17: "Three Types of Faith", 18: "Renunciation"
        }
        
        chapter_name = chapter_names.get(chapter, f"Chapter {chapter}")
        self.reference_label.configure(
            text=f"📖 Chapter {chapter}: {chapter_name} - Verse {verse}"
        )
        
        self.sanskrit_text.configure(text=sanskrit if sanskrit else "Sanskrit text not available")
        self.english_text.configure(text=english if english else "Translation not available")
        
    def update_status(self, message):
        self.status_label.configure(text=message)
        
    def show_error(self, message):
        self.update_status(f"⚠️ {message}")
        self.reference_label.configure(text="Please check your input and try again")
        self.sanskrit_text.configure(text="")
        self.english_text.configure(text="")
        
        # Show error popup
        messagebox.showerror("Input Error", message)
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = GitaVerseApp()
    app.run()