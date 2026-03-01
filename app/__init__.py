from datetime import datetime
import os
import json
from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # Define paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Go up one level from 'app/' to find the JSON files
    DATA_FILE = os.path.join(BASE_DIR, '..', 'cv_data.json')
    SECRETS_FILE = os.path.join(BASE_DIR, '..', 'secrets.json')

    def load_data():
        # 1. Load the Public Base Data
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 2. Check for Private Overrides (Local Dev Only)
        if os.path.exists(SECRETS_FILE):
            try:
                with open(SECRETS_FILE, 'r', encoding='utf-8') as f:
                    secrets = json.load(f)
                    
                    # Apply overrides
                    # We check if keys exist to avoid crashing on empty secrets file
                    if 'phone' in secrets:
                        data['basics']['phone'] = secrets['phone']
                    
                    # Add more overrides here later (e.g. specific address)
            except Exception as e:
                print(f"Warning: Found secrets.json but failed to load it: {e}")
                
        return data
    
    # --- Custom Filter for Dates ---
    @app.template_filter('format_date')
    def format_date(value):
        # If the value is "Present", just return it
        if value.lower() == 'present':
            return value
        
        # Try to parse YYYY-MM-DD
        try:
            # Returns "Mon YYYY"
            date_obj = datetime.strptime(value, '%Y-%m-%d')
            return date_obj.strftime('%b %Y') 
        except (ValueError, TypeError):
            # If it's just a year "2013" or invalid, return as-is
            return value
        
    # --- Orphan preventer filter ---
    @app.template_filter('prevent_orphan')
    def prevent_orphan(text):
        """
        Replaces the last space in a string with a non-breaking space (&nbsp;).
        Ensures the last word never sits alone on a new line.
        """
        if not text or not isinstance(text, str):
            return text
        
        # Split by spaces, starting from the right, max 1 split
        parts = text.rsplit(' ', 1)
        
        # If there's less than 2 words, return as is
        if len(parts) < 2:
            return text
        
        # Rejoin with a Non-Breaking Space (\u00A0)
        return f"{parts[0]}\u00A0{parts[1]}"

    @app.route('/')
    def index():
        cv = load_data()
        return render_template('index.html', cv=cv)

    @app.route('/health')
    def health():
        return {"status": "ok"}, 200

    return app