import streamlit as st
import requests
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from bs4 import BeautifulSoup
import random

# --- CONFIG ---
GENIUS_ACCESS_TOKEN = "YQkWoMNacdeC9oX7Uf1m-qkKULs5a8mUI700Kq7ZmFrXA_NRsW6B3Gee59NjwAeQ"

# Era-specific configuration
ERA_CONFIG = {
    "Debut": {
        "color": "#228B22",  # Forest green
        "font": "Montserrat",
        "songs": ["Our Song", "Tim McGraw", "Teardrops on My Guitar", "Picture to Burn"]
    },
    "Fearless": {
        "color": "#DAA520",  # Goldenrod
        "font": "Poppins",
        "songs": ["Fearless", "You Belong With Me", "Love Story", "Fifteen", "White Horse"]
    },
    "Speak Now": {
        "color": "#8A2BE2",  # Blue violet
        "font": "Roboto",
        "songs": ["Enchanted", "Long Live", "Mine", "Back to December", "Mean"]
    },
    "Red": {
        "color": "#DC143C",  # Crimson red
        "font": "Open Sans",
        "songs": ["22", "We Are Never Ever Getting Back Together", "I Knew You Were Trouble", "All Too Well", "Red"]
    },
    "1989": {
        "color": "#4169E1",  # Royal blue
        "font": "Lato",
        "songs": ["Style", "Blank Space", "Shake It Off", "Wildest Dreams", "Bad Blood", "Out of the Woods"]
    },
    "Reputation": {
        "color": "#2F2F2F",  # Dark gray
        "font": "Inter",
        "songs": ["Ready For It", "Delicate", "Don't Blame Me", "Look What You Made Me Do", "Getaway Car"]
    },
    "Lover": {
        "color": "#FF69B4",  # Hot pink
        "font": "Nunito",
        "songs": ["Cruel Summer", "Lover", "The Man", "You Need to Calm Down", "The Archer", "Miss Americana"]
    },
    "Folklore": {
        "color": "#696969",  # Dim gray
        "font": "Source Sans Pro",
        "songs": ["The 1", "Betty", "The Last Great American Dynasty", "August", "Illicit Affairs", "Cardigan"]
    },
    "Evermore": {
        "color": "#CD853F",  # Peru (rust/orange)
        "font": "Ubuntu",
        "songs": ["Willow", "Champagne Problems", "Tolerate It", "Marjorie", "Tis the Damn Season"]
    },
    "Midnights": {
        "color": "#191970",  # Midnight blue
        "font": "Raleway",
        "songs": ["Lavender Haze", "Anti-Hero", "Midnight Rain", "Vigilante Shit", "Bejeweled", "Karma"]
    },
    "TTPD": {
        "color": "#8B0000",  # Dark red
        "font": "Work Sans",
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

def get_era_for_song(song_title):
    """Determine which era a song belongs to"""
    song_title_lower = song_title.lower()
    for era, config in ERA_CONFIG.items():
        for song in config["songs"]:
            if song.lower() in song_title_lower or song_title_lower in song.lower():
                return era
    return "Lover"  # Default era

def get_era_styles(era):
    """Get CSS styles for a specific era"""
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
    }}
    .era-lyrics-{era.lower().replace(' ', '-')}:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px {config['color']}50, 0 6px 20px rgba(0,0,0,0.15);
    }}
    .era-header-{era.lower().replace(' ', '-')} {{
        font-family: '{config['font']}', sans-serif;
        color: {config['color']};
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: bold;
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
    }}
    
    @keyframes glow {{
        from {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.5), 0 0 20px #FF69B4; }}
        to {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.5), 0 0 30px #9370DB, 0 0 40px #FFD700; }}
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
    }}
    
    .stExpander > div > div {{
        background: transparent !important;
    }}
    
    .stExpander > div > div > div {{
        background: transparent !important;
    }}
    
    .stSidebar {{
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.2);
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

def main():
    st.markdown('<div class="main-header">🎤 Taylor Swift Lyrics & Word Cloud 🎵</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="quote">"{random.choice(TAYLOR_QUOTES)}"</div>', unsafe_allow_html=True)
    
    # Sidebar with era information
    st.sidebar.markdown("## 💜 About This App")
    st.sidebar.info("""
    - Enter a Taylor Swift song title
    - Get real lyrics from Genius
    - See era-specific theming
    - Enjoy Swiftie quotes and word clouds
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🎵 Popular Songs by Era:**")
    
    # Group songs by era in sidebar
    for era, config in ERA_CONFIG.items():
        with st.sidebar.expander(f"📀 {era}"):
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
                    
                    # Display lyrics with era-specific styling
                    st.markdown(f'<div class="era-lyrics-{era_class}">' + lyrics.replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
                    
                    # Generate word cloud
                    st.markdown("### ☁️ Word Cloud")
                    img = create_wordcloud(lyrics, ERA_CONFIG[era]["color"])
                    st.image(img, use_container_width=True)
                    
                    # Era info
                    st.info(f"🎤 **{era} Era**: {ERA_CONFIG[era]['font']} font • {ERA_CONFIG[era]['color']} theme")
                else:
                    st.error(error)
        else:
            st.warning("Please enter a song title!")
    
    st.markdown('<div class="footer">🎵 Built with ❤️ for Swifties | Powered by Streamlit & Genius API</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()