import streamlit as st
import requests
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from bs4 import BeautifulSoup
import random
import time
import json

# --- CONFIG ---
GENIUS_ACCESS_TOKEN = "YQkWoMNacdeC9oX7Uf1m-qkKULs5a8mUI700Kq7ZmFrXA_NRsW6B3Gee59NjwAeQ"

# Era-specific configuration with enhanced themes
ERA_CONFIG = {
    "Debut": {
        "color": "#228B22",  # Forest green
        "font": "Montserrat",
        "background": "linear-gradient(135deg, #90EE90 0%, #228B22 100%)",
        "animation": "butterflies",
        "icon": "🤠",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%23228B22\" d=\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z\"/></svg>'), auto",
        "songs": ["Our Song", "Tim McGraw", "Teardrops on My Guitar", "Picture to Burn"]
    },
    "Fearless": {
        "color": "#DAA520",  # Goldenrod
        "font": "Poppins",
        "background": "linear-gradient(135deg, #FFD700 0%, #DAA520 100%)",
        "animation": "glitter",
        "icon": "🎸",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%23DAA520\" d=\"M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z\"/></svg>'), auto",
        "songs": ["Fearless", "You Belong With Me", "Love Story", "Fifteen", "White Horse"]
    },
    "Speak Now": {
        "color": "#8A2BE2",  # Blue violet
        "font": "Roboto",
        "background": "linear-gradient(135deg, #DDA0DD 0%, #8A2BE2 100%)",
        "animation": "lanterns",
        "icon": "⭐",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%238A2BE2\" d=\"M12 2L13.09 8.26L20 9l-5.5 5.39L15.18 21L12 17.77L8.82 21L9.5 14.39L4 9l6.91-.74L12 2z\"/></svg>'), auto",
        "songs": ["Enchanted", "Long Live", "Mine", "Back to December", "Mean"]
    },
    "Red": {
        "color": "#DC143C",  # Crimson red
        "font": "Open Sans",
        "background": "linear-gradient(135deg, #FF6347 0%, #DC143C 100%)",
        "animation": "leaves",
        "icon": "🧣",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%23DC143C\" d=\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z\"/></svg>'), auto",
        "songs": ["22", "We Are Never Ever Getting Back Together", "I Knew You Were Trouble", "All Too Well", "Red"]
    },
    "1989": {
        "color": "#4169E1",  # Royal blue
        "font": "Lato",
        "background": "linear-gradient(135deg, #87CEEB 0%, #4169E1 100%)",
        "animation": "polaroid",
        "icon": "🏙️",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%234169E1\" d=\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z\"/></svg>'), auto",
        "songs": ["Style", "Blank Space", "Shake It Off", "Wildest Dreams", "Bad Blood", "Out of the Woods"]
    },
    "Reputation": {
        "color": "#2F2F2F",  # Dark gray
        "font": "Inter",
        "background": "linear-gradient(135deg, #4A4A4A 0%, #2F2F2F 100%)",
        "animation": "static",
        "icon": "🐍",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%232F2F2F\" d=\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z\"/></svg>'), auto",
        "songs": ["Ready For It", "Delicate", "Don't Blame Me", "Look What You Made Me Do", "Getaway Car"]
    },
    "Lover": {
        "color": "#FF69B4",  # Hot pink
        "font": "Nunito",
        "background": "linear-gradient(135deg, #FFB6C1 0%, #FF69B4 100%)",
        "animation": "hearts",
        "icon": "🌈",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%23FF69B4\" d=\"M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z\"/></svg>'), auto",
        "songs": ["Cruel Summer", "Lover", "The Man", "You Need to Calm Down", "The Archer", "Miss Americana"]
    },
    "Folklore": {
        "color": "#696969",  # Dim gray
        "font": "Source Sans Pro",
        "background": "linear-gradient(135deg, #C0C0C0 0%, #696969 100%)",
        "animation": "raindrops",
        "icon": "🌲",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%23696969\" d=\"M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z\"/></svg>'), auto",
        "songs": ["The 1", "Betty", "The Last Great American Dynasty", "August", "Illicit Affairs", "Cardigan"]
    },
    "Evermore": {
        "color": "#CD853F",  # Peru (rust/orange)
        "font": "Ubuntu",
        "background": "linear-gradient(135deg, #DEB887 0%, #CD853F 100%)",
        "animation": "snowfall",
        "icon": "❄️",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%23CD853F\" d=\"M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z\"/></svg>'), auto",
        "songs": ["Willow", "Champagne Problems", "Tolerate It", "Marjorie", "Tis the Damn Season"]
    },
    "Midnights": {
        "color": "#191970",  # Midnight blue
        "font": "Raleway",
        "background": "linear-gradient(135deg, #4169E1 0%, #191970 100%)",
        "animation": "stars",
        "icon": "⭐",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%23191970\" d=\"M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z\"/></svg>'), auto",
        "songs": ["Lavender Haze", "Anti-Hero", "Midnight Rain", "Vigilante Shit", "Bejeweled", "Karma"]
    },
    "TTPD": {
        "color": "#8B0000",  # Dark red
        "font": "Work Sans",
        "background": "linear-gradient(135deg, #800020 0%, #8B0000 100%)",
        "animation": "typewriter",
        "icon": "✒️",
        "cursor": "url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path fill=\"%238B0000\" d=\"M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z\"/></svg>'), auto",
        "songs": ["Fortnight", "The Tortured Poets Department", "The Black Dog", "But Daddy I Love Him", "So Long London"]
    }
}

