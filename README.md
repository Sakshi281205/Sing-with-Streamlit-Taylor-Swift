# 🎤 Taylor Swift Lyrics & Word Cloud Studio 🎵

A stunning, interactive web application built with Streamlit that brings Taylor Swift's music to life with 3D graphics, era-specific theming, and exclusive Swiftie features! Experience the magic of Taylor's lyrics with an immersive interface designed specifically for the Swiftie community.

## ✨ Features

### 🎨 **Immersive 3D Experience**
- **3D Glass Morphism Design**: Beautiful floating cards with backdrop blur effects
- **Custom Microphone Cursor**: Interactive cursor that changes based on the era
- **Hover Animations**: Cards lift up with enhanced shadows and sparkle effects
- **Era-Specific Transitions**: Glitter for Lover, raindrops for Folklore, static for Reputation
- **Vinyl Record Player**: Spinning animation when songs are playing

### 🌈 **Era-Specific Themes (Auto-Switching)**
When you select a song, the entire UI changes theme based on the song's era:

| **Era** | **Background** | **Animations** | **Icons** | **Colors** |
|---------|----------------|----------------|-----------|------------|
| **Debut** | Sunlight + soft fields | Butterflies | 🤠 Cowboy boots | Forest Green |
| **Fearless** | Sparkling lights | Glitter trails | 🎸 Guitar picks | Goldenrod |
| **Speak Now** | Enchanted forest | Floating lanterns | ⭐ Swirling stars | Blue Violet |
| **Red** | Fall leaves animation | Wind rustle effects | 🧣 Red scarf | Crimson Red |
| **1989** | Polaroid frame | Flash camera effects | 🏙️ NYC skyline | Royal Blue |
| **Reputation** | Dark gradient + glitch | Snake slither effects | 🐍 Pixel distortion | Dark Gray |
| **Lover** | Cotton candy clouds | Heart animations | 🌈 Rainbow doodles | Hot Pink |
| **Folklore** | Sepia tone + grain | Fog drift effects | 🌲 Handwritten poems | Dim Gray |
| **Evermore** | Snowfall animation | Faint piano notes | ❄️ Fairy lights | Rust/Orange |
| **Midnights** | Night sky + shooting stars | Clock ticking sounds | ⭐ Glitter dust | Midnight Blue |
| **TTPD** | Typewriter fade-in | Paper-tearing effects | ✒️ Quill pen | Dark Red |

### 🎶 **Interactive Lyrics Features**
- **Hover Effects**: Hover over lyrics to reveal fan theories and hidden meanings
- **Swiftie Annotation Mode**: Toggle annotations to see Swifties' interpretations
- **Lyric "Glow Up"**: Iconic lines subtly glow or pulse
- **Scratch-to-Reveal**: Interactive elements for deluxe edition songs
- **Auto-generated Hashtags**: Social media hashtags for each song

### 🎤 **Music & Audio Features**
- **Background Ambience**: Era-specific ambient sounds
- **Voice Pitch Match Game**: Sing into the mic and match Taylor's pitch
- **Secret Audio Messages**: Unlockable voice memos and Easter eggs
- **13-Second Countdown Loader**: Taylor's lucky number for page transitions

### 🔐 **Swiftie-Exclusive Elements**
- **Hidden Rooms**: "Secret Session" room with password hints in lyrics
- **"The Vault"**: For unreleased fan demos and edits
- **Interactive Scarf Tracker**: Click the red scarf, it floats to "All Too Well" lyrics
- **"Are You A Real Swiftie?" Quiz**: Unlock UI upgrades and badges
- **Star Chart Generator**: Stars based on song release dates

### 💫 **Aesthetic Elements**
- **Typewriter Animation**: TTPD lyrics type out slowly for dramatic effect
- **Star Chart Generator**: Display stars based on song release dates
- **Subtle Sparkles**: Animated sparkles around lyrics when hovered
- **Era Icons**: Floating era-specific icons around headers

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **API Integration**: Genius API for lyrics data
- **3D Graphics**: Custom CSS with glass morphism and animations
- **Data Processing**: Python (requests, beautifulsoup4)
- **Visualization**: WordCloud, Matplotlib
- **Styling**: Advanced CSS with era-specific themes
- **Web Scraping**: BeautifulSoup4 for lyrics extraction
- **Animations**: CSS keyframes and JavaScript effects

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Genius API Access Token (included in the app)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Sing-with-Streamlit-Taylor-Swift.git
   cd Sing-with-Streamlit-Taylor-Swift
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py --server.port 8501
   ```

4. **Start exploring!**
   Navigate to `http://localhost:8501` and experience the magic!

