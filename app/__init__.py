import json
import os
from datetime import date

from flask import Flask, Response, render_template


def create_app():
    app = Flask(__name__)

    # Define paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Go up one level from 'app/' to find the JSON files
    DATA_FILE = os.path.join(BASE_DIR, "..", "cv_data.json")
    SECRETS_FILE = os.path.join(BASE_DIR, "..", "secrets.json")

    def load_data():
        # 1. Load the Public Base Data
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 2. Check for Private Overrides (Local Dev Only)
        if os.path.exists(SECRETS_FILE):
            # 2. Check for Private Overrides (Local Dev Only)
            try:
                with open(SECRETS_FILE, "r", encoding="utf-8") as f:
                    secrets = json.load(f)
            except FileNotFoundError:
                pass
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
                print(f"Warning: Found secrets.json but failed to load it: {e}")
            else:
                if isinstance(secrets, dict) and "phone" in secrets:
                    data["basics"]["phone"] = secrets["phone"]

            return data

    # --- Custom Filter for Dates ---
    @app.template_filter("format_date")
    def format_date(value):
        # If the value is "Present", just return it
        if value.lower() == "present":
            return value

        # Try to parse YYYY-MM-DD
        try:
            # Returns "Mon YYYY"
            date_obj = date.fromisoformat(value)
            return date_obj.strftime("%b %Y")
        except (ValueError, TypeError):
            # If it's just a year "2013" or invalid, return as-is
            return value

    # --- Orphan preventer filter ---
    @app.template_filter("prevent_orphan")
    def prevent_orphan(text):
        """
        Replaces the last space in a string with a non-breaking space (&nbsp;).
        Ensures the last word never sits alone on a new line.
        """
        if not text or not isinstance(text, str):
            return text

        # Split by spaces, starting from the right, max 1 split
        parts = text.rsplit(" ", 1)

        # If there's less than 2 words, return as is
        if len(parts) < 2:
            return text

        # Rejoin with a Non-Breaking Space (\u00A0)
        return f"{parts[0]}\u00a0{parts[1]}"

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        response.headers["Content-Security-Policy"] = (
            "frame-ancestors 'none'; object-src 'none'; base-uri 'self'"
        )
        return response

    @app.route("/")
    def index():
        cv = load_data()
        return render_template("index.html", cv=cv)

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    @app.route("/robots.txt")
    def robots_txt():
        content = "User-agent: *\nAllow: /\nSitemap: https://dundua.dev/sitemap.xml\n"
        return Response(content, mimetype="text/plain")

    @app.route("/sitemap.xml")
    def sitemap():
        content = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://dundua.dev/</loc>
        </url>
    </urlset>
    """
        return Response(content, mimetype="application/xml")

    return app