TAYLOR_QUOTES = [
    "You are not the opinion of someone who doesn't know you.",
    "Long live all the magic we made.",
    "Just because something is over doesn't mean it wasn't incredible.",
    "I've never been shy about my songwriting.",
    "We are too busy dancing to get knocked off our feet.",
    "I remember it all too well.",
    "Love is a ruthless game unless you play it good and right."
]

# Swiftie annotations for popular lyrics
SWIFTIE_ANNOTATIONS = {
    "all too well": "This line references the red scarf and the relationship with Jake Gyllenhaal",
    "cruel summer": "The 'summer' refers to the summer of 2019 when Taylor was dating Joe Alwyn",
    "love story": "Inspired by Romeo and Juliet, but with a happy ending",
    "blank space": "A satirical take on how the media portrays Taylor's dating life",
    "shake it off": "Taylor's response to haters and criticism",
    "cardigan": "The cardigan represents comfort and nostalgia in the Folklore universe",
    "anti-hero": "Taylor's most personal song about her insecurities and self-doubt"
}

def get_era_for_song(song_title):
    """Determine which era a song belongs to"""
    song_title_lower = song_title.lower()
    for era, config in ERA_CONFIG.items():
        for song in config["songs"]:
            if song.lower() in song_title_lower or song_title_lower in song.lower():
                return era
    return "Lover"  # Default era

def generate_hashtags(song_title, era):
    """Generate hashtags for social media sharing"""
    base_hashtags = [f"#{song_title.replace(' ', '')}", f"#{era}Era", "#TaylorSwift", "#Swiftie"]
    
    era_specific = {
        "Debut": ["#CountryTaylor", "#TimMcGraw"],
        "Fearless": ["#FearlessEra", "#LoveStory"],
        "Speak Now": ["#SpeakNow", "#Enchanted"],
        "Red": ["#RedEra", "#AllTooWell"],
        "1989": ["#1989Era", "#PopTaylor"],
        "Reputation": ["#ReputationEra", "#SnakeTaylor"],
        "Lover": ["#LoverEra", "#CruelSummer"],
        "Folklore": ["#FolkloreEra", "#Cardigan"],
        "Evermore": ["#EvermoreEra", "#Willow"],
        "Midnights": ["#MidnightsEra", "#AntiHero"],
        "TTPD": ["#TTPDEra", "#Fortnight"]
    }
    
    return base_hashtags + era_specific.get(era, [])