## 📦 Dependencies

The app requires the following Python packages (see `requirements.txt`):

- `streamlit>=1.28.0` - Web application framework
- `requests>=2.31.0` - HTTP library for API calls
- `beautifulsoup4>=4.12.0` - HTML parsing for lyrics extraction
- `wordcloud>=1.9.0` - Word cloud generation
- `matplotlib>=3.7.0` - Plotting library
- `Pillow>=10.0.0` - Image processing
- `numpy>=1.24.0` - Numerical computing

## 🎯 How to Use

1. **Choose Your Era**: Browse songs by era in the sidebar
2. **Select a Song**: Enter any Taylor Swift song title or use quick buttons
3. **Experience the Magic**: Watch the UI transform to match the song's era
4. **Interact**: Hover over lyrics for annotations and sparkles
5. **Share**: Copy hashtags for social media sharing
6. **Explore**: Try different songs to see all the era themes

## 🎨 Design Features

### Interactive 3D Elements
- **Glass Morphism Cards**: Semi-transparent floating elements with blur effects
- **Hover Animations**: Cards lift and sparkle on interaction
- **Custom Cursors**: Era-specific cursor designs
- **Floating Icons**: Animated era icons around headers
- **Vinyl Player**: Spinning record animation

### Era-Specific Styling
- **Dynamic Backgrounds**: Each era has unique gradient backgrounds
- **Custom Fonts**: Era-appropriate typography for each album
- **Color Schemes**: Carefully chosen colors representing each era
- **Animation Themes**: Unique animations for each era
- **Interactive Elements**: Era-specific hover effects and transitions

### Swiftie-Exclusive Features
- **13-Second Loader**: Taylor's lucky number countdown
- **Hidden Easter Eggs**: Secret interactions and animations
- **Fan Annotations**: Swiftie interpretations of lyrics
- **Social Integration**: Auto-generated hashtags for sharing
- **Quiz System**: Test your Swiftie knowledge

## 🔧 API Configuration

### Genius API Setup

The app comes pre-configured with a Genius API access token. For production deployment:

