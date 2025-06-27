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
TAYLOR_QUOTES = [
    "'I'm the one who makes the jokes, but I'm the one who laughs the loudest'",
    "'I want to be remembered as someone who was never afraid to be herself'",
    "'I think fearless is having fears but jumping anyway'",
    "'I'm intimidated by the fear of being average'",
    "'You are not the opinion of someone who doesn't know you'",
    "'No matter what happens in life, be good to people'",
    "'People haven't always been there for me, but music always has'",
    "'Just be yourself, there is no one better'",
    "'Unique and different is the next generation of beautiful'",
    "'The lesson I've learned the most often in life is that you're always going to know more in the future than you know now'"
]

# --- PAGE STYLE ---
st.set_page_config(page_title="Taylor Swift Lyrics & Word Cloud", page_icon="🎤", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #f3e6f5 100%);
    }
    .main-header {
        font-family: 'Dancing Script', cursive;
        font-size: 3rem;
        color: #FF69B4;
        text-align: center;
        margin-bottom: 0.5em;
        text-shadow: 1px 1px 8px #fff, 0 0 10px #9370DB;
    }
    .quote {
        font-family: 'Dancing Script', cursive;
        color: #9370DB;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 1.5em;
    }
    .lyrics-box {
        background: #fff0f6;
        border-left: 6px solid #FF69B4;
        border-radius: 12px;
        padding: 1.5em;
        margin: 1em 0;
        font-size: 1.1rem;
        color: #4B2067;
        font-family: 'Poppins', sans-serif;
        white-space: pre-line;
        box-shadow: 0 2px 12px #f3e6f5;
    }
    .stButton > button {
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
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #9370DB 0%, #FF69B4 100%);
        color: #fff0f6;
    }
    .wordcloud-container {
        background: #f3e6f5;
        border-radius: 16px;
        padding: 1em;
        margin: 1em 0;
        text-align: center;
        box-shadow: 0 2px 12px #f3e6f5;
    }
    .footer {
        text-align: center;
        color: #9370DB;
        font-family: 'Dancing Script', cursive;
        font-size: 1.1rem;
        margin-top: 2em;
        padding: 1em;
    }
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
    for div in soup.find_all("div", attrs={"data-lyrics-container": "true"}):
        lyrics += div.get_text(separator="\n") + "\n"
    if not lyrics:
        # fallback for old layout
        lyrics_div = soup.find("div", class_="lyrics")
        if lyrics_div:
            lyrics = lyrics_div.get_text(separator="\n")
    return lyrics.strip() if lyrics else None

def get_lyrics(song_title):
    url = search_genius_song(song_title)
    if not url:
        return None, "Song not found on Genius. Please check the title."
    lyrics = scrape_lyrics_from_url(url)
    if not lyrics:
        return None, "Lyrics not found or not available for this song."
    return lyrics, None

def create_wordcloud(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    stop_words = set([w.strip() for w in '''the a an and or but in on at to for of with by i you he she it we they me him her us them my your his its our their mine yours hers ours theirs this that these those am is are was were be been being have has had do does did will would could should may might must can oh yeah baby just like got get gonna wanna cause chorus verse bridge intro outro repeat x2 x3 x4'''.split()])
    wordcloud = WordCloud(
        width=800, height=400, background_color='white', colormap='plasma', max_words=100,
        stopwords=stop_words, random_state=42
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
    st.markdown(f'<div class="quote">{random.choice(TAYLOR_QUOTES)}</div>', unsafe_allow_html=True)
    st.sidebar.markdown("## 💜 About This App")
    st.sidebar.info("""
    - Enter a Taylor Swift song title
    - Get real lyrics from Genius
    - See a beautiful word cloud
    - Enjoy Swiftie quotes and theme
    """)
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Popular Songs:**")
    for song in ["Love Story", "Shake It Off", "Blank Space", "Cruel Summer", "Anti-Hero", "Cardigan", "Lover", "You Belong With Me"]:
        if st.sidebar.button(f"🎵 {song}"):
            st.session_state["song_input"] = song
            st.rerun()
    song_title = st.text_input("Enter a Taylor Swift song title:", key="song_input", placeholder="e.g., Love Story, Cruel Summer, ...")
    if st.button("Get Lyrics & Word Cloud", type="primary"):
        if song_title:
            with st.spinner("Fetching lyrics and generating word cloud..."):
                lyrics, error = get_lyrics(song_title)
                if lyrics:
                    st.markdown('<div class="lyrics-box">' + lyrics.replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
                    st.markdown("### ☁️ Word Cloud")
                    img = create_wordcloud(lyrics)
                    st.image(img, use_column_width=True)
                else:
                    st.error(error)
        else:
            st.warning("Please enter a song title!")
    st.markdown('<div class="footer">🎵 Built with ❤️ for Swifties | Powered by Streamlit & Genius API</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()