def get_era_styles(era):
    """Get CSS styles for a specific era with animations"""
    config = ERA_CONFIG.get(era, ERA_CONFIG["Lover"])
    return f"""
    .era-lyrics-{era.lower().replace(' ', '-')} {{
        background: linear-gradient(135deg, {config['color']}20 0%, {config['color']}30 100%);
        border-left: 6px solid {config['color']};
        border-radius: 16px;
        padding: 2em;
        margin: 1.5em 0;
        font-size: 1.2rem;
        color: #1a1a1a;
        font-family: '{config['font']}', sans-serif;
        white-space: pre-line;
        box-shadow: 0 8px 32px {config['color']}40, 0 4px 16px rgba(0,0,0,0.1);
        transform: translateY(0);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }}
    .era-lyrics-{era.lower().replace(' ', '-')}:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px {config['color']}50, 0 6px 20px rgba(0,0,0,0.15);
    }}
    .era-lyrics-{era.lower().replace(' ', '-')}:hover::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="{config['color']}" opacity="0.6"><animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite"/></circle><circle cx="80" cy="30" r="1.5" fill="{config['color']}" opacity="0.4"><animate attributeName="opacity" values="0.4;0;0.4" dur="1.5s" repeatCount="indefinite"/></circle><circle cx="40" cy="80" r="1" fill="{config['color']}" opacity="0.8"><animate attributeName="opacity" values="0.8;0;0.8" dur="3s" repeatCount="indefinite"/></circle></svg>');
        pointer-events: none;
        z-index: 1;
    }}
    .era-header-{era.lower().replace(' ', '-')} {{
        font-family: '{config['font']}', sans-serif;
        color: {config['color']};
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: bold;
        position: relative;
    }}
    .era-header-{era.lower().replace(' ', '-')}::before {{
        content: '{config['icon']}';
        position: absolute;
        left: -50px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
    }}
    .era-header-{era.lower().replace(' ', '-')}::after {{
        content: '{config['icon']}';
        position: absolute;
        right: -50px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        animation: float 3s ease-in-out infinite reverse;
    }}
    """

# --- PAGE STYLE ---
st.set_page_config(page_title="Taylor Swift Lyrics & Word Cloud", page_icon="🎤", layout="wide")

