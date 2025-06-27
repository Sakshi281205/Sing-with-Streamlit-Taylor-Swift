import streamlit as st
import requests
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from bs4 import BeautifulSoup, Tag
import random
import time
import json
import webbrowser
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- CONFIG ---
GENIUS_ACCESS_TOKEN = "jtXbVxgBORC18-9tON29Spr3xjQwOsSUae66_RPK6LEK0MIoGaSb8kij04Phji6M"
SPOTIFY_CLIENT_ID = "t6YNtBA8R5l2VuOA_dC8pGKZTWsMATafMFyJLW91ZRX2Umz6AGwtT0ZTrE-hLnjF"
SPOTIFY_CLIENT_SECRET = "gQVv9QSFpbKgBiihiDR0INInQG3tKeoSbsVoz7GNJ2O0N9kgmzObLO25vW_aYN4H8BjdUKNYYhnDAJ6I9j8qoQ"
SPOTIFY_REDIRECT_URI = "http://localhost"

# Function to get Spotify preview URL and track link
def get_spotify_preview_url(song_title, artist="Taylor Swift"):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))
        results = sp.search(q=f"track:{song_title} artist:{artist}", type="track", limit=1)
        tracks = results.get("tracks", {}).get("items", [])
        if tracks:
            return tracks[0].get("preview_url"), tracks[0].get("external_urls", {}).get("spotify")
        return None, None
    except Exception as e:
        st.warning(f"Spotify preview unavailable: {e}")
        return None, None

