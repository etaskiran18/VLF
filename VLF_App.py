#!/usr/bin/env python3
"""
VLF Research Mobile App
A comprehensive educational and research app for VLF electromagnetic waves,
lightning-generated EM waves, and space physics.
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
import requests
import json
import math
from datetime import datetime
import threading
import xml.etree.ElementTree as ET
import webbrowser

kivy.require('2.0.0')

# Text alternatives that display properly across all systems:
SYMBOLS = {
    # Lightning/Electric
    'lightning': '[⚡]',
    'lightning_alt': '[BOLT]',
    'electric': '~~~',
    
    # Space/Science
    'space': '[★]',
    'earth': '[EARTH]',
    'satellite': '[SAT]',
    'wave': '[WAVE]',
    
    # Academic/Research
    'research': '[RESEARCH]',
    'theory': '[THEORY]',
    'formula': '[CALC]',
    'data': '[DATA]',
    
    # Navigation
    'back': '<-',
    'forward': '->',
    'up': '^',
    'down': 'v',
    
    # Web/Links
    'link': '[LINK]',
    'globe': '[WEB]',
    'external': '->',
}

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        
        # Main layout with dark space background
        layout = BoxLayout(orientation='vertical', spacing=20, padding=25)
        
        # Add space background (fixed - removed LinearGradient import)
        with layout.canvas.before:
            Color(0.05, 0.05, 0.15, 1)  # Deep space blue
            layout.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self.update_bg, pos=self.update_bg)
        
        # Header with university collaboration and lab URL
        header_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None, height='170dp')
        
        # University logos layout with modern styling
        logos_layout = BoxLayout(orientation='horizontal', spacing=30, size_hint_y=None, height='100dp')
        
        # Koç University logo container with modern styling
        koc_container = BoxLayout(orientation='vertical', padding=10)
        with koc_container.canvas.before:
            # Glassmorphism effect
            Color(0.15, 0.25, 0.45, 0.3)  # Semi-transparent blue
            koc_container.bg_rect = RoundedRectangle(size=koc_container.size, pos=koc_container.pos, radius=[15,])
            # Electric border effect
            Color(0.3, 0.7, 1, 0.8)  # Electric blue border
            koc_container.border_line = Line(rounded_rectangle=(koc_container.x, koc_container.y, koc_container.width, koc_container.height, 15), width=2)
            koc_container.bind(size=self.update_logo_rect, pos=self.update_logo_rect)
        
        # Try to load actual logo image, fallback to styled text
        try:
            koc_logo = Image(source='koc_logo.png', size_hint=(1, 0.8), allow_stretch=True, keep_ratio=True)
            koc_container.add_widget(koc_logo)
        except:
            # Fallback to modern text design with better sizing
            koc_logo = Label(
                text='KOC UNIVERSITY\n\nVLF Research Lab',
                font_size='13sp',
                bold=True,
                color=(0.9, 0.95, 1, 1),
                halign='center',
                valign='center'
            )
            # Set text_size to enable proper text wrapping
            def update_text_size(instance, size):
                instance.text_size = (size[0] - 10, size[1] - 10)
            koc_logo.bind(size=update_text_size)
            koc_container.add_widget(koc_logo)
        
        logos_layout.add_widget(koc_container)
        
        # Lightning collaboration symbol
        collab_container = BoxLayout(orientation='vertical', size_hint_x=0.25)
        collab_symbol = Label(
            text='[BOLT]\n<->\nCOLLAB',
            font_size='12sp',
            color=(1, 1, 0.3, 1),  # Electric yellow
            halign='center',
            bold=True
        )
        collab_container.add_widget(collab_symbol)
        logos_layout.add_widget(collab_container)
        
        # Stanford VLF logo container with modern styling
        stanford_container = BoxLayout(orientation='vertical', padding=10)
        with stanford_container.canvas.before:
            Color(0.45, 0.15, 0.25, 0.3)  # Semi-transparent red
            stanford_container.bg_rect = RoundedRectangle(size=stanford_container.size, pos=stanford_container.pos, radius=[15,])
            # Electric border effect
            Color(1, 0.3, 0.5, 0.8)  # Electric pink border
            stanford_container.border_line = Line(rounded_rectangle=(stanford_container.x, stanford_container.y, stanford_container.width, stanford_container.height, 15), width=2)
            stanford_container.bind(size=self.update_logo_rect, pos=self.update_logo_rect)
        
        # Try to load actual logo image, fallback to styled text
        try:
            stanford_logo = Image(source='stanford_logo.png', size_hint=(1, 0.8), allow_stretch=True, keep_ratio=True)
            stanford_container.add_widget(stanford_logo)
        except:
            # Fallback to modern text design with better sizing
            stanford_logo = Label(
                text='STANFORD VLF\n\nGroup Partnership',
                font_size='13sp',
                bold=True,
                color=(1, 0.9, 0.95, 1),
                halign='center',
                valign='center'
            )
            # Set text_size to enable proper text wrapping
            def update_text_size(instance, size):
                instance.text_size = (size[0] - 10, size[1] - 10)
            stanford_logo.bind(size=update_text_size)
            stanford_container.add_widget(stanford_logo)
        
        logos_layout.add_widget(stanford_container)
        header_layout.add_widget(logos_layout)
        
        # Lab website link with modern button design
        lab_link_btn = Button(
            text='[WEB] Visit VLF Research Lab Website: vlfstanford.ku.edu.tr',
            font_size='14sp',
            size_hint_y=None,
            height='35dp',
            background_color=(0.1, 0.4, 0.8, 0.8),
            on_press=self.open_lab_website
        )
        # Add modern button styling
        with lab_link_btn.canvas.before:
            Color(0.2, 0.6, 1, 0.3)
            lab_link_btn.bg_rect = RoundedRectangle(size=lab_link_btn.size, pos=lab_link_btn.pos, radius=[10,])
            lab_link_btn.bind(size=self.update_button_bg, pos=self.update_button_bg)
        
        header_layout.add_widget(lab_link_btn)
        
        # Main title with space theme
        title_container = BoxLayout(orientation='vertical', size_hint_y=None, height='80dp')
        with title_container.canvas.before:
            Color(0.1, 0.1, 0.2, 0.5)
            title_container.bg_rect = RoundedRectangle(size=title_container.size, pos=title_container.pos, radius=[20,])
            title_container.bind(size=self.update_title_bg, pos=self.update_title_bg)
        
        title = Label(
            text='[BOLT] VLF RESEARCH HUB [BOLT]\nElectromagnetic Wave Propagation & Plasma Physics',
            font_size='24sp',
            bold=True,
            color=(0.9, 1, 1, 1),
            halign='center',
            markup=True
        )
        title_container.add_widget(title)
        header_layout.add_widget(title_container)
        
        layout.add_widget(header_layout)
        
        # Modern navigation menu with space theme
        menu_container = BoxLayout(orientation='vertical', spacing=15)
        menu_grid = GridLayout(cols=2, spacing=20, size_hint_y=1)
        
        # EM Theory button with lightning theme
        theory_btn = self.create_modern_button(
            '[BOLT] EM THEORY\n\nMaxwell\'s Equations\nVLF Fundamentals\nEarth-Ionosphere Waveguide',
            (0.1, 0.3, 0.7, 0.9),  # Deep blue
            (0.2, 0.5, 1, 0.4),    # Light blue glow
            self.go_to_theory
        )
        menu_grid.add_widget(theory_btn)
        
        # News button with cosmic theme
        news_btn = self.create_modern_button(
            '[STAR] VLF NEWS\n\nSpace Physics News\narXiv Papers\nPhysics Updates',
            (0.6, 0.2, 0.4, 0.9),  # Deep purple
            (1, 0.4, 0.6, 0.4),    # Pink glow
            self.go_to_news
        )
        menu_grid.add_widget(news_btn)
        
        # Calculators button with electric theme
        calc_btn = self.create_modern_button(
            '[CALC] CALCULATORS\n\nFrequency Conversion\nPropagation Distance\nWaveguide Parameters',
            (0.1, 0.6, 0.3, 0.9),  # Deep green
            (0.3, 1, 0.5, 0.4),    # Green glow
            self.go_to_calculators
        )
        menu_grid.add_widget(calc_btn)
        
        # Papers button with academic theme
        papers_btn = self.create_modern_button(
            '[RESEARCH] RESEARCH PAPERS\n\nVLF Studies\nSpace Physics\nElectromagnetic Research',
            (0.7, 0.4, 0.1, 0.9),  # Deep orange
            (1, 0.7, 0.2, 0.4),    # Orange glow
            self.go_to_papers
        )
        menu_grid.add_widget(papers_btn)
        
        # Plasma Physics button with aurora theme
        plasma_btn = self.create_modern_button(
            '[WAVE] PLASMA PHYSICS\n\nMagnetospheric Waves\nSpace Weather\nWave-Particle Interactions',
            (0.4, 0.1, 0.6, 0.9),  # Deep magenta
            (0.8, 0.3, 1, 0.4),    # Magenta glow
            self.go_to_plasma
        )
        menu_grid.add_widget(plasma_btn)
        
        # Space Weather button with atmospheric theme
        weather_btn = self.create_modern_button(
            '[EARTH] SPACE WEATHER\n\nSolar Activity\nGeomagnetic Conditions\nIonospheric Effects',
            (0.1, 0.5, 0.5, 0.9),  # Deep teal
            (0.2, 0.8, 0.8, 0.4),  # Cyan glow
            self.go_to_space_weather
        )
        menu_grid.add_widget(weather_btn)
        
        menu_container.add_widget(menu_grid)
        layout.add_widget(menu_container)
        
        # Modern footer with space theme
        footer_container = BoxLayout(orientation='vertical', size_hint_y=None, height='40dp')
        with footer_container.canvas.before:
            Color(0.05, 0.05, 0.1, 0.7)
            footer_container.bg_rect = RoundedRectangle(size=footer_container.size, pos=footer_container.pos, radius=[15,])
            footer_container.bind(size=self.update_footer_bg, pos=self.update_footer_bg)
        
        footer = Label(
            text='[BOLT] Advanced VLF Research Platform • Koç University & Stanford VLF Group [BOLT]',
            font_size='14sp',
            color=(0.7, 0.8, 1, 1),
            halign='center'
        )
        footer_container.add_widget(footer)
        layout.add_widget(footer_container)
        
        self.add_widget(layout)
    
    def create_modern_button(self, text, bg_color, glow_color, callback):
        """Create a modern button with glassmorphism and glow effects"""
        btn_container = BoxLayout()
        
        btn = Button(
            text=text,
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            background_color=(0, 0, 0, 0),  # Transparent background
            on_press=callback
        )
        
        # Add modern styling with canvas
        with btn.canvas.before:
            # Main background with glassmorphism
            Color(*bg_color)
            btn.bg_rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[20,])
            # Glow effect
            Color(*glow_color)
            btn.glow_rect = RoundedRectangle(size=(btn.width + 10, btn.height + 10), 
                                          pos=(btn.x - 5, btn.y - 5), radius=[25,])
            # Electric border
            Color(1, 1, 1, 0.3)
            btn.border_line = Line(rounded_rectangle=(btn.x, btn.y, btn.width, btn.height, 20), width=1)
            
            btn.bind(size=self.update_button_style, pos=self.update_button_style)
        
        btn_container.add_widget(btn)
        return btn_container
    
    def update_bg(self, instance, value):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size
    
    def update_logo_rect(self, instance, value):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size
        # Update border
        instance.border_line.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, 15)
    
    def update_button_bg(self, instance, value):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size
    
    def update_title_bg(self, instance, value):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size
    
    def update_footer_bg(self, instance, value):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size
    
    def update_button_style(self, instance, value):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size
        instance.glow_rect.pos = (instance.x - 5, instance.y - 5)
        instance.glow_rect.size = (instance.width + 10, instance.height + 10)
        instance.border_line.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, 20)
    
    def open_lab_website(self, instance):
        """Open the lab website"""
        try:
            webbrowser.open('https://vlfstanford.ku.edu.tr/')
        except Exception as e:
            print(f'Could not open website: {e}')
    
    def go_to_theory(self, instance):
        self.manager.current = 'theory'
    
    def go_to_news(self, instance):
        self.manager.current = 'news'
    
    def go_to_calculators(self, instance):
        self.manager.current = 'calculators'
    
    def go_to_papers(self, instance):
        self.manager.current = 'papers'
    
    def go_to_plasma(self, instance):
        self.manager.current = 'plasma'
    
    def go_to_space_weather(self, instance):
        self.manager.current = 'weather'

class TheoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'theory'
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header with back button
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        back_btn = Button(text='← Back', size_hint_x=0.2, background_color=(0.8, 0.3, 0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header_layout.add_widget(back_btn)
        header_layout.add_widget(Label(text='Electromagnetic Theory', font_size='20sp', bold=True))
        layout.add_widget(header_layout)
        
        # Scrollable content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Theory sections with comprehensive content
        sections = [
            {
                'title': 'Maxwell\'s Equations and VLF Fundamentals',
                'content': '''
MAXWELL'S EQUATIONS IN VLF CONTEXT:

Differential Form:
• ∇ × E = -∂B/∂t (Faraday's Law)
• ∇ × H = J + ∂D/∂t (Ampère-Maxwell Law)
• ∇ · D = ρ (Gauss's Law)
• ∇ · B = 0 (No magnetic monopoles)

VLF Wave Properties:
• Frequency range: 3-30 kHz
• Wavelengths: λ = c/f = 10-100 km
• Period: T = 1/f = 33-333 μs
• Wave number: k = 2π/λ = ω/c
• Phase velocity: vₚ = ω/k ≈ c (in vacuum)

Free Space Wave Equation:
∇²E - μ₀ε₀ ∂²E/∂t² = 0
∇²B - μ₀ε₀ ∂²B/∂t² = 0

Where c = 1/√(μ₀ε₀) = 299,792,458 m/s
                '''
            },
            {
                'title': 'Lightning as a VLF Source',
                'content': '''
LIGHTNING PHYSICS:

Lightning Formation:
• Charge separation in thunderclouds
• Electric field buildup: ~100-300 kV/m
• Critical breakdown: ~3 MV/m in air
• Stepped leader formation
• Return stroke initiation

Lightning Current Characteristics:
• Peak current: Iₚ = 10-200 kA (typical: 30 kA)
• Rise time: τᵣ = 1-10 μs (typical: 2-5 μs)
• Pulse duration: τ = 50-500 μs
• Total charge: Q = 1-300 C
• Channel temperature: ~30,000 K

VLF Generation Mechanism:
• Vertical lightning channel acts as dipole antenna
• Length l ≪ λ (short dipole approximation)
• Broadband spectrum: DC to several MHz
• Peak energy: 1-10 kHz range
                '''
            },
            {
                'title': 'Earth-Ionosphere Waveguide',
                'content': '''
WAVEGUIDE STRUCTURE:

Physical Boundaries:
• Lower boundary: Earth surface (σ ≈ 10⁻² S/m)
• Upper boundary: D-layer ionosphere (h ≈ 60-90 km)
• Waveguide height: h = 85 km (typical)
• Earth radius: a = 6371 km

D-Layer Properties:
• Altitude: 60-90 km (day), 85-95 km (night)
• Electron density: Nₑ = 10²-10⁴ cm⁻³
• Collision frequency: νₑᵢ = 10⁶-10⁷ s⁻¹

WAVEGUIDE MODES:

TM Mode Equations:
• Mode designation: TMₘₙ
• Principal mode (TM₀₁): least attenuation
• Cutoff frequency: fₒ ≈ c/(2.4h) ≈ 1.8 kHz
• Phase velocity: vₚ = c/√(1-(fₒ/f)²)
• Group velocity: vₘ = c√(1-(fₒ/f)²)

Propagation Characteristics:
• Day: Higher D-layer ionization → more absorption
• Night: Lower D-layer → less attenuation
• Attenuation: α ≈ 2-3 dB/Mm (day), 1-2 dB/Mm (night)
                '''
            }
        ]
        
        for section in sections:
            # Section header
            header = Label(
                text=section['title'],
                font_size='16sp',
                bold=True,
                size_hint_y=None,
                height='40dp',
                color=(0.2, 0.6, 1, 1)
            )
            content.add_widget(header)
            
            # Section content
            text_label = Label(
                text=section['content'],
                text_size=(None, None),
                size_hint_y=None,
                halign='left',
                valign='top',
                font_size='14sp'
            )
            text_label.bind(texture_size=text_label.setter('size'))
            content.add_widget(text_label)
            
            # Spacing
            content.add_widget(Label(size_hint_y=None, height='20dp'))
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)

class NewsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'news'
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        back_btn = Button(text='← Back', size_hint_x=0.2, background_color=(0.8, 0.3, 0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header_layout.add_widget(back_btn)
        header_layout.add_widget(Label(text='VLF & Space Physics News', font_size='18sp', bold=True))
        layout.add_widget(header_layout)
        
        # API source buttons
        api_buttons = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        
        spaceflight_btn = Button(text='Space News', background_color=(0.3, 0.7, 1, 1))
        spaceflight_btn.bind(on_press=lambda x: self.fetch_spaceflight_news())
        
        arxiv_btn = Button(text='arXiv Papers', background_color=(0.7, 0.3, 1, 1))
        arxiv_btn.bind(on_press=lambda x: self.fetch_arxiv_papers())
        
        physics_btn = Button(text='Physics News', background_color=(0.3, 1, 0.7, 1))
        physics_btn.bind(on_press=lambda x: self.fetch_physics_news())
        
        api_buttons.add_widget(spaceflight_btn)
        api_buttons.add_widget(arxiv_btn)
        api_buttons.add_widget(physics_btn)
        layout.add_widget(api_buttons)
        
        # Status label
        self.status_label = Label(
            text='Click a button above to fetch latest news',
            size_hint_y=0.08,
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(self.status_label)
        
        # News content
        self.news_scroll = ScrollView()
        self.news_content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.news_content.bind(minimum_height=self.news_content.setter('height'))
        
        # Load initial content
        self.load_sample_news()
        
        self.news_scroll.add_widget(self.news_content)
        layout.add_widget(self.news_scroll)
        self.add_widget(layout)
    
    def clear_news(self):
        """Clear current news content"""
        self.news_content.clear_widgets()
    
    def update_status(self, message):
        """Update the status label"""
        self.status_label.text = message
    
    def fetch_spaceflight_news(self):
        """Fetch space news from Spaceflight News API"""
        self.update_status('Fetching spaceflight news...')
        threading.Thread(target=self._fetch_spaceflight_news_thread, daemon=True).start()
    
    def _fetch_spaceflight_news_thread(self):
        try:
            url = "https://api.spaceflightnewsapi.net/v4/articles"
            params = {
                'limit': 10,
                'search': 'space physics plasma magnetic'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('results', [])
                Clock.schedule_once(lambda dt: self._update_spaceflight_news(articles))
            else:
                Clock.schedule_once(lambda dt: self.update_status(f'Error: HTTP {response.status_code}'))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f'Error fetching news: {str(e)}'))
    
    def _update_spaceflight_news(self, articles):
        """Update UI with spaceflight news"""
        self.clear_news()
        self.update_status(f'Loaded {len(articles)} spaceflight articles')
        
        for article in articles:
            news_item = {
                'title': article.get('title', 'No title'),
                'date': article.get('published_at', '')[:10],
                'content': article.get('summary', 'No summary available'),
                'source': article.get('news_site', 'Spaceflight News'),
                'url': article.get('url', '')
            }
            if news_item['url']:
                self.add_news_item(news_item)
    
    def fetch_arxiv_papers(self):
        """Fetch latest VLF and space physics papers from arXiv"""
        self.update_status('Fetching arXiv papers...')
        self.clear_news()
        threading.Thread(target=self._fetch_arxiv_papers_thread, daemon=True).start()
    
    def _fetch_arxiv_papers_thread(self):
        """Thread function to fetch arXiv papers"""
        try:
            import urllib.request
            import urllib.parse
            
            search_queries = [
                'VLF electromagnetic waves',
                'very low frequency radio',
                'earth ionosphere waveguide',
                'whistler waves',
                'magnetospheric waves'
            ]
            
            all_papers = []
            
            for query in search_queries:
                encoded_query = urllib.parse.quote(query)
                url = f'http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending'
                
                try:
                    with urllib.request.urlopen(url, timeout=10) as response:
                        xml_data = response.read().decode('utf-8')
                    
                    # Parse XML
                    root = ET.fromstring(xml_data)
                    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
                    
                    entries = root.findall('atom:entry', namespace)
                    
                    for entry in entries:
                        title_elem = entry.find('atom:title', namespace)
                        title = title_elem.text.strip() if title_elem is not None else 'No title'
                        
                        id_elem = entry.find('atom:id', namespace)
                        arxiv_url = id_elem.text if id_elem is not None else ''
                        
                        if 'arxiv.org/abs/' in arxiv_url:
                            arxiv_id = arxiv_url.split('/')[-1]
                            clean_url = f'https://arxiv.org/abs/{arxiv_id}'
                        else:
                            clean_url = arxiv_url
                        
                        published_elem = entry.find('atom:published', namespace)
                        published = published_elem.text[:10] if published_elem is not None else '2025-05-25'
                        
                        summary_elem = entry.find('atom:summary', namespace)
                        summary = summary_elem.text.strip() if summary_elem is not None else 'No abstract available'
                        
                        authors = []
                        for author in entry.findall('atom:author', namespace):
                            name_elem = author.find('atom:name', namespace)
                            if name_elem is not None:
                                authors.append(name_elem.text)
                        
                        author_text = ', '.join(authors[:3])
                        if len(authors) > 3:
                            author_text += ' et al.'
                        
                        paper = {
                            'title': title,
                            'date': published,
                            'content': f'Authors: {author_text}\n\nAbstract: {summary[:200]}...',
                            'source': 'arXiv',
                            'url': clean_url
                        }
                        all_papers.append(paper)
                        
                except Exception as e:
                    print(f'Error fetching from arXiv for query "{query}": {e}')
                    continue
            
            # Remove duplicates and sort by date
            unique_papers = []
            seen_titles = set()
            for paper in all_papers:
                if paper['title'] not in seen_titles:
                    unique_papers.append(paper)
                    seen_titles.add(paper['title'])
            
            unique_papers.sort(key=lambda x: x['date'], reverse=True)
            final_papers = unique_papers[:10]
            
            Clock.schedule_once(lambda dt: self._update_arxiv_papers(final_papers))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f'Error fetching arXiv papers: {str(e)}'))
    
    def _update_arxiv_papers(self, papers):
        """Update UI with arXiv papers"""
        if papers:
            for paper in papers:
                self.add_news_item(paper)
            self.update_status(f'Loaded {len(papers)} arXiv papers')
        else:
            self.update_status('No arXiv papers found')
    
    def fetch_physics_news(self):
        """Fetch general physics news"""
        self.update_status('Fetching physics news...')
        threading.Thread(target=self._fetch_physics_news_thread, daemon=True).start()
    
    def _fetch_physics_news_thread(self):
        try:
            sample_physics_news = [
                {
                    'title': 'New Discoveries in Electromagnetic Wave Propagation',
                    'date': '2025-05-24',
                    'content': 'Recent research reveals novel mechanisms in VLF wave propagation through the Earth-ionosphere waveguide.',
                    'source': 'Physics Today',
                    'url': 'https://physicstoday.scitation.org/'
                },
                {
                    'title': 'Lightning-Generated Radio Waves Studied with AI',
                    'date': '2025-05-23',
                    'content': 'Machine learning algorithms help scientists better understand the electromagnetic signatures of lightning strikes.',
                    'source': 'Nature Physics',
                    'url': 'https://www.nature.com/nphys/'
                },
                {
                    'title': 'Space Weather Impact on VLF Communications',
                    'date': '2025-05-22',
                    'content': 'Solar activity affects Very Low Frequency radio propagation, impacting global navigation systems.',
                    'source': 'Geophysical Research Letters',
                    'url': 'https://agupubs.onlinelibrary.wiley.com/journal/19448007'
                }
            ]
            
            Clock.schedule_once(lambda dt: self._update_physics_news(sample_physics_news))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f'Error fetching physics news: {str(e)}'))
    
    def _update_physics_news(self, articles):
        """Update UI with physics news"""
        self.clear_news()
        self.update_status(f'Loaded {len(articles)} physics articles')
        
        for article in articles:
            self.add_news_item(article)
    
    def load_sample_news(self):
        """Load sample news items as fallback"""
        news_items = [
            {
                'title': 'Welcome to VLF Research News Hub',
                'date': '2025-05-24',
                'content': 'Click the buttons above to fetch the latest news from Spaceflight News API, arXiv research papers, or general physics news. The app will fetch real-time data from these sources and open articles directly in your browser.',
                'source': 'VLF Research Hub',
                'url': 'https://vlfstanford.ku.edu.tr/'
            },
            {
                'title': 'API Integration Features',
                'date': '2025-05-24',
                'content': 'This app integrates with: • Spaceflight News API for space-related news • arXiv API for latest research papers • Physics news from various sources. Click any article to open it in your web browser.',
                'source': 'App Info',
                'url': 'https://arxiv.org/list/physics.space-ph/recent'
            }
        ]
        
        for item in news_items:
            self.add_news_item(item)
    
    def add_news_item(self, item):
        # News item container with fixed height
        item_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height='160dp')
        
        # Main container with background and click handling
        main_container = BoxLayout(orientation='vertical', spacing=5, padding=[10, 8, 10, 8])
        
        # Title
        title = Label(
            text=item['title'],
            font_size='15sp',
            bold=True,
            size_hint_y=None,
            height='45dp',
            color=(0.3, 0.7, 1, 1),
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        main_container.add_widget(title)
        
        # Date and source
        meta_text = f"[DATE] {item['date']} • [NEWS] {item['source']}"
        meta = Label(
            text=meta_text,
            font_size='12sp',
            size_hint_y=None,
            height='20dp',
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        main_container.add_widget(meta)
        
        # Content preview
        preview_text = item['content']
        if len(preview_text) > 100:
            preview_text = preview_text[:100] + '...'
        
        content = Label(
            text=preview_text,
            font_size='13sp',
            size_hint_y=None,
            height='50dp',
            color=(0.9, 0.9, 0.9, 1),
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        main_container.add_widget(content)
        
        # Click button
        click_btn = Button(
            text='[LINK] Open Article',
            font_size='12sp',
            size_hint_y=None,
            height='25dp',
            background_color=(0.2, 0.5, 0.8, 1),
            on_press=lambda x: self.open_article_detail(item)
        )
        main_container.add_widget(click_btn)
        
        # Add background color
        with main_container.canvas.before:
            Color(0.15, 0.15, 0.25, 0.8)
            main_container.rect = RoundedRectangle(size=main_container.size, pos=main_container.pos, radius=[5,])
            main_container.bind(size=self.update_rect, pos=self.update_rect)
        
        # Update text sizes when container size changes
        def update_text_sizes(instance, size):
            title.text_size = (size[0] - 20, None)
            meta.text_size = (size[0] - 20, None)
            content.text_size = (size[0] - 20, None)
        
        main_container.bind(size=update_text_sizes)
        
        item_layout.add_widget(main_container)
        self.news_content.add_widget(item_layout)
    
    def update_rect(self, instance, value):
        """Update rectangle size and position"""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def open_article_detail(self, item):
        """Open article in web browser"""
        url = item.get('url', '')
        
        if url:
            try:
                webbrowser.open(url)
                self.update_status(f'Opening article in browser: {item["title"][:50]}...')
            except Exception as e:
                self.update_status(f'Could not open browser: {str(e)}')
        else:
            self.update_status('No direct URL available for this article')

class CalculatorsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'calculators'
        
        # Main layout with padding
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        # Header with back button
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing=10)
        
        # Back button
        back_btn = Button(
            text='← Back to Main',
            font_size='16sp',
            size_hint_x=0.3,
            background_color=(0.3, 0.3, 0.6, 1),
            on_press=self.go_back
        )
        header_layout.add_widget(back_btn)
        
        # Title
        title = Label(
            text='VLF Research Calculators',
            font_size='24sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign='center'
        )
        header_layout.add_widget(title)
        
        # Lab website button
        lab_btn = Button(
            text='[WEB] Lab Website',
            font_size='14sp',
            size_hint_x=0.25,
            background_color=(0.2, 0.6, 0.8, 1),
            on_press=self.open_lab_website
        )
        header_layout.add_widget(lab_btn)
        
        main_layout.add_widget(header_layout)
        
        # Calculators scroll view
        scroll = ScrollView()
        calc_layout = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None, padding=[0, 10])
        calc_layout.bind(minimum_height=calc_layout.setter('height'))
        
        # Calculator 1: Frequency/Wavelength Converter
        calc1_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height='200dp', padding=10)
        with calc1_container.canvas.before:
            Color(0.2, 0.3, 0.5, 0.8)
            calc1_container.rect = RoundedRectangle(size=calc1_container.size, pos=calc1_container.pos, radius=[10,])
            calc1_container.bind(size=self.update_calc_rect, pos=self.update_calc_rect)
        
        calc1_title = Label(
            text='[RADIO] Frequency ↔ Wavelength Converter',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height='30dp',
            color=(0.9, 0.9, 1, 1)
        )
        calc1_container.add_widget(calc1_title)
        
        calc1_content = BoxLayout(orientation='vertical', spacing=5)
        
        # Input row
        input_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')
        
        freq_label = Label(text='Frequency:', size_hint_x=0.25, font_size='14sp')
        input_row.add_widget(freq_label)
        
        self.freq_input = TextInput(
            hint_text='Enter frequency (Hz)',
            multiline=False,
            size_hint_x=0.5,
            font_size='14sp'
        )
        input_row.add_widget(self.freq_input)
        
        convert_btn = Button(
            text='Convert',
            size_hint_x=0.25,
            background_color=(0.2, 0.6, 0.8, 1),
            font_size='14sp',
            on_press=self.convert_frequency
        )
        input_row.add_widget(convert_btn)
        
        calc1_content.add_widget(input_row)
        
        # Result
        self.wavelength_result = Label(
            text='Wavelength: --',
            font_size='16sp',
            color=(0.8, 1, 0.8, 1),
            size_hint_y=None,
            height='30dp'
        )
        calc1_content.add_widget(self.wavelength_result)
        
        # Info
        info1 = Label(
            text='VLF range: 3-30 kHz (100-10 km wavelength)',
            font_size='12sp',
            color=(0.7, 0.7, 0.8, 1),
            size_hint_y=None,
            height='25dp'
        )
        calc1_content.add_widget(info1)
        
        calc1_container.add_widget(calc1_content)
        calc_layout.add_widget(calc1_container)
        
        # Calculator 2: Great Circle Distance
        calc2_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height='280dp', padding=10)
        with calc2_container.canvas.before:
            Color(0.3, 0.5, 0.2, 0.8)
            calc2_container.rect = RoundedRectangle(size=calc2_container.size, pos=calc2_container.pos, radius=[10,])
            calc2_container.bind(size=self.update_calc_rect, pos=self.update_calc_rect)
        
        calc2_title = Label(
            text='[EARTH] Great Circle Distance Calculator',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height='30dp',
            color=(0.9, 1, 0.9, 1)
        )
        calc2_container.add_widget(calc2_title)
        
        calc2_content = BoxLayout(orientation='vertical', spacing=5)
        
        # Start coordinates
        start_row = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height='35dp')
        start_row.add_widget(Label(text='Start:', size_hint_x=0.15, font_size='12sp'))
        start_row.add_widget(Label(text='Lat:', size_hint_x=0.1, font_size='12sp'))
        self.start_lat = TextInput(hint_text='41.0', multiline=False, size_hint_x=0.3, font_size='12sp')
        start_row.add_widget(self.start_lat)
        start_row.add_widget(Label(text='Lon:', size_hint_x=0.1, font_size='12sp'))
        self.start_lon = TextInput(hint_text='29.0', multiline=False, size_hint_x=0.3, font_size='12sp')
        start_row.add_widget(self.start_lon)
        calc2_content.add_widget(start_row)
        
        # End coordinates
        end_row = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height='35dp')
        end_row.add_widget(Label(text='End:', size_hint_x=0.15, font_size='12sp'))
        end_row.add_widget(Label(text='Lat:', size_hint_x=0.1, font_size='12sp'))
        self.end_lat = TextInput(hint_text='37.4', multiline=False, size_hint_x=0.3, font_size='12sp')
        end_row.add_widget(self.end_lat)
        end_row.add_widget(Label(text='Lon:', size_hint_x=0.1, font_size='12sp'))
        self.end_lon = TextInput(hint_text='-122.2', multiline=False, size_hint_x=0.3, font_size='12sp')
        end_row.add_widget(self.end_lon)
        calc2_content.add_widget(end_row)
        
        # Calculate button
        calc_dist_btn = Button(
            text='Calculate Distance',
            size_hint_y=None,
            height='35dp',
            background_color=(0.4, 0.7, 0.2, 1),
            font_size='14sp',
            on_press=self.calculate_distance
        )
        calc2_content.add_widget(calc_dist_btn)
        
        # Result
        self.distance_result = Label(
            text='Distance: --',
            font_size='16sp',
            color=(0.8, 1, 0.8, 1),
            size_hint_y=None,
            height='30dp'
        )
        calc2_content.add_widget(self.distance_result)
        
        # Info
        info2 = Label(
            text='Istanbul to Stanford example: ~11,900 km\nUseful for VLF propagation path analysis',
            font_size='12sp',
            color=(0.7, 0.8, 0.7, 1),
            size_hint_y=None,
            height='40dp'
        )
        calc2_content.add_widget(info2)
        
        calc2_container.add_widget(calc2_content)
        calc_layout.add_widget(calc2_container)
        
        # Calculator 3: Earth-Ionosphere Waveguide
        calc3_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height='320dp', padding=10)
        with calc3_container.canvas.before:
            Color(0.5, 0.2, 0.3, 0.8)
            calc3_container.rect = RoundedRectangle(size=calc3_container.size, pos=calc3_container.pos, radius=[10,])
            calc3_container.bind(size=self.update_calc_rect, pos=self.update_calc_rect)
        
        calc3_title = Label(
            text='[BOLT] Earth-Ionosphere Waveguide Parameters',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height='30dp',
            color=(1, 0.9, 0.9, 1)
        )
        calc3_container.add_widget(calc3_title)
        
        calc3_content = BoxLayout(orientation='vertical', spacing=5)
        
        # Input rows
        freq_row = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height='35dp')
        freq_row.add_widget(Label(text='Frequency (Hz):', size_hint_x=0.35, font_size='12sp'))
        self.waveguide_freq = TextInput(hint_text='20000', multiline=False, size_hint_x=0.35, font_size='12sp')
        freq_row.add_widget(self.waveguide_freq)
        calc3_content.add_widget(freq_row)
        
        height_row = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height='35dp')
        height_row.add_widget(Label(text='D-layer height (km):', size_hint_x=0.35, font_size='12sp'))
        self.dlayer_height = TextInput(hint_text='70', multiline=False, size_hint_x=0.35, font_size='12sp')
        height_row.add_widget(self.dlayer_height)
        calc3_content.add_widget(height_row)
        
        # Calculate button
        calc_waveguide_btn = Button(
            text='Calculate Waveguide Parameters',
            size_hint_y=None,
            height='35dp',
            background_color=(0.7, 0.2, 0.4, 1),
            font_size='14sp',
            on_press=self.calculate_waveguide
        )
        calc3_content.add_widget(calc_waveguide_btn)
        
        # Results
        results_layout = BoxLayout(orientation='vertical', spacing=3)
        
        self.cutoff_result = Label(
            text='TM₀ cutoff: --',
            font_size='14sp',
            color=(1, 0.8, 0.8, 1),
            size_hint_y=None,
            height='25dp'
        )
        results_layout.add_widget(self.cutoff_result)
        
        self.phase_velocity_result = Label(
            text='Phase velocity: --',
            font_size='14sp',
            color=(1, 0.8, 0.8, 1),
            size_hint_y=None,
            height='25dp'
        )
        results_layout.add_widget(self.phase_velocity_result)
        
        self.group_velocity_result = Label(
            text='Group velocity: --',
            font_size='14sp',
            color=(1, 0.8, 0.8, 1),
            size_hint_y=None,
            height='25dp'
        )
        results_layout.add_widget(self.group_velocity_result)
        
        self.attenuation_result = Label(
            text='Attenuation: --',
            font_size='14sp',
            color=(1, 0.8, 0.8, 1),
            size_hint_y=None,
            height='25dp'
        )
        results_layout.add_widget(self.attenuation_result)
        
        calc3_content.add_widget(results_layout)
        
        # Info
        info3 = Label(
            text='Simplified TM₀ mode calculations\nTypical D-layer: 60-90 km altitude',
            font_size='12sp',
            color=(0.8, 0.7, 0.7, 1),
            size_hint_y=None,
            height='35dp'
        )
        calc3_content.add_widget(info3)
        
        calc3_container.add_widget(calc3_content)
        calc_layout.add_widget(calc3_container)
        
        scroll.add_widget(calc_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        """Go back to main screen"""
        self.manager.current = 'main'
    
    def convert_frequency(self, instance):
        """Convert frequency to wavelength"""
        try:
            freq = float(self.freq_input.text)
            c = 299792458  # Speed of light in m/s
            wavelength = c / freq
            
            if wavelength >= 1000:
                self.wavelength_result.text = f'Wavelength: {wavelength/1000:.2f} km'
            else:
                self.wavelength_result.text = f'Wavelength: {wavelength:.2f} m'
        except ValueError:
            self.wavelength_result.text = 'Invalid input - please enter a number'
        except ZeroDivisionError:
            self.wavelength_result.text = 'Frequency cannot be zero'
    
    def calculate_distance(self, instance):
        """Calculate great circle distance between two points"""
        try:
            lat1 = math.radians(float(self.start_lat.text))
            lon1 = math.radians(float(self.start_lon.text))
            lat2 = math.radians(float(self.end_lat.text))
            lon2 = math.radians(float(self.end_lon.text))
            
            # Haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            r = 6371  # Earth radius in km
            distance = c * r
            
            self.distance_result.text = f'Distance: {distance:.1f} km'
        except ValueError:
            self.distance_result.text = 'Invalid coordinates - please enter numbers'
        except Exception as e:
            self.distance_result.text = f'Error: {str(e)}'
    
    def calculate_waveguide(self, instance):
        """Calculate Earth-ionosphere waveguide parameters"""
        try:
            freq = float(self.waveguide_freq.text)
            height = float(self.dlayer_height.text) * 1000  # Convert to meters
            c = 299792458  # Speed of light
            
            # TM0 mode cutoff frequency (simplified)
            cutoff_freq = c / (2 * height)
            self.cutoff_result.text = f'TM₀ cutoff: {cutoff_freq:.1f} Hz'
            
            # Phase velocity (simplified for TM0)
            if freq > cutoff_freq:
                phase_vel = c / math.sqrt(1 - (cutoff_freq/freq)**2)
                self.phase_velocity_result.text = f'Phase velocity: {phase_vel/c:.4f}c'
                
                # Group velocity
                group_vel = c * math.sqrt(1 - (cutoff_freq/freq)**2)
                self.group_velocity_result.text = f'Group velocity: {group_vel/c:.4f}c'
            else:
                self.phase_velocity_result.text = 'Below cutoff frequency'
                self.group_velocity_result.text = 'Below cutoff frequency'
            
            # Simplified attenuation
            atten_db_per_mm = 2.5  # Typical VLF attenuation
            self.attenuation_result.text = f'Attenuation: ~{atten_db_per_mm} dB/Mm'
            
        except ValueError:
            self.cutoff_result.text = 'Invalid input - please enter numbers'
            self.phase_velocity_result.text = '--'
            self.group_velocity_result.text = '--'
            self.attenuation_result.text = '--'
        except Exception as e:
            self.cutoff_result.text = f'Error: {str(e)}'
            self.phase_velocity_result.text = '--'
            self.group_velocity_result.text = '--'
            self.attenuation_result.text = '--'
    
    def update_calc_rect(self, instance, value):
        """Update calculator rectangle position and size"""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def open_lab_website(self, instance):
        """Open the lab website"""
        try:
            webbrowser.open('https://vlfstanford.ku.edu.tr/')
        except Exception as e:
            print(f'Could not open website: {e}')

class PapersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'papers'
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        back_btn = Button(text='← Back', size_hint_x=0.2, background_color=(0.8, 0.3, 0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header_layout.add_widget(back_btn)
        header_layout.add_widget(Label(text='Research Papers', font_size='18sp', bold=True))
        layout.add_widget(header_layout)
        
        # Search controls
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        
        self.search_input = TextInput(hint_text='Search terms (e.g., VLF, plasma, electromagnetic)', multiline=False)
        search_btn = Button(text='Search arXiv', size_hint_x=0.25, background_color=(0.3, 0.7, 1, 1))
        search_btn.bind(on_press=self.search_arxiv)
        
        category_btn = Button(text='Physics Categories', size_hint_x=0.25, background_color=(0.7, 0.3, 1, 1))
        category_btn.bind(on_press=self.load_physics_categories)
        
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_btn)
        search_layout.add_widget(category_btn)
        layout.add_widget(search_layout)
        
        # Status label
        self.status_label = Label(
            text='Enter search terms and click "Search arXiv" for latest papers',
            size_hint_y=0.08,
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(self.status_label)
        
        # Papers list
        scroll = ScrollView()
        self.papers_content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.papers_content.bind(minimum_height=self.papers_content.setter('height'))
        
        self.load_sample_papers()
        
        scroll.add_widget(self.papers_content)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def update_status(self, message):
        """Update the status label"""
        self.status_label.text = message
    
    def clear_papers(self):
        """Clear current papers"""
        self.papers_content.clear_widgets()
    
    def search_arxiv(self, instance):
        """Search arXiv for papers"""
        search_terms = self.search_input.text.strip()
        if not search_terms:
            self.update_status('Please enter search terms')
            return
        
        self.update_status(f'Searching arXiv for: {search_terms}...')
        threading.Thread(target=self._search_arxiv_thread, args=(search_terms,), daemon=True).start()
    
    def _search_arxiv_thread(self, search_terms):
        """Thread function to search arXiv"""
        try:
            base_url = "http://export.arxiv.org/api/query"
            
            params = {
                'search_query': f'all:{search_terms}',
                'start': 0,
                'max_results': 15,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            response = requests.get(base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                
                papers = []
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                    summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                    published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                    
                    authors = []
                    for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                        name_elem = author.find('{http://www.w3.org/2005/Atom}name')
                        if name_elem is not None:
                            authors.append(name_elem.text)
                    
                    categories = []
                    for category in entry.findall('{http://www.w3.org/2005/Atom}category'):
                        term = category.get('term', '')
                        if term:
                            categories.append(term)
                    
                    # Extract arXiv ID and construct URLs
                    arxiv_id = ''
                    pdf_url = ''
                    abstract_url = ''
                    
                    entry_id = entry.find('{http://www.w3.org/2005/Atom}id')
                    if entry_id is not None:
                        id_text = entry_id.text
                        if 'arxiv.org/abs/' in id_text:
                            arxiv_id = id_text.split('arxiv.org/abs/')[-1]
                            if 'v' in arxiv_id:
                                arxiv_id = arxiv_id.split('v')[0]
                            
                            abstract_url = f"https://arxiv.org/abs/{arxiv_id}"
                            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                    
                    paper = {
                        'title': title_elem.text.strip() if title_elem is not None else 'No title',
                        'abstract': summary_elem.text.strip() if summary_elem is not None else 'No abstract',
                        'authors': authors,
                        'published': published_elem.text[:10] if published_elem is not None else '',
                        'categories': categories,
                        'pdf_url': pdf_url,
                        'abstract_url': abstract_url,
                        'arxiv_id': arxiv_id
                    }
                    papers.append(paper)
                
                Clock.schedule_once(lambda dt: self._update_arxiv_results(papers, search_terms))
            else:
                Clock.schedule_once(lambda dt: self.update_status(f'Error: HTTP {response.status_code}'))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f'Error searching arXiv: {str(e)}'))
    
    def _update_arxiv_results(self, papers, search_terms):
        """Update UI with arXiv search results"""
        self.clear_papers()
        self.update_status(f'Found {len(papers)} papers for "{search_terms}"')
        
        for paper in papers:
            self.add_arxiv_paper(paper)
    
    def load_physics_categories(self, instance):
        """Load papers from specific physics categories"""
        self.update_status('Loading papers from physics categories...')
        threading.Thread(target=self._load_physics_categories_thread, daemon=True).start()
    
    def _load_physics_categories_thread(self):
        """Thread function to load physics category papers"""
        try:
            base_url = "http://export.arxiv.org/api/query"
            
            categories = [
                'physics.space-ph',    # Space Physics
                'physics.plasm-ph',    # Plasma Physics
                'physics.ao-ph',       # Atmospheric and Oceanic Physics
                'physics.geo-ph',      # Geophysics
            ]
            
            all_papers = []
            
            for category in categories:
                params = {
                    'search_query': f'cat:{category}',
                    'start': 0,
                    'max_results': 5,
                    'sortBy': 'submittedDate',
                    'sortOrder': 'descending'
                }
                
                response = requests.get(base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    
                    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                        title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                        summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                        published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                        
                        authors = []
                        for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                            name_elem = author.find('{http://www.w3.org/2005/Atom}name')
                            if name_elem is not None:
                                authors.append(name_elem.text)
                        
                        categories_list = []
                        for cat in entry.findall('{http://www.w3.org/2005/Atom}category'):
                            term = cat.get('term', '')
                            if term:
                                categories_list.append(term)
                        
                        # Extract arXiv ID and construct URLs
                        arxiv_id = ''
                        pdf_url = ''
                        abstract_url = ''
                        
                        entry_id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                        if entry_id_elem is not None:
                            id_text = entry_id_elem.text
                            if 'arxiv.org/abs/' in id_text:
                                arxiv_id = id_text.split('arxiv.org/abs/')[-1]
                                if 'v' in arxiv_id:
                                    arxiv_id = arxiv_id.split('v')[0]
                                
                                abstract_url = f"https://arxiv.org/abs/{arxiv_id}"
                                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                        
                        paper = {
                            'title': title_elem.text.strip() if title_elem is not None else 'No title',
                            'abstract': summary_elem.text.strip() if summary_elem is not None else 'No abstract',
                            'authors': authors,
                            'published': published_elem.text[:10] if published_elem is not None else '',
                            'categories': categories_list,
                            'pdf_url': pdf_url,
                            'abstract_url': abstract_url,
                            'arxiv_id': arxiv_id
                        }
                        all_papers.append(paper)
            
            Clock.schedule_once(lambda dt: self._update_category_results(all_papers))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f'Error loading categories: {str(e)}'))
    
    def _update_category_results(self, papers):
        """Update UI with category results"""
        self.clear_papers()
        self.update_status(f'Loaded {len(papers)} papers from physics categories')
        
        for paper in papers:
            self.add_arxiv_paper(paper)
    
    def add_arxiv_paper(self, paper):
        """Add an arXiv paper to the display"""
        paper_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height='180dp')
        
        main_container = BoxLayout(orientation='vertical', spacing=5, padding=[10, 8, 10, 8])
        
        # Title
        title = Label(
            text=paper['title'],
            font_size='15sp',
            bold=True,
            size_hint_y=None,
            height='50dp',
            color=(0.3, 0.7, 1, 1),
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        main_container.add_widget(title)
        
        # Authors
        authors_text = ', '.join(paper['authors'][:3]) if paper['authors'] else 'Unknown authors'
        if len(paper['authors']) > 3:
            authors_text += f' et al. ({len(paper["authors"])} total)'
        
        authors = Label(
            text=f"[PEOPLE] {authors_text}",
            font_size='13sp',
            size_hint_y=None,
            height='25dp',
            color=(0.4, 0.8, 0.4, 1),
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        main_container.add_widget(authors)
        
        # Date and categories
        categories_text = ', '.join(paper['categories'][:2]) if paper['categories'] else 'No categories'
        if len(paper['categories']) > 2:
            categories_text += '...'
        
        meta = Label(
            text=f"[DATE] {paper['published']} • [TAG] {categories_text}",
            font_size='12sp',
            size_hint_y=None,
            height='20dp',
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        main_container.add_widget(meta)
        
        # Abstract preview
        abstract_preview = paper['abstract']
        if len(abstract_preview) > 90:
            abstract_preview = abstract_preview[:90] + '...'
        
        abstract = Label(
            text=abstract_preview,
            font_size='13sp',
            size_hint_y=None,
            height='40dp',
            color=(0.9, 0.9, 0.9, 1),
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        main_container.add_widget(abstract)
        
        # Click button
        click_btn = Button(
            text='[DOC] Open Paper',
            font_size='12sp',
            size_hint_y=None,
            height='25dp',
            background_color=(0.2, 0.6, 0.3, 1),
            on_press=lambda x: self.open_paper_detail(paper)
        )
        main_container.add_widget(click_btn)
        
        # Add background color
        with main_container.canvas.before:
            Color(0.15, 0.25, 0.15, 0.8)
            main_container.rect = RoundedRectangle(size=main_container.size, pos=main_container.pos, radius=[5,])
            main_container.bind(size=self.update_rect, pos=self.update_rect)
        
        # Update text sizes when container size changes
        def update_text_sizes(instance, size):
            title.text_size = (size[0] - 20, None)
            authors.text_size = (size[0] - 20, None)
            meta.text_size = (size[0] - 20, None)
            abstract.text_size = (size[0] - 20, None)
        
        main_container.bind(size=update_text_sizes)
        
        paper_layout.add_widget(main_container)
        self.papers_content.add_widget(paper_layout)
    
    def update_rect(self, instance, value):
        """Update rectangle size and position"""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def open_paper_detail(self, paper):
        """Open research paper in web browser"""
        abstract_url = paper.get('abstract_url', '')
        pdf_url = paper.get('pdf_url', '')
        arxiv_id = paper.get('arxiv_id', '')
        
        url_to_open = ''
        
        if abstract_url and 'arxiv.org' in abstract_url:
            url_to_open = abstract_url
            url_type = "arXiv abstract page"
        elif arxiv_id:
            url_to_open = f"https://arxiv.org/abs/{arxiv_id}"
            url_type = "arXiv abstract page"
        elif pdf_url and 'arxiv.org' in pdf_url:
            url_to_open = pdf_url
            url_type = "arXiv PDF"
        else:
            title_clean = paper['title'].replace(' ', '+').replace(',', '').replace(':', '').replace('"', '')
            url_to_open = f"https://arxiv.org/search/?query={title_clean}&searchtype=title"
            url_type = "arXiv search results"
        
        if url_to_open:
            try:
                webbrowser.open(url_to_open)
                self.update_status(f'Opening {url_type}: {paper["title"][:40]}...')
            except Exception as e:
                self.update_status(f'Could not open browser: {str(e)}')
        else:
            self.update_status('No valid URL found for this paper')
    
    def load_sample_papers(self):
        """Load sample papers as fallback"""
        papers = [
            {
                'title': 'Welcome to VLF Research Papers',
                'authors': ['VLF Research Hub'],
                'published': '2025-05-24',
                'abstract': 'Use the search box above to find the latest research papers from arXiv. You can search for specific terms like "VLF electromagnetic waves", "lightning radio waves", or "plasma physics".',
                'categories': ['App Info'],
                'pdf_url': '',
                'abstract_url': 'https://arxiv.org/list/physics.space-ph/recent',
                'arxiv_id': ''
            }
        ]
        
        for paper in papers:
            self.add_arxiv_paper(paper)

class PlasmaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'plasma'
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        back_btn = Button(text='← Back', size_hint_x=0.2, background_color=(0.8, 0.3, 0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header_layout.add_widget(back_btn)
        header_layout.add_widget(Label(text='Plasma Physics', font_size='18sp', bold=True))
        layout.add_widget(header_layout)
        
        # Content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Plasma physics sections
        sections = [
            {
                'title': 'Fundamental Plasma Physics',
                'content': '''
PLASMA DEFINITION AND CHARACTERISTICS:

What is Plasma?
• Fourth state of matter: ionized gas
• Quasi-neutral: nₑ ≈ nᵢ (macroscopically)
• Collective behavior dominates
• Long-range Coulomb forces important
• ~99% of visible universe is plasma

Plasma Parameters:
• Electron density: nₑ [m⁻³]
• Ion density: nᵢ [m⁻³] 
• Electron temperature: Tₑ [K] or [eV]
• Ion temperature: Tᵢ [K] or [eV]
• Magnetic field strength: B [T] or [nT]

CHARACTERISTIC FREQUENCIES:

Plasma Frequency:
• Electron: ωₚₑ = √(nₑe²/mₑε₀) [rad/s]
• fₚₑ = ωₚₑ/2π ≈ 8980√nₑ Hz (nₑ in cm⁻³)

Cyclotron Frequency:
• Electron: ωcₑ = eB/mₑ ≈ 1.76×10¹¹ B [rad/s]
• fcₑ = ωcₑ/2π ≈ 28.0 B [Hz] (B in nT)
• Proton: fcₚ ≈ 15.2 B [Hz] (B in nT)

Debye Length:
• λD = √(ε₀kTₑ/nₑe²) ≈ 740√(Tₑ[eV]/nₑ[cm⁻³]) m
• Plasma condition: λD ≪ L (system size)
                '''
            },
            {
                'title': 'Space Plasma Environments',
                'content': '''
SOLAR WIND:

Properties at 1 AU:
• Density: nₚ ≈ 5-20 cm⁻³ (typical: 7 cm⁻³)
• Velocity: v ≈ 300-800 km/s (typical: 400 km/s)
• Temperature: Tₚ ≈ 10⁴-10⁵ K (1-10 eV)
• Magnetic field: B ≈ 3-10 nT

MAGNETOSPHERE:

Regions:
• Bow shock: standoff distance ~15 RE
• Magnetosheath: shocked solar wind
• Magnetopause: boundary at ~10 RE (subsolar)
• Plasmasphere: cold, dense plasma (< 4 RE)
• Ring current: hot ions (3-8 RE)
• Plasma sheet: hot, tenuous plasma (> 8 RE)

IONOSPHERE:

Layers and Properties:
• D-layer (60-90 km): nₑ ~ 10²-10⁴ cm⁻³
• E-layer (90-130 km): nₑ ~ 10⁴-10⁵ cm⁻³
• F1-layer (130-200 km): nₑ ~ 10⁵ cm⁻³
• F2-layer (200-500 km): nₑ ~ 10⁶ cm⁻³

VAN ALLEN RADIATION BELTS:

Inner Belt:
• Location: L ~ 1.2-2.5
• Composition: mainly protons (10-100 MeV)
• Relatively stable population

Outer Belt:
• Location: L ~ 3-7
• Composition: mainly electrons (0.1-10 MeV)
• Highly variable with geomagnetic activity
                '''
            },
            {
                'title': 'VLF Waves in Plasma',
                'content': '''
ELECTROMAGNETIC WAVES IN PLASMA:

Whistler Mode Waves:
• Frequency range: ωcᵢ ≪ ω ≪ ωcₑ
• Right-hand circularly polarized
• Propagation: mostly parallel to B₀
• Dispersion: ω ∝ k² (highly dispersive)

VLF WAVES IN MAGNETOSPHERE:

Natural VLF Emissions:
• Whistlers: dispersed lightning VLF
• Chorus: coherent emissions near fcₑ/2
• Hiss: broadband incoherent noise
• QP (Quasi-Periodic) emissions

Whistler Characteristics:
• Source: lightning VLF enters magnetosphere
• Propagation: along geomagnetic field lines
• Dispersion time: Δt = D/√f
• D ≈ 36√(L) s·Hz¹/² (empirical)

Chorus Waves:
• Frequency: typically 0.1-0.8 fcₑ
• Generation: cyclotron instability
• Structure: rising or falling tones
• Duration: 0.1-1 s individual elements

WAVE-PARTICLE INTERACTIONS:

Cyclotron Resonance:
• Resonance condition: ω - k∥v∥ = nωc
• First-order cyclotron (n = 1)
• Pitch angle scattering of electrons
• Energy transfer between wave and particles

Applications to VLF Research:
• Lightning-generated whistlers
• VLF transmitter signals
• D-region electron density changes
• Space weather monitoring
                '''
            }
        ]
        
        for section in sections:
            # Section header
            header = Label(
                text=section['title'],
                font_size='16sp',
                bold=True,
                size_hint_y=None,
                height='40dp',
                color=(0.2, 0.6, 1, 1)
            )
            content.add_widget(header)
            
            # Section content
            text_label = Label(
                text=section['content'],
                text_size=(None, None),
                size_hint_y=None,
                halign='left',
                valign='top',
                font_size='14sp'
            )
            text_label.bind(texture_size=text_label.setter('size'))
            content.add_widget(text_label)
            
            # Spacing
            content.add_widget(Label(size_hint_y=None, height='20dp'))
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)

class SpaceWeatherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'weather'
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        back_btn = Button(text='← Back', size_hint_x=0.2, background_color=(0.8, 0.3, 0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        header_layout.add_widget(back_btn)
        header_layout.add_widget(Label(text='Space Weather & VLF', font_size='18sp', bold=True))
        layout.add_widget(header_layout)
        
        # Status and controls
        controls_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        
        update_btn = Button(text='Update Space Weather', background_color=(0.3, 0.8, 0.3, 1))
        update_btn.bind(on_press=self.fetch_space_weather)
        
        self.status_label = Label(
            text='Click "Update Space Weather" for current conditions',
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        
        controls_layout.add_widget(update_btn)
        controls_layout.add_widget(self.status_label)
        layout.add_widget(controls_layout)
        
        # Space weather content
        scroll = ScrollView()
        self.weather_content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.weather_content.bind(minimum_height=self.weather_content.setter('height'))
        
        self.load_space_weather_info()
        
        scroll.add_widget(self.weather_content)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def update_status(self, message):
        """Update the status label"""
        self.status_label.text = message
    
    def clear_content(self):
        """Clear current content"""
        self.weather_content.clear_widgets()
    
    def fetch_space_weather(self, instance):
        """Fetch current space weather data"""
        self.update_status('Fetching space weather data...')
        threading.Thread(target=self._fetch_space_weather_thread, daemon=True).start()
    
    def _fetch_space_weather_thread(self):
        """Thread function to fetch space weather"""
        try:
            sample_data = {
                'solar_flux': '142 sfu',
                'sunspot_number': '85',
                'k_index': '3 (Unsettled)',
                'solar_wind_speed': '425 km/s',
                'bz_component': '-2.3 nT',
                'geomagnetic_activity': 'Quiet to Unsettled',
                'vlf_impact': 'Normal propagation conditions',
                'd_layer_absorption': 'Low (<1 dB)',
                'forecast': 'Quiet geomagnetic conditions expected for next 24h'
            }
            
            Clock.schedule_once(lambda dt: self._update_space_weather(sample_data))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f'Error fetching data: {str(e)}'))
    
    def _update_space_weather(self, data):
        """Update UI with space weather data"""
        self.clear_content()
        self.update_status('Space weather data updated')
        
        # Current conditions
        self.add_weather_section('Current Space Weather Conditions', [
            f"Solar Flux (10.7 cm): {data['solar_flux']}",
            f"Sunspot Number: {data['sunspot_number']}",
            f"K-index: {data['k_index']}",
            f"Solar Wind Speed: {data['solar_wind_speed']}",
            f"Bz Component: {data['bz_component']}",
            f"Geomagnetic Activity: {data['geomagnetic_activity']}"
        ])
        
        # VLF Impact
        self.add_weather_section('VLF Propagation Impact', [
            f"Current VLF Conditions: {data['vlf_impact']}",
            f"D-layer Absorption: {data['d_layer_absorption']}",
            "• Normal VLF propagation in Earth-ionosphere waveguide",
            "• Minimal signal degradation expected",
            "• Standard attenuation rates (~2-3 dB/Mm)"
        ])
        
        # Forecast
        self.add_weather_section('24-Hour Forecast', [
            data['forecast'],
            "• VLF propagation should remain stable",
            "• Monitor for sudden ionospheric disturbances",
            "• Lightning-generated sferics unaffected"
        ])
    
    def add_weather_section(self, title, items):
        """Add a weather information section"""
        # Section title
        title_label = Label(
            text=title,
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height='40dp',
            color=(0.2, 0.6, 1, 1),
            halign='left',
            text_size=(None, None)
        )
        self.weather_content.add_widget(title_label)
        
        # Section content
        for item in items:
            item_label = Label(
                text=item,
                font_size='14sp',
                size_hint_y=None,
                halign='left',
                text_size=(None, None)
            )
            item_label.bind(texture_size=item_label.setter('size'))
            self.weather_content.add_widget(item_label)
        
        # Spacing
        self.weather_content.add_widget(Label(size_hint_y=None, height='20dp'))
    
    def load_space_weather_info(self):
        """Load initial space weather information"""
        self.add_weather_section('Space Weather & VLF Research', [
            'Space weather affects VLF wave propagation through:',
            '• D-layer ionization changes',
            '• Geomagnetic storm effects on ionosphere',
            '• Solar flare X-ray enhancement',
            '• Sudden ionospheric disturbances (SIDs)',
            '',
            'Click "Update Space Weather" for current conditions.'
        ])
        
        self.add_weather_section('Key Parameters for VLF', [
            'Solar Flux (10.7 cm): Indicates solar activity level',
            'K-index: Geomagnetic activity indicator',
            'Solar wind parameters: Affect magnetosphere',
            'X-ray flux: Directly ionizes D-layer',
            '',
            'VLF propagation is most affected by D-layer changes.'
        ])

class VLFResearchApp(App):
    def build(self):
        self.title = 'VLF Research Hub'
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MainScreen())
        sm.add_widget(TheoryScreen())
        sm.add_widget(NewsScreen())
        sm.add_widget(PapersScreen())
        sm.add_widget(CalculatorsScreen())
        sm.add_widget(PlasmaScreen())
        sm.add_widget(SpaceWeatherScreen())
        
        return sm

if __name__ == '__main__':
    VLFResearchApp().run()