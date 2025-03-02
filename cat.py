import tkinter as tk
import requests
import json
import logging

class CatFactApp:
    def __init__(self, root):
        logging.basicConfig(
            filename='logs.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)
        
        self.root = root
        self.load_settings()
        self.setup_window()
        self.create_widgets()
        
    def load_settings(self):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
            self.logger.info("Successfully loaded settings.json")
        except FileNotFoundError:
            self.logger.error("File settings.json not found!")
            exit(1)
        except json.JSONDecodeError:
            self.logger.error("Error while parsing settings.json")
            exit(1)
            
    def setup_window(self):
        window = self.settings['window']
        colors = self.settings['colors']
        
        self.root.title(window['title'])
        self.root.geometry(f"{window['width']}x{window['height']}")
        self.root.configure(bg=colors['background'])
        self.root.resizable(window['resizable'], window['resizable'])
        self.logger.info("Window setup successfully")
        
    def create_widgets(self):
        colors = self.settings['colors']
        fonts = self.settings['fonts']
        padding = self.settings['padding']
        
        title_label = tk.Label(
            self.root,
            text="🐱 Cat Facts",
            font=fonts['title'],
            bg=colors['background'],
            fg=colors['text']
        )
        title_label.pack(pady=padding['title'])
        self.fact_frame = tk.Frame(
            self.root,
            bg=colors['accent'],
            bd=2,
            relief="flat"
        )
        self.fact_frame.pack(
            pady=padding['fact_frame'],
            padx=padding['fact_frame'],
            fill="both",
            expand=True
        )
        self.fact_label = tk.Label(
            self.fact_frame,
            text="Press the button to get a cat fact!",
            font=fonts['fact'],
            bg=colors['accent'],
            fg=colors['text'],
            wraplength=self.settings['window']['width'] - 70,
            justify="center",
            pady=20,
            padx=20
        )
        self.fact_label.pack(expand=True)

        generate_button = tk.Button(
            self.root,
            text="Get Fact",
            command=self.get_cat_fact,
            bg=colors['button'],
            fg=colors['text'],
            font=fonts['button'],
            bd=0,
            activebackground=colors['button_hover'],
            activeforeground=colors['text'],
            padx=20,
            pady=10
        )
        generate_button.pack(pady=padding['button'])

        quit_button = tk.Button(
            self.root,
            text="Exit",
            command=self.root.quit,
            bg=colors['accent'],
            fg=colors['text'],
            font=fonts['quit_button'],
            bd=0,
            activebackground=colors['button'],
            activeforeground=colors['text'],
            padx=15,
            pady=5
        )
        quit_button.pack(pady=padding['quit_button'])
        
        self.logger.info("App widgets created successfully")
        
    def get_cat_fact(self):
        try:
            response = requests.get(self.settings['api']['url'])
            if response.status_code == 200:
                fact = response.json()["fact"]
                self.fact_label.config(text=fact)
            else:
                self.fact_label.config(text="😿 Unable to get fact, try again later!")
                self.logger.warning(f"Failed to get response: {response.status_code}")
        except requests.RequestException as e:
            self.fact_label.config(text="😿 Something's gone wrong. Check the Internet!")
            self.logger.error(f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = CatFactApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()