1. **Get Your Own Token**: Visit [Genius API](https://genius.com/developers) to create your own app
2. **Set Environment Variable**: Add your token to Streamlit secrets:
   ```toml
   # .streamlit/secrets.toml
   GENIUS_ACCESS_TOKEN = "your_token_here"
   ```

### Rate Limits

- Genius API has rate limits for free accounts
- The app includes error handling for API limits
- Consider upgrading to a paid Genius API plan for production use

## 🌐 Deployment

### Streamlit Community Cloud

1. **Push to GitHub**: Make sure your code is in a public GitHub repository
2. **Sign up**: Create an account at [share.streamlit.io](https://share.streamlit.io)
3. **Deploy**: Connect your GitHub repository and deploy
4. **Set Secrets**: Add your Genius API token in the Streamlit Cloud settings
5. **Share**: Get a public URL to share your interactive studio with Swifties worldwide!

### Other Platforms

The app can also be deployed on:
- Heroku
- AWS
- Google Cloud Platform
- Any platform that supports Python web applications

## 🎵 Popular Songs by Era

### Debut Era 🤠
- **Our Song** - The classic country anthem
- **Tim McGraw** - The song that started it all
- **Teardrops on My Guitar** - The relatable heartbreak ballad

### Fearless Era 🎸
- **Love Story** - The Romeo and Juliet inspired classic
- **You Belong With Me** - The relatable high school anthem
- **Fearless** - The empowering title track

### Speak Now Era ⭐
- **Enchanted** - The magical love story
- **Long Live** - The celebration of friendship
- **Mine** - The romantic proposal song

### Red Era 🧣
- **All Too Well** - The emotional masterpiece
- **22** - The carefree celebration
- **We Are Never Ever Getting Back Together** - The breakup anthem

### 1989 Era 🏙️
- **Blank Space** - The satirical media response
- **Shake It Off** - The empowering anthem
- **Style** - The sleek pop perfection

### Reputation Era 🐍
- **Look What You Made Me Do** - The revenge anthem
- **Delicate** - The vulnerable love song
- **Ready For It** - The dramatic opener

### Lover Era 🌈
- **Cruel Summer** - The catchy summer anthem
- **Lover** - The romantic title track
- **The Man** - The feminist anthem

### Folklore Era 🌲
- **Cardigan** - The cottagecore masterpiece
- **August** - The summer love story
- **The 1** - The reflective opener

### Evermore Era ❄️
- **Willow** - The magical love spell
- **Champagne Problems** - The heartbreaking ballad
- **Tolerate It** - The emotional masterpiece

### Midnights Era ⭐
- **Anti-Hero** - The introspective lead single
- **Lavender Haze** - The dreamy opener
- **Bejeweled** - The glittering anthem

### TTPD Era ✒️
- **Fortnight** - The poetic collaboration
- **The Tortured Poets Department** - The title track
- **The Black Dog** - The emotional ballad

## 🚀 Final Features

- **Now Playing Section**: Displays the current song and artist, with a direct Spotify link for instant listening.
- **Auto-Scroll to Lyrics**: When a song is selected, the app automatically scrolls to the top so lyrics are always visible.
- **Comprehensive Taylor Swift Song List**: All songs are available in a 4-column grid and sidebar, grouped by era for easy navigation.
- **Robust Lyrics Fetching & Cleaning**: Lyrics are fetched from Genius and aggressively cleaned to remove navigation, language links, and formatting clutter.
- **Era-Specific Theming**: The UI changes color, font, and background based on the song's era, with Swiftie icons and animations.
- **Swiftie Quotes & Annotations**: Enjoy random Taylor Swift quotes and unique Swiftie notes for special lyrics.
- **Interactive Word Cloud**: Generates a word cloud from the lyrics, styled to match the era.
- **Responsive, Polished UI**: Pink main background, light blue sidebar, scrollable emoji album bar, and mobile-friendly design.
- **Error Handling**: User-friendly error messages for missing lyrics or song titles.

---

This app is now ready for Swifties everywhere! 🎤✨

## 🎯 Future Enhancements

- [ ] **Audio Integration**: Background music and instrumental tracks
- [ ] **Voice Recording**: Record your karaoke performances
- [ ] **Multiplayer Mode**: Sing along with friends in real-time
- [ ] **Advanced Analytics**: Detailed song analysis and insights
- [ ] **Playlist Creation**: Create custom Taylor Swift playlists
- [ ] **Social Features**: Share performances and connect with Swifties
- [ ] **AR Features**: Augmented reality elements for mobile
- [ ] **AI Integration**: Smart song recommendations

## 🤝 Contributing

We welcome contributions from the Swiftie community! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Ideas

- Add more era-specific animations and effects
- Improve lyrics extraction accuracy
- Add more interactive elements
- Enhance the 3D graphics and animations
- Add more Swiftie-exclusive features
- Improve mobile experience
- Add unit tests and documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Taylor Swift**: For creating the amazing music that inspires this project
- **Genius**: For providing the lyrics API and data
- **Streamlit**: For the incredible web framework
- **Python Community**: For the amazing libraries and tools
- **Swiftie Community**: For the inspiration, support, and creative ideas
- **CSS/Web Design Community**: For the glass morphism and animation techniques

## 📞 Support

If you have any questions or need help:

- **Issues**: Create an issue on GitHub
- **Discussions**: Start a discussion in the GitHub Discussions tab
- **Email**: Reach out to the maintainers

## 🎵 About the Creator

This project was created by a Swiftie who loves Python, web design, and wants to share the joy of Taylor Swift's music through an immersive, interactive experience. The goal is to create a beautiful, engaging platform that celebrates Taylor's artistry, connects Swifties worldwide, and provides a unique way to experience her lyrics and music.

## 🌟 Featured by Genius API

This application is proudly powered by the Genius API, providing accurate, real-time lyrics and song information to enhance the Swiftie experience.

---

*Built with ❤️ for Swifties worldwide | Powered by Streamlit & Genius API*