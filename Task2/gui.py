import tkinter as tk
from tkinter import ttk, Canvas
from PIL import Image, ImageTk, ImageEnhance
import json
from pathlib import Path
import os
from game_logic import GameLogic, GameMode
import math
import time
import random

class ModernRPSGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Epic Rock Paper Scissors")
        self.root.geometry("1280x800")
        self.root.configure(bg='#1A1A2E')
        
        # Enable transparency
        self.root.attributes('-alpha', 0.0)
        
        self.game_logic = GameLogic()
        self.scores = self.load_scores()
        
        # Enhanced power-up system
        self.power_meter = 0
        self.power_up_active = False
        self.power_up_types = ['Double Damage', 'Second Chance', 'Pattern Break']
        self.current_power_up = None
        
        # Enhanced particle system
        self.particles = []
        self.particle_types = ['circle', 'star', 'spark']
        
        # Animation states
        self.animations = {
            'fade_in': {'progress': 0, 'duration': 20},
            'button_scale': {'scale': 1.0},
            'power_pulse': {'scale': 1.0, 'increasing': True}
        }
        
        self.setup_styles()
        self.load_enhanced_assets()
        self.create_enhanced_widgets()
        self.start_animations()
        
        # Fade in animation
        self.fade_in_animation()

    def load_enhanced_assets(self):
        # Remove image loading since we'll use shapes/animations instead
        self.move_colors = {
            'rock': '#E74C3C',     # Red
            'paper': '#3498DB',    # Blue
            'scissors': '#2ECC71', # Green
            'lizard': '#9B59B6',   # Purple
            'spock': '#F1C40F'     # Yellow
        }

    def create_star_image(self):
        size = 20
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        # Create star shape using PIL
        return ImageTk.PhotoImage(img)

    def setup_styles(self):
        self.colors = {
            'bg': '#1A1A2E',
            'fg': '#E94560',
            'button': '#0F3460',
            'button_hover': '#16213E',
            'win': '#4CAF50',
            'lose': '#F44336',
            'tie': '#FF9800',
            'power': '#9C27B0',
            'accent1': '#00B4D8',
            'accent2': '#FF6B6B'
        }
        
        style = ttk.Style()
        style.configure("Game.TFrame", background=self.colors['bg'])
        style.configure("Game.TLabel",
                       font=('Montserrat', 16),
                       background=self.colors['bg'],
                       foreground=self.colors['fg'])
        style.configure("Score.TLabel",
                       font=('Montserrat', 28, 'bold'),
                       background=self.colors['bg'],
                       foreground=self.colors['fg'])

    def create_enhanced_widgets(self):
        # Main container with gradient background
        self.main_frame = ttk.Frame(self.root, style="Game.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Header with animated title
        self.create_animated_header()

        # Mode selector with modern tabs
        self.create_mode_selector()

        # Enhanced score display with animations
        self.create_score_display()

        # Create game area before power-up system
        self.create_game_area()

        # Power-up system with visual effects
        self.create_power_up_system()

        # Move buttons with hover effects and animations
        self.create_enhanced_move_buttons()

    def create_animated_header(self):
        self.header_frame = ttk.Frame(self.main_frame, style="Game.TFrame")
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ttk.Label(self.header_frame,
                                    text="Epic Rock Paper Scissors",
                                    style="Game.TLabel",
                                    font=('Montserrat', 32, 'bold'))
        self.title_label.pack()
        
        self.animate_title()

    def create_mode_selector(self):
        mode_frame = ttk.Frame(self.main_frame, style="Game.TFrame")
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        for mode in GameMode:
            btn = tk.Button(mode_frame,
                           text=mode.value,
                           command=lambda m=mode: self.change_mode(m),
                           font=('Roboto', 12),
                           bg=self.colors['button'],
                           fg='white',
                           relief=tk.FLAT,
                           padx=15,
                           pady=8)
            btn.pack(side=tk.LEFT, padx=5, expand=True)
            self.setup_button_hover(btn)

    def create_score_display(self):
        """Create the score display area"""
        self.score_frame = ttk.Frame(self.main_frame, style="Game.TFrame")
        self.score_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.score_label = ttk.Label(self.score_frame,
                                    text=self.get_score_text(),
                                    style="Game.TLabel",
                                    font=('Montserrat', 24, 'bold'))
        self.score_label.pack()

    def create_power_up_system(self):
        """Create the power-up meter and display"""
        power_frame = ttk.Frame(self.main_frame, style="Game.TFrame")
        power_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Power meter canvas
        self.power_canvas = Canvas(power_frame,
                                 width=400,  # Set initial width
                                 height=30,
                                 bg=self.colors['bg'],
                                 highlightthickness=0)
        self.power_canvas.pack(fill=tk.X, padx=20)
        
        # Create power meter bar with initial position
        self.power_bar = self.power_canvas.create_rectangle(
            10, 5, 10, 25,
            fill=self.colors['power'],
            width=0
        )

    def create_game_area(self):
        """Create the main game area canvas"""
        self.game_area = Canvas(self.main_frame,
                               width=800,
                               height=400,
                               bg=self.colors['bg'],
                               highlightthickness=0)
        self.game_area.pack(pady=20)

    def animate_title(self):
        progress = self.animations['fade_in']['progress']
        if progress < self.animations['fade_in']['duration']:
            opacity = progress / self.animations['fade_in']['duration']
            self.root.attributes('-alpha', opacity)
            self.animations['fade_in']['progress'] += 1
            
            # Add glow effect
            glow_intensity = math.sin(progress * math.pi / 10)  # Oscillating glow
            glow_color = self.adjust_color_brightness(self.colors['fg'], int(glow_intensity * 30))
            self.title_label.configure(foreground=glow_color)
            
            self.root.after(50, self.animate_title)
        else:
            self.root.attributes('-alpha', 1.0)

    def fade_in_animation(self):
        progress = self.animations['fade_in']['progress']
        if progress < self.animations['fade_in']['duration']:
            opacity = progress / self.animations['fade_in']['duration']
            self.root.attributes('-alpha', opacity)
            self.animations['fade_in']['progress'] += 1
            self.root.after(16, self.fade_in_animation)

    def start_animations(self):
        self.animate_particles()
        self.animate_power_meter()
        self.animate_title()

    def create_enhanced_move_buttons(self):
        btn_frame = ttk.Frame(self.main_frame, style="Game.TFrame")
        btn_frame.pack(fill=tk.X, pady=20)
        
        choices = self.game_logic.get_current_choices()
        for choice in choices:
            btn = tk.Button(btn_frame,
                          text=choice.title(),
                          command=lambda c=choice: self.play_round(c),
                          font=('Roboto', 14, 'bold'),
                          bg=self.move_colors.get(choice, self.colors['button']),  # Added fallback color
                          fg='white',
                          relief=tk.FLAT,
                          padx=20,
                          pady=10)
            btn.pack(side=tk.LEFT, padx=10, expand=True)
            self.setup_button_hover(btn)

    def setup_button_hover(self, button):
        button.bind('<Enter>', lambda e: self.button_hover_effect(button, True))
        button.bind('<Leave>', lambda e: self.button_hover_effect(button, False))

    def button_hover_effect(self, button, entering):
        if entering:
            button.config(bg=self.colors['button_hover'])
            # Add floating effect
            button.pack_configure(pady=5)
        else:
            button.config(bg=self.colors['button'])
            button.pack_configure(pady=10)

    def change_mode(self, mode):
        self.game_logic.set_mode(mode)
        self.power_meter = 0
        self.update_power_bar()
        # Recreate buttons for advanced mode
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Frame) and widget != self.score_frame:
                widget.destroy()
        self.create_enhanced_move_buttons()  # Changed from create_move_buttons

    def play_round(self, player_choice):
        if self.power_up_active:
            # Enhanced power-up effects
            if self.current_power_up == 'Double Damage':
                result = self.game_logic.play_round(player_choice)
                if result['outcome'] == 'win':
                    self.scores['player'] += 1  # Extra point
            elif self.current_power_up == 'Second Chance':
                result = self.game_logic.play_round(player_choice)
                if result['outcome'] == 'lose':
                    result = self.game_logic.play_round(player_choice)
            else:  # Pattern Break
                self.game_logic.player_history = []  # Reset pattern
                result = self.game_logic.play_round(player_choice)
                
            self.power_up_active = False
            self.power_meter = 0
            self.current_power_up = None
        else:
            result = self.game_logic.play_round(player_choice)

        # Enhanced battle animation
        self.animate_enhanced_battle(player_choice, result['computer_choice'], result['outcome'])
        
        # Update scores and effects
        if result['outcome'] == 'win':
            self.scores['player'] += 1
            self.power_meter = min(100, self.power_meter + 20)
            if result['combo'] > 1:
                self.show_enhanced_combo_animation(result['combo'])
        elif result['outcome'] == 'lose':
            self.scores['computer'] += 1
            
        self.score_label.configure(text=self.get_score_text())
        self.update_power_bar()
        self.save_scores()

    def animate_enhanced_battle(self, player_choice, computer_choice, outcome):
        # Clear canvas and set up initial positions
        self.game_area.delete("all")
        
        # Create background effects
        self.create_battle_background(outcome)
        
        # Animate moves with enhanced effects
        self.animate_moves(player_choice, computer_choice, outcome)
        
        # Add particle effects
        self.add_enhanced_battle_effects(outcome)

    def create_battle_background(self, outcome):
        # Create dynamic background based on outcome
        color = self.colors['tie']
        if outcome == 'win':
            color = self.colors['win']
        elif outcome == 'lose':
            color = self.colors['lose']
            
        # Add gradient and glow effects
        self.game_area.create_rectangle(0, 0, 800, 400,
                                      fill=color,
                                      stipple='gray50')

    def show_enhanced_combo_animation(self, combo):
        # Create combo text with glow effect
        text = f"COMBO x{combo}! 🔥"
        x = self.game_area.winfo_width() / 2
        y = self.game_area.winfo_height() / 2
        
        # Add multiple layers for glow effect
        for i in range(3):
            self.game_area.create_text(
                x, y + i*2,
                text=text,
                font=('Montserrat', 36 - i*2, 'bold'),
                fill=self.adjust_color_brightness(self.colors['win'], -20*i)
            )
        
        # Add particle burst
        self.add_combo_particles(x, y, combo)

    def add_combo_particles(self, x, y, combo):
        for _ in range(combo * 5):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 10)
            particle = {
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(20, 40),
                'color': self.colors['win'],
                'type': random.choice(self.particle_types)
            }
            self.particles.append(particle)

    def add_enhanced_battle_effects(self, outcome):
        # Add particles
        color = self.colors['tie']
        if outcome == 'win':
            color = self.colors['win']
        elif outcome == 'lose':
            color = self.colors['lose']
            
        for _ in range(5):
            particle = {
                'x': 400,
                'y': 200,
                'dx': random.uniform(-5, 5),
                'dy': random.uniform(-5, 5),
                'life': 20,
                'color': color
            }
            self.particles.append(particle)

    def animate_particles(self):
        # Update and draw particles
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            
            if particle['life'] > 0:
                size = particle['life']
                self.game_area.create_oval(
                    particle['x']-size, particle['y']-size,
                    particle['x']+size, particle['y']+size,
                    fill=particle['color'], outline=""
                )
            else:
                self.particles.remove(particle)
                
        self.root.after(16, self.animate_particles)

    def get_score_text(self):
        return f"Player {self.scores['player']} - {self.scores['computer']} Computer"

    def load_scores(self):
        try:
            with open('scores.json', 'r') as f:
                return json.load(f)
        except:
            return {'player': 0, 'computer': 0}

    def save_scores(self):
        with open('scores.json', 'w') as f:
            json.dump(self.scores, f)

    def adjust_color_brightness(self, color, factor):
        """Adjust the brightness of a hex color by a factor"""
        # Remove the '#' and convert to RGB
        r = int(color[1:3], 16) + factor
        g = int(color[3:5], 16) + factor
        b = int(color[5:7], 16) + factor
        
        # Ensure values stay within valid range (0-255)
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        # Convert back to hex format
        return f'#{r:02x}{g:02x}{b:02x}'

    def update_power_bar(self):
        """Update the power bar with error handling"""
        try:
            width = self.power_canvas.winfo_width()
            if width > 0:  # Only update if width is valid
                bar_width = (width - 20) * self.power_meter / 100
                self.power_canvas.coords(self.power_bar, 10, 5, 10 + bar_width, 25)
                
                if self.power_meter >= 100:
                    self.show_power_up_options()
        except Exception as e:
            print(f"Error updating power bar: {e}")
            # Set a default width if there's an error
            self.power_canvas.configure(width=400)

    def show_power_up_options(self):
        if not self.power_up_active:
            power_up = random.choice(self.power_up_types)
            self.current_power_up = power_up
            self.power_up_active = True
            
            # Create floating notification
            notification = tk.Label(self.game_area,
                                  text=f"Power Up: {power_up}!",
                                  font=('Montserrat', 16, 'bold'),
                                  fg=self.colors['power'],
                                  bg=self.colors['bg'])
            notification.place(relx=0.5, rely=0.1, anchor='center')
            
            # Animate notification
            self.animate_notification(notification)

    def animate_notification(self, widget, opacity=1.0):
        if opacity > 0:
            widget.configure(fg=self.adjust_color_brightness(self.colors['power'], 
                                                           int((1-opacity) * 100)))
            self.root.after(50, lambda: self.animate_notification(widget, opacity - 0.05))
        else:
            widget.destroy()

    def animate_power_meter(self):
        """Animates the power meter with a pulsing effect when full"""
        if self.power_meter >= 100:
            # Pulsing animation when power meter is full
            if self.animations['power_pulse']['increasing']:
                self.animations['power_pulse']['scale'] += 0.05
                if self.animations['power_pulse']['scale'] >= 1.2:
                    self.animations['power_pulse']['increasing'] = False
            else:
                self.animations['power_pulse']['scale'] -= 0.05
                if self.animations['power_pulse']['scale'] <= 1.0:
                    self.animations['power_pulse']['increasing'] = True
        
            # Apply the scale effect
            scale = self.animations['power_pulse']['scale']
            self.power_canvas.itemconfig(self.power_bar, 
                                       fill=self.adjust_color_brightness(self.colors['power'], 
                                                                       int((scale - 1) * 50)))
    
        # Continue the animation loop
        self.root.after(50, self.animate_power_meter)

    def animate_moves(self, player_choice, computer_choice, outcome):
        """Animate the battle between player and computer moves"""
        # Starting positions
        player_x, player_y = 200, 200
        computer_x, computer_y = 600, 200
        
        # Create move representations
        self.game_area.create_text(player_x, player_y - 50, 
                                  text=player_choice.title(),
                                  fill='white',
                                  font=('Montserrat', 16))
        self.game_area.create_text(computer_x, computer_y - 50, 
                                  text=computer_choice.title(),
                                  fill='white',
                                  font=('Montserrat', 16))
        
        # Show outcome
        result_text = "It's a tie!"
        if outcome == 'win':
            result_text = "You win!"
        elif outcome == 'lose':
            result_text = "Computer wins!"
        
        self.game_area.create_text(400, 100,
                                  text=result_text,
                                  fill='white',
                                  font=('Montserrat', 24, 'bold'))
        
        # Add move description if available
        move_desc = self.game_logic.get_move_description(player_choice, computer_choice)
        if move_desc:
            self.game_area.create_text(400, 150,
                                      text=move_desc,
                                      fill='white',
                                      font=('Montserrat', 16))

def launch_gui():
    app = ModernRPSGame()
    app.root.mainloop()