# Era-specific configuration with enhanced themes
ERA_CONFIG = {
    "Debut": {
        "color": "#228B22",  # Forest green
        "font": "Montserrat",
        "background": "linear-gradient(135deg, #e8f5e8 0%, #228B22 100%)",
        "animation": "butterflies",
        "icon": "🤠",
        "songs": ["Our Song", "Tim McGraw", "Teardrops on My Guitar", "Picture to Burn"],
        "facts": ["Taylor's debut album was released when she was just 16", "The album was recorded in Nashville, Tennessee", "Tim McGraw was the first single released"]
    },
    "Fearless": {
        "color": "#DAA520",  # Goldenrod
        "font": "Poppins",
        "background": "linear-gradient(135deg, #fff8dc 0%, #DAA520 100%)",
        "animation": "glitter",
        "icon": "🎸",
        "songs": ["Fearless", "You Belong With Me", "Love Story", "Fifteen", "White Horse"],
        "facts": ["Fearless won Album of the Year at the 2010 Grammys", "Love Story was inspired by Romeo and Juliet", "The album sold over 12 million copies worldwide"]
    },
    "Speak Now": {
        "color": "#8A2BE2",  # Blue violet
        "font": "Roboto",
        "background": "linear-gradient(135deg, #f0e6ff 0%, #8A2BE2 100%)",
        "animation": "lanterns",
        "icon": "⭐",
        "songs": ["Enchanted", "Long Live", "Mine", "Back to December", "Mean"],
        "facts": ["Taylor wrote every song on Speak Now by herself", "The album was recorded in secret", "Enchanted was written about Adam Young from Owl City"]
    },
    "Red": {
        "color": "#DC143C",  # Crimson red
        "font": "Open Sans",
        "background": "linear-gradient(135deg, #ffe6e6 0%, #DC143C 100%)",
        "animation": "leaves",
        "icon": "🧣",
        "songs": ["22", "We Are Never Ever Getting Back Together", "I Knew You Were Trouble", "All Too Well", "Red"],
        "facts": ["All Too Well is considered one of Taylor's best songs", "The red scarf became a famous Swiftie symbol", "The album marked Taylor's transition to pop music"]
    },
    "1989": {
        "color": "#4169E1",  # Royal blue
        "font": "Lato",
        "background": "linear-gradient(135deg, #e6f3ff 0%, #4169E1 100%)",
        "animation": "polaroid",
        "icon": "🏙️",
        "songs": ["Style", "Blank Space", "Shake It Off", "Wildest Dreams", "Bad Blood", "Out of the Woods"],
        "facts": ["1989 was Taylor's first full pop album", "The album was named after her birth year", "Shake It Off became a global anthem"]
    },
    "Reputation": {
        "color": "#2F2F2F",  # Dark gray
        "font": "Inter",
        "background": "linear-gradient(135deg, #f5f5f5 0%, #2F2F2F 100%)",
        "animation": "static",
        "icon": "🐍",
        "songs": ["Ready For It", "Delicate", "Don't Blame Me", "Look What You Made Me Do", "Getaway Car"],
        "facts": ["Reputation was Taylor's response to media scrutiny", "The snake imagery became iconic", "The album was released after a year of silence"]
    },
    "Lover": {
        "color": "#FF69B4",  # Hot pink
        "font": "Nunito",
        "background": "linear-gradient(135deg, #ffe6f2 0%, #FF69B4 100%)",
        "animation": "hearts",
        "icon": "🌈",
        "songs": ["Cruel Summer", "Lover", "The Man", "You Need to Calm Down", "The Archer", "Miss Americana"],
        "facts": ["Lover was inspired by Taylor's relationship with Joe Alwyn", "The album celebrates love in all forms", "Cruel Summer was written about the summer of 2019"]
    },
    "Folklore": {
        "color": "#696969",  # Dim gray
        "font": "Source Sans Pro",
        "background": "linear-gradient(135deg, #f8f8f8 0%, #696969 100%)",
        "animation": "raindrops",
        "icon": "🌲",
        "songs": ["The 1", "Betty", "The Last Great American Dynasty", "August", "Illicit Affairs", "Cardigan"],
        "facts": ["Folklore was written and recorded during quarantine", "The album tells fictional stories", "Cardigan was the lead single"]
    },
    "Evermore": {
        "color": "#CD853F",  # Peru (rust/orange)
        "font": "Ubuntu",
        "background": "linear-gradient(135deg, #fff8f0 0%, #CD853F 100%)",
        "animation": "snowfall",
        "icon": "❄️",
        "songs": ["Willow", "Champagne Problems", "Tolerate It", "Marjorie", "Tis the Damn Season"],
        "facts": ["Evermore is the sister album to Folklore", "The album was a surprise release", "Willow was the lead single"]
    },
    "Midnights": {
        "color": "#191970",  # Midnight blue
        "font": "Raleway",
        "background": "linear-gradient(135deg, #e6e6fa 0%, #191970 100%)",
        "animation": "stars",
        "icon": "⭐",
        "songs": ["Lavender Haze", "Anti-Hero", "Midnight Rain", "Vigilante Shit", "Bejeweled", "Karma"],
        "facts": ["Midnights explores 13 sleepless nights", "Anti-Hero became Taylor's biggest hit", "The album was inspired by sleepless nights"]
    },
    "TTPD": {
        "color": "#8B0000",  # Dark red
        "font": "Work Sans",
        "background": "linear-gradient(135deg, #ffe6e6 0%, #8B0000 100%)",
        "animation": "typewriter",
        "icon": "✒️",
        "songs": ["Fortnight", "The Tortured Poets Department", "The Black Dog", "But Daddy I Love Him", "So Long London"],
        "facts": ["TTPD is Taylor's 11th studio album", "The album explores themes of heartbreak and poetry", "Fortnight features Post Malone"]
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

# Taylor Swift song list (expanded)
SONG_LIST = [
    {"Song": "Tim McGraw", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Liz Rose", "Album": "Taylor Swift", "Year": 2006},
    {"Song": "Teardrops on My Guitar", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Liz Rose", "Album": "Taylor Swift", "Year": 2006},
    {"Song": "Our Song", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Taylor Swift", "Year": 2006},
    {"Song": "Picture to Burn", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Liz Rose", "Album": "Taylor Swift", "Year": 2006},
    {"Song": "Should've Said No", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Taylor Swift", "Year": 2006},
    {"Song": "Love Story", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Fearless", "Year": 2008},
    {"Song": "You Belong with Me", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Liz Rose", "Album": "Fearless", "Year": 2008},
    {"Song": "Fifteen", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Fearless", "Year": 2008},
    {"Song": "Fearless", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Liz Rose, Hillary Lindsey", "Album": "Fearless", "Year": 2008},
    {"Song": "White Horse", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Liz Rose", "Album": "Fearless", "Year": 2008},
    {"Song": "Hey Stephen", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Fearless", "Year": 2008},
    {"Song": "Forever & Always", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Fearless", "Year": 2008},
    {"Song": "Change", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Fearless", "Year": 2008},
    {"Song": "Enchanted", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Speak Now", "Year": 2010},
    {"Song": "Mine", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Speak Now", "Year": 2010},
    {"Song": "Back to December", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Speak Now", "Year": 2010},
    {"Song": "Mean", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Speak Now", "Year": 2010},
    {"Song": "Long Live", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Speak Now", "Year": 2010},
    {"Song": "Sparks Fly", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Speak Now", "Year": 2010},
    {"Song": "All Too Well", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Liz Rose", "Album": "Red", "Year": 2012},
    {"Song": "22", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback", "Album": "Red", "Year": 2012},
    {"Song": "We Are Never Ever Getting Back Together", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback", "Album": "Red", "Year": 2012},
    {"Song": "I Knew You Were Trouble", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback", "Album": "Red", "Year": 2012},
    {"Song": "Red", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Dan Wilson", "Album": "Red", "Year": 2012},
    {"Song": "State of Grace", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Red", "Year": 2012},
    {"Song": "Begin Again", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Red", "Year": 2012},
    {"Song": "Blank Space", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback", "Album": "1989", "Year": 2014},
    {"Song": "Style", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback, Ali Payami", "Album": "1989", "Year": 2014},
    {"Song": "Shake It Off", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback", "Album": "1989", "Year": 2014},
    {"Song": "Wildest Dreams", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback", "Album": "1989", "Year": 2014},
    {"Song": "Bad Blood", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback", "Album": "1989", "Year": 2014},
    {"Song": "Out of the Woods", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff", "Album": "1989", "Year": 2014},
    {"Song": "Welcome to New York", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Ryan Tedder", "Album": "1989", "Year": 2014},
    {"Song": "Look What You Made Me Do", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff, Fred Fairbrass, Richard Fairbrass, Rob Manzoli", "Album": "Reputation", "Year": 2017},
    {"Song": "...Ready for It?", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback, Ali Payami", "Album": "Reputation", "Year": 2017},
    {"Song": "Delicate", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Max Martin, Shellback", "Album": "Reputation", "Year": 2017},
    {"Song": "Getaway Car", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff", "Album": "Reputation", "Year": 2017},
    {"Song": "End Game", "Artist": "Taylor Swift feat. Ed Sheeran & Future", "Writers": "Taylor Swift, Max Martin, Shellback, Ed Sheeran, Nayvadius Wilburn", "Album": "Reputation", "Year": 2017},
    {"Song": "Lover", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "Lover", "Year": 2019},
    {"Song": "Cruel Summer", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff, Annie Clark", "Album": "Lover", "Year": 2019},
    {"Song": "The Man", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Joel Little", "Album": "Lover", "Year": 2019},
    {"Song": "You Need to Calm Down", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Joel Little", "Album": "Lover", "Year": 2019},
    {"Song": "The Archer", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff", "Album": "Lover", "Year": 2019},
    {"Song": "Miss Americana & the Heartbreak Prince", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Joel Little", "Album": "Lover", "Year": 2019},
    {"Song": "Cardigan", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Aaron Dessner", "Album": "Folklore", "Year": 2020},
    {"Song": "The 1", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Aaron Dessner", "Album": "Folklore", "Year": 2020},
    {"Song": "Exile", "Artist": "Taylor Swift feat. Bon Iver", "Writers": "Taylor Swift, Justin Vernon, William Bowery", "Album": "Folklore", "Year": 2020},
    {"Song": "August", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff", "Album": "Folklore", "Year": 2020},
    {"Song": "Betty", "Artist": "Taylor Swift", "Writers": "Taylor Swift, William Bowery", "Album": "Folklore", "Year": 2020},
    {"Song": "Willow", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Aaron Dessner", "Album": "Evermore", "Year": 2020},
    {"Song": "Champagne Problems", "Artist": "Taylor Swift", "Writers": "Taylor Swift, William Bowery", "Album": "Evermore", "Year": 2020},
    {"Song": "Tolerate It", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Aaron Dessner", "Album": "Evermore", "Year": 2020},
    {"Song": "No Body, No Crime", "Artist": "Taylor Swift feat. HAIM", "Writers": "Taylor Swift", "Album": "Evermore", "Year": 2020},
    {"Song": "Coney Island", "Artist": "Taylor Swift feat. The National", "Writers": "Taylor Swift, Aaron Dessner, Bryce Dessner, William Bowery", "Album": "Evermore", "Year": 2020},
    {"Song": "Anti-Hero", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff", "Album": "Midnights", "Year": 2022},
    {"Song": "Bejeweled", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff", "Album": "Midnights", "Year": 2022},
    {"Song": "Lavender Haze", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff, Zoë Kravitz, Mark Spears, Jahaan Sweet, Sam Dew", "Album": "Midnights", "Year": 2022},
    {"Song": "Karma", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff, Mark Spears, Jahaan Sweet, Keanu Torres", "Album": "Midnights", "Year": 2022},
    {"Song": "Midnight Rain", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff", "Album": "Midnights", "Year": 2022},
    {"Song": "Fortnight", "Artist": "Taylor Swift feat. Post Malone", "Writers": "Taylor Swift, Jack Antonoff, Austin Post", "Album": "TTPD", "Year": 2024},
    {"Song": "The Tortured Poets Department", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Jack Antonoff", "Album": "TTPD", "Year": 2024},
    {"Song": "So Long, London", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Aaron Dessner", "Album": "TTPD", "Year": 2024},
    {"Song": "But Daddy I Love Him", "Artist": "Taylor Swift", "Writers": "Taylor Swift, Aaron Dessner", "Album": "TTPD", "Year": 2024},
    {"Song": "The Black Dog", "Artist": "Taylor Swift", "Writers": "Taylor Swift", "Album": "TTPD", "Year": 2024},
    # ... (add more for full discography if desired) ...
]

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
        background: linear-gradient(135deg, {config['color']}15 0%, {config['color']}25 100%);
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
        max-height: 400px;
        overflow-y: auto;
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
        background: #f8f9fa;
        min-height: 100vh;
        color: #333333;
    }}
    
    .main-header {{
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(2rem, 6vw, 4rem);
        color: #FF69B4;
        text-align: center;
        margin-bottom: 1em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: bold;
        letter-spacing: 2px;
        animation: glow 2s ease-in-out infinite alternate;
        position: relative;
        word-break: break-word;
        width: 100%;
        max-width: 100vw;
        box-sizing: border-box;
        overflow-wrap: break-word;
        white-space: normal;
        line-height: 1.1;
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
        from {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.3), 0 0 20px #FF69B4; }}
        to {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.3), 0 0 30px #9370DB, 0 0 40px #FFD700; }}
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
        color: #8B4513;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 2em;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        background: rgba(255,255,255,0.9);
        padding: 1.5em;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        font-weight: 600;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    .quote::before {{
        content: '"';
        position: absolute;
        left: 20px;
        top: 10px;
        font-size: 4rem;
        color: rgba(139, 69, 19, 0.3);
        font-family: serif;
    }}
    
    .quote::after {{
        content: '"';
        position: absolute;
        right: 20px;
        bottom: 10px;
        font-size: 4rem;
        color: rgba(139, 69, 19, 0.3);
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
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        padding: 2em;
        margin: 2em 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
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
        color: #8B4513;
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        margin-top: 3em;
        padding: 2em;
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        font-weight: 600;
        position: relative;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    .footer::after {{
        content: 'Featured by Genius API';
        position: absolute;
        bottom: 10px;
        right: 20px;
        font-size: 0.8rem;
        color: rgba(139, 69, 19, 0.7);
        font-style: italic;
    }}
    
    .stTextInput > div > div > input {{
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        border: 2px solid rgba(147, 112, 219, 0.3);
        padding: 1em;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #1a1a1a;
        font-family: 'Poppins', sans-serif;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #9370DB;
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.3);
    }}
    
    .stExpander {{
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 0.5em 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    .stExpander:hover {{
        background: rgba(255,255,255,1);
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }}
    
    .stExpander > div > div {{
        background: transparent !important;
    }}
    
    .stExpander > div > div > div {{
        background: transparent !important;
    }}
    
    section[data-testid="stSidebar"], .stSidebar {{
        background: linear-gradient(135deg, #e8f4fd 0%, #b3e0ff 100%) !important;
        color: #111 !important;
    }}
    
    .stSidebar > div > div > div {{
        background: transparent !important;
    }}
    
    .stMarkdown {{
        color: #333333;
    }}
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: #333333;
        font-family: 'Poppins', sans-serif;
    }}
    
    .hashtags {{
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
        padding: 1em;
        margin: 1em 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
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
        background: rgba(139, 69, 19, 0.1);
        border-left: 3px solid #8B4513;
        padding: 0.5em 1em;
        margin: 0.5em 0;
        border-radius: 5px;
        font-size: 0.9rem;
        font-style: italic;
        color: #8B4513;
        font-weight: 600;
    }}
    
    .facts-cloud {{
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 1.5em;
        margin: 1em 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    .fact-item {{
        background: linear-gradient(45deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        padding: 0.8em;
        margin: 0.5em 0;
        border-left: 4px solid #FF69B4;
        font-size: 0.9rem;
        color: #495057;
        font-weight: 500;
    }}
    {all_era_styles}
    /* Sidebar override for light blue */
    section[data-testid="stSidebar"], .stSidebar, .sidebar-content{{
        background: linear-gradient(135deg, #e8f4fd 0%, #b3e0ff 100%) !important;color: #111 !important;
    }}
    /* --- Mobile Responsive Styles --- */
    @media (max-width: 900px) {{
        section[data-testid="stSidebar"] {{
            display: none !important;
        }}
        body.show-sidebar section[data-testid="stSidebar"] {{
            display: block !important;
        }}
        .show-sidebar-btn {{
            display: block !important;
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 9999;
            background: #FF69B4;
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0.7em 1.2em;
            font-size: 1.1rem;
            font-family: 'Poppins', sans-serif;
            box-shadow: 0 2px 8px #ffb6d540;
            cursor: pointer;
        }}
        .main-header, .song-grid-btn, .block-container, .stApp {{
            writing-mode: initial !important;
            transform: none !important;
            letter-spacing: normal !important;
            display: block !important;
            text-align: center !important;
            line-height: 1.2 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }}
        [class^="era-lyrics-"] {{
            word-break: normal !important;
            white-space: normal !important;
            overflow-wrap: normal !important;
            width: 100% !important;
            max-width: 100vw !important;
            font-size: 1.1rem !important;
            padding: 1em !important;
        }}
        .main-header {{
            margin-top: 3.5em !important;
        }}
    }}
    @media (min-width: 901px) {{
        .show-sidebar-btn {{
            display: none !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# Add Show Sidebar button for mobile
st.markdown('''<button class="show-sidebar-btn" onclick="document.body.classList.toggle('show-sidebar')">☰ Show Sidebar</button>''', unsafe_allow_html=True)

# --- GENIUS API HELPERS ---
def search_genius_song(song_title, artist="Taylor Swift"):
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    params = {"q": f"{song_title} {artist}"}
    r = requests.get(url, headers=headers, params=params)
    print("Genius API status:", r.status_code)
    print("Genius API response:", r.text)
    if r.status_code != 200:
        st.warning(f"Genius API error: {r.status_code}")
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
    # Genius now uses multiple <div data-lyrics-container='true'> blocks for lyrics
    lyrics_blocks = soup.find_all("div", attrs={"data-lyrics-container": "true"})
    if lyrics_blocks:
        lyrics = "\n".join(block.get_text(separator="\n").strip() for block in lyrics_blocks)
        return lyrics.strip()
    # Fallback: try old selectors
    lyrics_selectors = [
        "div.lyrics",
        "div[class*='lyrics']",
        "div[class*='Lyrics']",
        ".SongPageGriddesktop__LyricsWrapper-sc-1px5b71-1"
    ]
    for selector in lyrics_selectors:
        lyrics_elements = soup.select(selector)
        if lyrics_elements:
            for element in lyrics_elements:
                text = element.get_text(separator="\n")
                if text.strip():
                    lyrics += text + "\n"
    return lyrics.strip() if lyrics else None

def get_lyrics_lyricsovh(song_title, artist="Taylor Swift"):
    """Get lyrics from lyrics.ovh API as fallback"""
    try:
        url = f"https://api.lyrics.ovh/v1/{artist}/{song_title}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("lyrics", "")
        return None
    except Exception as e:
        return None

def get_lyrics(song_title):
    url = search_genius_song(song_title)
    if not url:
        return None, "Song not found on Genius. Please check the title."
    lyrics = scrape_lyrics_from_url(url)
    if not lyrics:
        # Try lyrics.ovh as fallback
        lyrics = get_lyrics_lyricsovh(song_title)
        if lyrics:
            return lyrics, None
        # If both fail, provide Genius link
        return None, f"Lyrics not available, but you can <a href='{url}' target='_blank'>view them on Genius</a>."
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
    """Add Swiftie annotations to lyrics, but only once per annotation per song."""
    annotated_lyrics = lyrics
    for key, annotation in SWIFTIE_ANNOTATIONS.items():
        if key in song_title.lower():
            # Find lines that might have annotations
            lines = lyrics.split('\n')
            annotation_added = False
            for i, line in enumerate(lines):
                if not annotation_added and any(word in line.lower() for word in key.split()):
                    lines[i] = f"{line}\n<div class='annotation'>💜 Swiftie Note: {annotation}</div>"
                    annotation_added = True
            annotated_lyrics = '\n'.join(lines)
            break
    return annotated_lyrics

def clean_lyrics(text):
    # Remove formatting instructions, empty lines, lines with only ?, language links, numbers, and unwanted phrases
    lines = text.split('\n')
    cleaned = []
    seen = set()
    language_pattern = re.compile(r'^(Afrikaans|Slovenščina|Español|Français|Deutsch|Italiano|Magyar|Polski|Português|Русский|Svenska|Türkçe|Українська|日本語|한국어|ไทย|Română|Česky|Català|فارسی|Беларуская|العربية|简体中文|繁體中文)$', re.IGNORECASE)
    unwanted_patterns = [
        re.compile(r'^\d+$'),  # lines that are just numbers
        re.compile(r'^You might also like', re.IGNORECASE),
        re.compile(r'^Use italics', re.IGNORECASE),
        re.compile(r'^Use bold', re.IGNORECASE),
        re.compile(r'^or visit our', re.IGNORECASE),
        re.compile(r'^lyric\)?$', re.IGNORECASE),
        re.compile(r'^\(lyric\)?$', re.IGNORECASE),
        re.compile(r'^\)$', re.IGNORECASE),
        re.compile(r'^\($', re.IGNORECASE),
    ]
    for line in lines:
        l = line.strip()
        if not l or l == '?' or l.lower().startswith('use italics') or l.lower().startswith('use bold') or l.lower().startswith('if you don') or l.lower().startswith('to learn more') or l.lower().startswith('lyrics should be broken down') or l.lower().startswith('type out all lyrics') or l.lower().startswith('section headers') or l.lower().startswith('visit our') or language_pattern.match(l):
            continue
        if any(p.match(l) for p in unwanted_patterns):
            continue
        if l not in seen:
            cleaned.append(l)
            seen.add(l)
    return '\n'.join(cleaned)

def set_song_input(song):
    st.session_state["song_input"] = song
    st.session_state["auto_search"] = True

def main():
    # Home button at the top
    if st.button('🏠 Home', key='home_btn'):
        st.session_state["song_input"] = ""
        st.session_state["auto_search"] = False
        st.rerun()

    st.markdown("""
    <style>
    html, body, [class*='css'] {
        height: 100vh !important;
        min-height: 100vh !important;
        width: 100vw !important;
        min-width: 100vw !important;
        overflow-x: hidden;
        background: #ffc0cb !important; /* Pink backdrop */
        color: #111 !important; /* Black font */
    }
    body, .main-header, .stSidebar, .block-container, .stApp {
        background: #ffc0cb !important;
        color: #111 !important;
    }
    .main-header {
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(2rem, 6vw, 4rem);
        color: #111 !important;
        text-align: center;
        margin-bottom: 1em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.08);
        font-weight: bold;
        letter-spacing: 2px;
        animation: glow 2s ease-in-out infinite alternate;
        position: relative;
        word-break: break-word;
        width: 100%;
        max-width: 100vw;
        box-sizing: border-box;
        overflow-wrap: break-word;
        white-space: normal;
        line-height: 1.1;
    }
    /* Fixed sidebar */
    section[data-testid="stSidebar"] {
        position: fixed !important;
        left: 0;
        top: 0;
        height: 100vh !important;
        min-height: 100vh !important;
        z-index: 100;
        box-shadow: 2px 0 8px rgba(0,0,0,0.04);
        width: 340px !important;
        max-width: 340px !important;
    }
    /* Adjust main content to not go under sidebar */
    div.block-container {
        margin-left: 340px !important;
        max-width: calc(100vw - 340px) !important;
        background: #ffc0cb !important;
        color: #111 !important;
    }
    .stSidebar {
        min-width: 320px !important;
        max-width: 400px !important;
        width: 22vw !important;
        overflow-y: auto;
    }
    .emoji-scroll {
        width: 100%;
        max-width: 100vw;
        overflow-x: auto;
        overflow-y: hidden;
        white-space: nowrap;
        padding-bottom: 0.5rem;
        margin-bottom: 1.2rem;
        scrollbar-color: #ffb6d5 #fff0f6;
        scrollbar-width: thin;
    }
    .emoji-item {
        display: inline-block;
        font-size: 2.2rem;
        margin: 0 0.7rem;
        transition: transform 0.2s;
        cursor: pointer;
        vertical-align: middle;
    }
    .emoji-item:hover {
        transform: scale(1.2) rotate(-8deg);
    }
    .wordcloud-img {
        display: block;
        max-width: 100%;
        width: 100%;
        height: auto;
        margin: 0 auto;
    }
    .song-grid-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1.2rem;
        margin-bottom: 0.8rem;
        justify-content: flex-start;
    }
    .song-grid-btn {
        flex: 1 1 22%;
        min-width: 0;
        max-width: 24%;
        background: #fff0f6;
        color: #111;
        border-radius: 12px;
        border: 1px solid #ffb6d5;
        font-size: 1rem;
        font-family: 'Montserrat', sans-serif;
        margin: 0.2rem 0.2rem;
        box-shadow: 0 2px 8px #ffb6d540;
        transition: transform 0.1s, box-shadow 0.1s;
        cursor: pointer;
        padding: 0.7rem 0.5rem;
        text-align: left;
        white-space: normal;
    }
    .song-grid-btn:hover {
        background: #ffe4ec;
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 4px 16px #ffb6d580;
    }
    /* Sidebar override for light blue */
    section[data-testid='stSidebar'], .stSidebar, .sidebar-content {
        background: linear-gradient(135deg, #e8f4fd 0%, #b3e0ff 100%) !important;
        color: #111 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-header">Taylor Swift Lyrics & Word Cloud</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="quote">{random.choice(TAYLOR_QUOTES)}</div>', unsafe_allow_html=True)
    # Persistent scroll-to-top script for all navigation/rerun
    st.markdown("""
    <script>
    (function() {
      const scrollToTop = () => window.scrollTo({top: 0, behavior: 'smooth'});
      document.addEventListener("DOMContentLoaded", scrollToTop);
      new MutationObserver(scrollToTop).observe(document.body, {childList: true, subtree: true});
    })();
    </script>
    """, unsafe_allow_html=True)
    # Force scroll-to-top on every song change
    dummy_scroll_key = st.session_state.get("song_input", "")
    st.markdown(f'<div id="scroll-dummy-{dummy_scroll_key}" style="display:none"></div>', unsafe_allow_html=True)
    st.markdown("""
    <script>
    window.scrollTo({top: 0, behavior: 'smooth'});
    </script>
    """, unsafe_allow_html=True)

    # Scrollable emojis with album links
    emoji_album_map = [
        ("🎤", "Taylor Swift Debut Album"),
        ("🎵", "Taylor Swift Fearless Album"),
        ("💜", "Taylor Swift Speak Now Album"),
        ("✨", "Taylor Swift Red Album"),
        ("🦋", "Taylor Swift 1989 Album"),
        ("💕", "Taylor Swift Lover Album"),
        ("🎸", "Taylor Swift Folklore Album"),
        ("⭐", "Taylor Swift Evermore Album"),
        ("🧣", "Taylor Swift Red Scarf"),
        ("🏙️", "Taylor Swift 1989 NYC"),
        ("🐍", "Taylor Swift Reputation Album"),
        ("🌈", "Taylor Swift Lover Album"),
        ("🌲", "Taylor Swift Folklore Album"),
        ("❄️", "Taylor Swift Evermore Album"),
        ("✒️", "Taylor Swift TTPD Album"),
        ("🎭", "Taylor Swift TTPD Album"),
        ("💎", "Taylor Swift Bejeweled"),
        ("🌙", "Taylor Swift Midnights Album"),
        ("🕰️", "Taylor Swift Midnights Album"),
        ("📝", "Taylor Swift Lyrics")
    ]
    emoji_html = '<div class="emoji-scroll">'
    for emoji, album in emoji_album_map:
        search_url = f'https://www.google.com/search?q={album.replace(" ", "+")}'
        emoji_html += f'<a href="{search_url}" target="_blank" class="emoji-item">{emoji}</a>'
    emoji_html += '</div>'
    st.markdown(emoji_html, unsafe_allow_html=True)

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
            # Get all albums for this era from SONG_LIST
            era_songs = [song for song in SONG_LIST if era.lower() in song["Album"].lower() or song["Album"].lower() == era.lower()]
            for song in era_songs:
                if st.button(f"🎵 {song['Song']}", key=f"sidebar_{song['Song']}_{era}", on_click=set_song_input, args=(song["Song"],)):
                    st.rerun()
    # Song input and auto-search on enter
    song_title = st.text_input("Enter a Taylor Swift song title:", key="song_input", placeholder="e.g., Love Story, Cruel Summer, ...")
    auto_search = st.session_state.get("auto_search", False)
    if song_title and (auto_search or st.session_state.get("song_input") != ""):
        st.session_state["auto_search"] = False
        try:
            lyrics, error = get_lyrics(song_title)
        except Exception as e:
            lyrics, error = None, f"Error: {str(e)}"
        if lyrics:
            era = get_era_for_song(song_title)
            era_class = era.lower().replace(' ', '-')
            st.markdown(f'<div class="era-header-{era_class}">🎵 {song_title} • {era} Era</div>', unsafe_allow_html=True)
            # Add scroll-to-top script with unique key before lyrics
            scroll_key = f"{song_title}_{random.randint(0, 1_000_000)}"
            st.markdown(f'<script id="scroll-script-{scroll_key}">window.scrollTo({{top: 0, behavior: "smooth"}});</script>', unsafe_allow_html=True)
            # Add annotations to lyrics
            annotated_lyrics = add_annotations_to_lyrics(clean_lyrics(lyrics), song_title)
            st.markdown(f'<div class="era-lyrics-{era_class}">' + annotated_lyrics.replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
            # Display era facts
            if era in ERA_CONFIG:
                facts = ERA_CONFIG[era]["facts"]
                facts_html = f'<div class="facts-cloud"><h4>📚 Fun Facts About {era} Era:</h4>'
                for fact in facts:
                    facts_html += f'<div class="fact-item">💡 {fact}</div>'
                facts_html += '</div>'
                st.markdown(facts_html, unsafe_allow_html=True)
            # Generate hashtags
            hashtags = generate_hashtags(song_title, era)
            st.markdown("### 📱 Share on Social Media")
            hashtag_html = '<div class="hashtags">'
            for hashtag in hashtags:
                hashtag_html += f'<span class="hashtag">{hashtag}</span>'
            hashtag_html += '</div>'
            st.markdown(hashtag_html, unsafe_allow_html=True)
            # Spotify preview and link (no Spotipy, just a direct link)
            spotify_search_url = f'https://open.spotify.com/search/{song_title.replace(" ", "%20")} %20{era.replace(" ", "%20")}'
            st.markdown(f'<a href="{spotify_search_url}" target="_blank" style="display:inline-block;margin:0.5em 0;padding:0.7em 1.2em;background:#1DB954;color:#fff;border-radius:8px;text-decoration:none;font-weight:bold;">Listen on Spotify 🎧</a>', unsafe_allow_html=True)
            # Generate word cloud
            st.markdown("### ☁️ Word Cloud")
            img = create_wordcloud(lyrics, ERA_CONFIG[era]["color"])
            st.image(img, use_container_width=True, output_format="PNG", caption=None, clamp=False, channels="RGB")
            st.markdown('<style>.element-container img {max-width: 100% !important; width: 100% !important; height: auto !important;}</style>', unsafe_allow_html=True)
            # Era info
            st.info(f"🎤 **{era} Era**: {ERA_CONFIG[era]['font']} font • {ERA_CONFIG[era]['color']} theme • {ERA_CONFIG[era]['animation']} animation")
        else:
            st.markdown(error or "Could not find lyrics. Please check the song title.", unsafe_allow_html=True)
    # Add JS to scroll to top after redirect or sidebar click
    st.markdown("""
    <script>
    window.scrollTo(0,0);
    const input = window.parent.document.querySelector('input[type="text"]');
    if(input){
      input.addEventListener('keydown', function(e){
        if(e.key === 'Enter'){
          window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', key: 'auto_search', value: true}, '*');
          window.scrollTo(0,0);
        }
      });
    }
    </script>
    """, unsafe_allow_html=True)
    # Song list below main content
    st.markdown("### 📜 Taylor Swift Song List")
    # Display all songs in 4 columns, no search box
    for i in range(0, len(SONG_LIST), 4):
        cols = st.columns(4)
        for j, song in enumerate(SONG_LIST[i:i+4]):
            btn_label = f"🎵 {song['Song']} ({song['Album']}, {song['Year']})"
            if cols[j].button(btn_label, key=f"songlist_{song['Song']}_{song['Album']}", on_click=set_song_input, args=(song["Song"],)):
                st.rerun()
    st.markdown('<div class="footer">🎵 Built with ❤️ for Swifties | Powered by Streamlit & Genius API</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()