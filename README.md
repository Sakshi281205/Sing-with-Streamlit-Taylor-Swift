# 🎤 Taylor Swift Karaoke Studio 🎵

A beautiful and immersive karaoke-style web application built with Streamlit that allows Swifties to sing along with their favorite Taylor Swift songs! Experience the magic of Taylor's lyrics with a stunning, interactive interface designed specifically for the Swiftie community.

## ✨ Features

- **🎤 Karaoke Experience**: Sing along with any Taylor Swift song in a beautiful, immersive interface
- **🎵 Real-Time Lyrics**: Fetch lyrics directly from Genius API for accurate, up-to-date content
- **☁️ Word Cloud Generation**: Beautiful visualizations of song themes and patterns
- **📊 Song Analysis**: Discover the most common words and themes in each song
- **💜 Taylor Swift Theme**: Immersive design with Taylor's quotes, colors, and aesthetic
- **🎨 Beautiful UI**: Stunning gradients, animations, and Swiftie-inspired design
- **📱 Mobile Friendly**: Perfect karaoke experience on any device
- **🔗 API-Powered**: Uses Genius API for accurate, real-time lyrics

## 🎼 The Swiftie Experience

This app is designed specifically for Swifties to:
- **Sing along** with their favorite Taylor Swift songs
- **Discover** new songs and lyrics
- **Connect** with Taylor's words and themes
- **Share** the experience with fellow Swifties
- **Enjoy** a beautiful, immersive interface

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **API Integration**: Genius API for lyrics data
- **Data Processing**: Python (requests, beautifulsoup4)
- **Visualization**: WordCloud, Matplotlib
- **Styling**: Custom CSS with Taylor Swift-inspired design
- **Web Scraping**: BeautifulSoup4 for lyrics extraction

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
   streamlit run app.py
   ```

4. **Start singing!**
   Navigate to `http://localhost:8501` and begin your karaoke session!

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

1. **Choose Your Song**: Enter any Taylor Swift song title in the search box
2. **Start Singing**: Click "🎤 Start Singing!" to fetch the lyrics
3. **Sing Along**: Read the lyrics in the beautiful karaoke-style display
4. **Explore**: Check out the word cloud and song analysis
5. **Try More**: Use the quick song buttons to explore different tracks

## 🎨 Design Features

### Taylor Swift Theme
- **Gradient Backgrounds**: Beautiful purple and pink gradients inspired by Taylor's aesthetic
- **Custom Fonts**: Dancing Script for headers, Poppins for content
- **Animations**: Sparkling effects and glowing elements
- **Taylor Quotes**: Random inspirational quotes from Taylor Swift
- **Swiftie Colors**: Pink, purple, and gold color scheme

### Interactive Elements
- **Karaoke Container**: Clean, readable lyrics display
- **Animated Buttons**: Hover effects and smooth transitions
- **Scrollable Lyrics**: Easy-to-read format for singing along
- **Word Cloud Display**: Beautiful visualization of song themes
- **Song Analysis**: Interactive statistics and word frequency

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
5. **Share**: Get a public URL to share your karaoke studio with Swifties worldwide!

### Other Platforms

The app can also be deployed on:
- Heroku
- AWS
- Google Cloud Platform
- Any platform that supports Python web applications

## 🎵 Popular Songs

The app includes quick access to popular Taylor Swift songs:
- **Love Story** - The classic Romeo and Juliet inspired ballad
- **Shake It Off** - The empowering anthem about ignoring haters
- **Blank Space** - The satirical take on media portrayal
- **Cruel Summer** - The catchy summer anthem
- **Anti-Hero** - The introspective lead single
- **Cardigan** - The folklore masterpiece
- **Lover** - The romantic title track
- **You Belong With Me** - The relatable high school anthem

## 🔮 Future Enhancements

- [ ] **Audio Integration**: Add background music or instrumental tracks
- [ ] **Lyrics Highlighting**: Karaoke-style word-by-word highlighting
- [ ] **Playlist Creation**: Create custom Taylor Swift playlists
- [ ] **Social Features**: Share karaoke sessions with friends
- [ ] **Voice Recording**: Record your karaoke performances
- [ ] **Album Themes**: Organize songs by album eras
- [ ] **Advanced Analytics**: More detailed song analysis

## 🤝 Contributing

We welcome contributions from the Swiftie community! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Ideas

- Add more Taylor Swift quotes and themes
- Improve lyrics extraction accuracy
- Add more visualization types
- Enhance the karaoke experience
- Add unit tests
- Improve mobile experience

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Taylor Swift**: For creating the amazing music that inspires this project
- **Genius**: For providing the lyrics API and data
- **Streamlit**: For the incredible web framework
- **Python Community**: For the amazing libraries and tools
- **Swiftie Community**: For the inspiration and support

## 📞 Support

If you have any questions or need help:

- **Issues**: Create an issue on GitHub
- **Discussions**: Start a discussion in the GitHub Discussions tab
- **Email**: Reach out to the maintainers

## 🎵 About the Creator

This project was created by a Swiftie who loves Python and wants to share the joy of singing along with Taylor Swift's music. The goal is to create an immersive, beautiful experience that celebrates Taylor's artistry and connects Swifties worldwide.

---

**Made with ❤️ for Swifties everywhere! 🐍🎵**

*"I'm the one who makes the jokes, but I'm the one who laughs the loudest"* - Taylor Swift