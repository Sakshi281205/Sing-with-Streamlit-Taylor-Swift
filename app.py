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
        "color": "#90EE90",  # Light green
        "font": "Dancing Script",
        "songs": ["Our Song", "Tim McGraw", "Teardrops on My Guitar", "Picture to Burn"]
    },
    "Fearless": {
        "color": "#FFD700",  # Gold
        "font": "Great Vibes",
        "songs": ["Fearless", "You Belong With Me", "Love Story", "Fifteen", "White Horse"]
    },
    "Speak Now": {
        "color": "#DDA0DD",  # Lilac
        "font": "Cinzel Decorative",
        "songs": ["Enchanted", "Long Live", "Mine", "Back to December", "Mean"]
    },
    "Red": {
        "color": "#DC143C",  # Crimson red
        "font": "Bebas Neue",
        "songs": ["22", "We Are Never Ever Getting Back Together", "I Knew You Were Trouble", "All Too Well", "Red"]
    },
    "1989": {
        "color": "#87CEEB",  # Light blue
        "font": "Montserrat",
        "songs": ["Style", "Blank Space", "Shake It Off", "Wildest Dreams", "Bad Blood", "Out of the Woods"]
    },
    "Reputation": {
        "color": "#2F2F2F",  # Dark gray
        "font": "UnifrakturCook",
        "songs": ["Ready For It", "Delicate", "Don't Blame Me", "Look What You Made Me Do", "Getaway Car"]
    },
    "Lover": {
        "color": "#FFB6C1",  # Pastel pink
        "font": "Parisienne",
        "songs": ["Cruel Summer", "Lover", "The Man", "You Need to Calm Down", "The Archer", "Miss Americana"]
    },
    "Folklore": {
        "color": "#C0C0C0",  # Gray
        "font": "Cormorant Garamond",
        "songs": ["The 1", "Betty", "The Last Great American Dynasty", "August", "Illicit Affairs", "Cardigan"]
    },
    "Evermore": {
        "color": "#CD853F",  # Rust/Orange
        "font": "EB Garamond",
        "songs": ["Willow", "Champagne Problems", "Tolerate It", "Marjorie", "Tis the Damn Season"]
    },
    "Midnights": {
        "color": "#191970",  # Midnight blue
        "font": "Orbitron",
        "songs": ["Lavender Haze", "Anti-Hero", "Midnight Rain", "Vigilante Shit", "Bejeweled", "Karma"]
    },
    "TTOD": {
        "color": "#800020",  # Deep burgundy
        "font": "Spectral",
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
        background: linear-gradient(135deg, {config['color']}15 0%, {config['color']}25 100%);
        border-left: 6px solid {config['color']};
        border-radius: 12px;
        padding: 1.5em;
        margin: 1em 0;
        font-size: 1.1rem;
        color: #2c2c2c;
        font-family: '{config['font']}', cursive;
        white-space: pre-line;
        box-shadow: 0 4px 15px {config['color']}30;
    }}
    .era-header-{era.lower().replace(' ', '-')} {{
        font-family: '{config['font']}', cursive;
        color: {config['color']};
        font-size: 2rem;
        text-align: center;
        margin-bottom: 1em;
        text-shadow: 1px 1px 8px #fff;
    }}
    """

# --- PAGE STYLE ---
st.set_page_config(page_title="Taylor Swift Lyrics & Word Cloud", page_icon="🎤", layout="wide")

# Generate all era styles
all_era_styles = "\n".join([get_era_styles(era) for era in ERA_CONFIG.keys()])

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Great+Vibes&family=Cinzel+Decorative&family=Bebas+Neue&family=Montserrat:wght@400;600&family=UnifrakturCook&family=Parisienne&family=Cormorant+Garamond&family=EB+Garamond&family=Orbitron&family=Spectral&family=Poppins:wght@400;600&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #f3e6f5 100%);
    }}
    
    .main-header {{
        font-family: 'Dancing Script', cursive;
        font-size: 3rem;
        color: #FF69B4;
        text-align: center;
        margin-bottom: 0.5em;
        text-shadow: 1px 1px 8px #fff, 0 0 10px #9370DB;
    }}
    
    .quote {{
        font-family: 'Dancing Script', cursive;
        color: #9370DB;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 1.5em;
    }}
    
    .stButton > button {{
        background: linear-gradient(90deg, #FF69B4 0%, #9370DB 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.7em 2em;
        font-weight: bold;
        font-size: 1.1rem;
        margin-top: 0.5em;
        margin-bottom: 1em;
        box-shadow: 0 2px 8px #f3e6f5;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(90deg, #9370DB 0%, #FF69B4 100%);
        color: #fff0f6;
    }}
    
    .wordcloud-container {{
        background: #f3e6f5;
        border-radius: 16px;
        padding: 1em;
        margin: 1em 0;
        text-align: center;
        box-shadow: 0 2px 12px #f3e6f5;
    }}
    
    .footer {{
        text-align: center;
        color: #9370DB;
        font-family: 'Dancing Script', cursive;
        font-size: 1.1rem;
        margin-top: 2em;
        padding: 1em;
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
    
    # Remove any "Read More" sections
    for read_more in soup.find_all(text=re.compile(r'Read More', re.IGNORECASE)):
        read_more.parent.decompose()
    
    for div in soup.find_all("div", attrs={"data-lyrics-container": "true"}):
        # Remove any "Read More" text from the lyrics
        text = div.get_text(separator="\n")
        text = re.sub(r'Read More.*', '', text, flags=re.IGNORECASE)
        lyrics += text + "\n"
    
    if not lyrics:
        # fallback for old layout
        lyrics_div = soup.find("div", class_="lyrics")
        if lyrics_div:
            text = lyrics_div.get_text(separator="\n")
            text = re.sub(r'Read More.*', '', text, flags=re.IGNORECASE)
            lyrics = text
    
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
                    st.image(img, use_column_width=True)
                    
                    # Era info
                    st.info(f"🎤 **{era} Era**: {ERA_CONFIG[era]['font']} font • {ERA_CONFIG[era]['color']} theme")
                else:
                    st.error(error)
        else:
            st.warning("Please enter a song title!")
    
    st.markdown('<div class="footer">🎵 Built with ❤️ for Swifties | Powered by Streamlit & Genius API</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()