# Generate all era styles
all_era_styles = "\n".join([get_era_styles(era) for era in ERA_CONFIG.keys()])

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Poppins:wght@400;600;700&family=Roboto:wght@400;500;700&family=Open+Sans:wght@400;600;700&family=Lato:wght@400;700&family=Inter:wght@400;600;700&family=Nunito:wght@400;600;700&family=Source+Sans+Pro:wght@400;600;700&family=Ubuntu:wght@400;500;700&family=Raleway:wght@400;600;700&family=Work+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
        background: #1e1e2e;
        min-height: 100vh;
        color: #ffffff;
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="%23FF69B4" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>'), auto;
    }}
    
    .main-header {{
        font-family: 'Montserrat', sans-serif;
        font-size: 4rem;
        color: #FF69B4;
        text-align: center;
        margin-bottom: 1em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-weight: bold;
        letter-spacing: 2px;
        animation: glow 2s ease-in-out infinite alternate;
        position: relative;
    }}
    
    .main-header::before {{
        content: '🎤';
        position: absolute;
        left: -60px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 3rem;
        animation: bounce 2s ease-in-out infinite;
    }}
    
    .main-header::after {{
        content: '🎵';
        position: absolute;
        right: -60px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 3rem;
        animation: bounce 2s ease-in-out infinite reverse;
    }}
    
    @keyframes glow {{
        from {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.5), 0 0 20px #FF69B4; }}
        to {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.5), 0 0 30px #9370DB, 0 0 40px #FFD700; }}
    }}
    
    @keyframes bounce {{
        0%, 20%, 50%, 80%, 100% {{ transform: translateY(-50%); }}
        40% {{ transform: translateY(-60%); }}
        60% {{ transform: translateY(-55%); }}
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(-50%) translateX(0); }}
        50% {{ transform: translateY(-50%) translateX(10px); }}
    }}
    
    .quote {{
        font-family: 'Poppins', sans-serif;
        color: #FFD700;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 2em;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        background: rgba(255,255,255,0.1);
        padding: 1.5em;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        font-weight: 600;
        position: relative;
        overflow: hidden;
    }}
    
    .quote::before {{
        content: '"';
        position: absolute;
        left: 20px;
        top: 10px;
        font-size: 4rem;
        color: rgba(255,215,0,0.3);
        font-family: serif;
    }}
    
    .quote::after {{
        content: '"';
        position: absolute;
        right: 20px;
        bottom: 10px;
        font-size: 4rem;
        color: rgba(255,215,0,0.3);
        font-family: serif;
    }}
    
    .stButton > button {{
        background: linear-gradient(45deg, #FF69B4, #9370DB);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 1em 2.5em;
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 1em;
        margin-bottom: 1.5em;
        box-shadow: 0 8px 25px rgba(147, 112, 219, 0.4);
        transform: translateY(0);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Poppins', sans-serif;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(45deg, #9370DB, #FF69B4);
        color: #fff0f6;
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(255, 105, 180, 0.5);
    }}
    
    .wordcloud-container {{
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 2em;
        margin: 2em 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
    }}
    
    .wordcloud-container::before {{
        content: '☁️';
        position: absolute;
        top: -10px;
        left: 20px;
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
    }}
    
    .footer {{
        text-align: center;
        color: #FFD700;
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        margin-top: 3em;
        padding: 2em;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        font-weight: 600;
        position: relative;
    }}
    
    .footer::after {{
        content: 'Featured by Genius API';
        position: absolute;
        bottom: 10px;
        right: 20px;
        font-size: 0.8rem;
        color: rgba(255,215,0,0.7);
        font-style: italic;
    }}
    
    .stTextInput > div > div > input {{
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        border: 2px solid rgba(147, 112, 219, 0.3);
        padding: 1em;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        color: #1a1a1a;
        font-family: 'Poppins', sans-serif;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #9370DB;
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.3);
    }}
    
    .stExpander {{
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 0.5em 0;
        transition: all 0.3s ease;
    }}
    
    .stExpander:hover {{
        background: rgba(255,255,255,0.15);
        transform: translateX(5px);
    }}
    
    .stExpander > div > div {{
        background: transparent !important;
    }}
    
    .stExpander > div > div > div {{
        background: transparent !important;
    }}
    
    .stSidebar {{
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.15) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.3);
        box-shadow: 2px 0 20px rgba(0,0,0,0.2);
    }}
    
    .stSidebar > div > div > div {{
        background: transparent !important;
    }}
    
    .stMarkdown {{
        color: #ffffff;
    }}
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }}
    
    .hashtags {{
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1em;
        margin: 1em 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    .hashtag {{
        display: inline-block;
        background: linear-gradient(45deg, #FF69B4, #9370DB);
        color: white;
        padding: 0.3em 0.8em;
        margin: 0.2em;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .hashtag:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
    }}
    
    .vinyl-player {{
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: linear-gradient(45deg, #000, #333);
        margin: 2em auto;
        position: relative;
        animation: spin 3s linear infinite;
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
    }}
    
    .vinyl-player::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 20px;
        height: 20px;
        background: #FFD700;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(255,215,0,0.5);
    }}
    
    @keyframes spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    .countdown {{
        font-size: 2rem;
        color: #FF69B4;
        text-align: center;
        margin: 1em 0;
        font-weight: bold;
        animation: pulse 1s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
    }}
    
    .annotation {{
        background: rgba(255,215,0,0.1);
        border-left: 3px solid #FFD700;
        padding: 0.5em 1em;
        margin: 0.5em 0;
        border-radius: 5px;
        font-size: 0.9rem;
        font-style: italic;
        color: #FFD700;
    }}
    
    {all_era_styles}
    </style>
""", unsafe_allow_html=True)

# --- GENIUS API HELPERS ---
def search_genius_song(song_title, artist="Taylor Swift"):
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    params = {"q": f"{song_title} {artist}"}
    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        return None
    data = r.json()
    hits = data.get("response", {}).get("hits", [])
    for hit in hits:
        if artist.lower() in hit["result"]["primary_artist"]["name"].lower():
            return hit["result"]["url"]
    if hits:
        return hits[0]["result"]["url"]
    return None

def scrape_lyrics_from_url(url):
    page = requests.get(url)
    if page.status_code != 200:
        return None
    soup = BeautifulSoup(page.content, "html.parser")
    lyrics = ""
    
    # Try multiple selectors for lyrics
    lyrics_selectors = [
        "div[data-lyrics-container='true']",
        "div.lyrics",
        "div[class*='lyrics']",
        "div[class*='Lyrics']",
        ".SongPageGriddesktop__LyricsWrapper-sc-1px5b71-1"
    ]
    
    for selector in lyrics_selectors:
        lyrics_elements = soup.select(selector)
        if lyrics_elements:
            for element in lyrics_elements:
                # Remove any "Read More" sections and other unwanted elements
                for unwanted in element.find_all(text=re.compile(r'Read More|Contributors|Translations|한국어|Türkçe|Español|srpski|Português|Polski|Italiano|Magyar|Deutsch|Français|فارسی|简体中文|繁體中文|Русский|Беларуская|العربية|Українська|Svenska|ไทย|Česky|Català|日本語|Română', re.IGNORECASE)):
                    if unwanted.parent:
                        unwanted.parent.decompose()
                
                text = element.get_text(separator="\n")
                # Clean up the text
                text = re.sub(r'Read More.*', '', text, flags=re.IGNORECASE)
                text = re.sub(r'Contributors.*', '', text, flags=re.IGNORECASE)
                text = re.sub(r'Translations.*', '', text, flags=re.IGNORECASE)
                text = re.sub(r'[0-9]+ Contributors.*', '', text, flags=re.IGNORECASE)
                text = re.sub(r'한국어.*|Türkçe.*|Español.*|srpski.*|Português.*|Polski.*|Italiano.*|Magyar.*|Deutsch.*|Français.*|فارسی.*|简体中文.*|繁體中文.*|Русский.*|Беларуская.*|العربية.*|Українська.*|Svenska.*|ไทย.*|Česky.*|Català.*|日本語.*|Română.*', '', text, flags=re.IGNORECASE)
                
                if text.strip():
                    lyrics += text + "\n"
    
    return lyrics.strip() if lyrics else None

def get_lyrics(song_title):
    url = search_genius_song(song_title)
    if not url:
        return None, "Song not found on Genius. Please check the title."
    lyrics = scrape_lyrics_from_url(url)
    if not lyrics:
        return None, "Lyrics not found or not available for this song."
    return lyrics, None

def create_wordcloud(text, era_color):
    text = re.sub(r'[^\w\s]', '', text.lower())
    stop_words = set([w.strip() for w in '''the a an and or but in on at to for of with by i you he she it we they me him her us them my your his its our their mine yours hers ours theirs this that these those am is are was were be been being have has had do does did will would could should may might must can oh yeah baby just like got get gonna wanna cause chorus verse bridge intro outro repeat x2 x3 x4'''.split()])
    
    # Create custom colormap based on era color
    wordcloud = WordCloud(
        width=800, height=400, 
        background_color='white', 
        colormap='plasma', 
        max_words=100,
        stopwords=stop_words, 
        random_state=42
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
    buf.seek(0)
    plt.close()
    return buf

def add_annotations_to_lyrics(lyrics, song_title):
    """Add Swiftie annotations to lyrics"""
    annotated_lyrics = lyrics
    for key, annotation in SWIFTIE_ANNOTATIONS.items():
        if key in song_title.lower():
            # Find lines that might have annotations
            lines = lyrics.split('\n')
            for i, line in enumerate(lines):
                if any(word in line.lower() for word in key.split()):
                    lines[i] = f"{line}\n<div class='annotation'>💜 Swiftie Note: {annotation}</div>"
            annotated_lyrics = '\n'.join(lines)
            break
    return annotated_lyrics

def main():
    # 13-second countdown loader (Taylor's lucky number)
    if 'countdown' not in st.session_state:
        st.session_state.countdown = 13
    
    if st.session_state.countdown > 0:
        st.markdown(f'<div class="countdown">🎵 Loading in {st.session_state.countdown}... 🎵</div>', unsafe_allow_html=True)
        st.session_state.countdown -= 1
        st.rerun()
    
    st.markdown('<div class="main-header">Taylor Swift Lyrics & Word Cloud</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="quote">{random.choice(TAYLOR_QUOTES)}</div>', unsafe_allow_html=True)
    
    # Sidebar with era information
    st.sidebar.markdown("## 💜 About This App")
    st.sidebar.info("""
    - Enter a Taylor Swift song title
    - Get real lyrics from Genius
    - See era-specific theming
    - Enjoy Swiftie quotes and word clouds
    - Interactive features and animations
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🎵 Popular Songs by Era:**")
    
    # Group songs by era in sidebar
    for era, config in ERA_CONFIG.items():
        with st.sidebar.expander(f"{config['icon']} {era}"):
            for song in config["songs"][:3]:  # Show first 3 songs per era
                if st.button(f"🎵 {song}", key=f"sidebar_{song}"):
                    st.session_state["song_input"] = song
                    st.rerun()
    
    song_title = st.text_input("Enter a Taylor Swift song title:", key="song_input", placeholder="e.g., Love Story, Cruel Summer, ...")
    
    if st.button("Get Lyrics & Word Cloud", type="primary"):
        if song_title:
            with st.spinner("Fetching lyrics and generating word cloud..."):
                lyrics, error = get_lyrics(song_title)
                if lyrics:
                    # Determine era and apply styling
                    era = get_era_for_song(song_title)
                    era_class = era.lower().replace(' ', '-')
                    
                    # Display era header
                    st.markdown(f'<div class="era-header-{era_class}">🎵 {song_title} • {era} Era</div>', unsafe_allow_html=True)
                    
                    # Add annotations to lyrics
                    annotated_lyrics = add_annotations_to_lyrics(lyrics, song_title)
                    
                    # Display lyrics with era-specific styling
                    st.markdown(f'<div class="era-lyrics-{era_class}">' + annotated_lyrics.replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
                    
                    # Generate hashtags
                    hashtags = generate_hashtags(song_title, era)
                    st.markdown("### 📱 Share on Social Media")
                    hashtag_html = '<div class="hashtags">'
                    for hashtag in hashtags:
                        hashtag_html += f'<span class="hashtag">{hashtag}</span>'
                    hashtag_html += '</div>'
                    st.markdown(hashtag_html, unsafe_allow_html=True)
                    
                    # Vinyl record player animation
                    st.markdown("### 🎵 Now Playing")
                    st.markdown('<div class="vinyl-player"></div>', unsafe_allow_html=True)
                    
                    # Generate word cloud
                    st.markdown("### ☁️ Word Cloud")
                    img = create_wordcloud(lyrics, ERA_CONFIG[era]["color"])
                    st.image(img, use_container_width=True)
                    
                    # Era info
                    st.info(f"🎤 **{era} Era**: {ERA_CONFIG[era]['font']} font • {ERA_CONFIG[era]['color']} theme • {ERA_CONFIG[era]['animation']} animation")
                else:
                    st.error(error)
        else:
            st.warning("Please enter a song title!")
    
    st.markdown('<div class="footer">🎵 Built with ❤️ for Swifties | Powered by Streamlit & Genius API</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()