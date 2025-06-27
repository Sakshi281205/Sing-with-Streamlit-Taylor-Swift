# 🎵 Taylor Swift Lyrics Explorer

A beautiful and interactive web application built with Streamlit that allows you to explore Taylor Swift's lyrics and generate stunning word clouds. Perfect for Swifties and Pythonistas who love combining music with data visualization!

## ✨ Features

- **🎶 Real-Time Lyrics Search**: Enter any Taylor Swift song title to fetch lyrics directly from Genius API
- **☁️ Word Cloud Generation**: Automatically creates beautiful, colorful word clouds from live lyrics
- **📊 Word Frequency Analysis**: See the most common words in each song with frequency counts
- **🎨 Beautiful UI**: Modern, responsive design with Taylor Swift-inspired color scheme
- **🚀 Interactive Experience**: Smooth animations and user-friendly interface
- **📱 Mobile Friendly**: Works perfectly on desktop and mobile devices
- **🔗 API-Powered**: Uses Genius API for accurate, up-to-date lyrics

## 🎼 How It Works

The app uses the **Genius API** to:
1. **Search** for Taylor Swift songs by title
2. **Fetch** lyrics in real-time from Genius.com
3. **Generate** word clouds and frequency analysis
4. **Display** results in a beautiful, interactive interface

## 🎼 Demo Songs Available

The app currently includes sample lyrics for these popular Taylor Swift songs:
- **Love Story** - The classic Romeo and Juliet inspired ballad
- **Shake It Off** - The empowering anthem about ignoring haters
- **Blank Space** - The satirical take on media portrayal

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **API Integration**: Genius API for lyrics data
- **Data Processing**: Python (requests, beautifulsoup4)
- **Visualization**: WordCloud, Matplotlib
- **Styling**: Custom CSS with Taylor Swift-inspired colors
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

4. **Open your browser**
   Navigate to `http://localhost:8501` to see the app in action!

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

1. **Enter a Song Title**: Type the name of any Taylor Swift song in the input field
2. **Get Lyrics**: Click the "Get Lyrics & Word Cloud" button
3. **View Results**: 
   - Read the lyrics fetched from Genius
   - Admire the generated word cloud
   - Check the word frequency analysis
4. **Try Popular Songs**: Use the quick demo buttons for instant results

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
5. **Share**: Get a public URL to share your app with the world!

### Other Platforms

The app can also be deployed on:
- Heroku
- AWS
- Google Cloud Platform
- Any platform that supports Python web applications

## 🔮 Future Enhancements

- [ ] **Caching**: Cache lyrics to reduce API calls
- [ ] **Audio Preview**: Add 30-second song previews
- [ ] **Lyrics Analysis**: Sentiment analysis and theme detection
- [ ] **Playlist Creation**: Create playlists based on word themes
- [ ] **Social Features**: Share word clouds on social media
- [ ] **More Artists**: Expand to include other artists
- [ ] **Advanced Analytics**: More detailed lyrics analysis

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Ideas

- Improve lyrics extraction accuracy
- Add more visualization types
- Enhance error handling
- Optimize API usage
- Add unit tests
- Improve mobile experience

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Taylor Swift**: For creating the amazing music that inspires this project
- **Genius**: For providing the lyrics API and data
- **Streamlit**: For the incredible web framework
- **Python Community**: For the amazing libraries and tools

## 📞 Support

If you have any questions or need help:

- **Issues**: Create an issue on GitHub
- **Discussions**: Start a discussion in the GitHub Discussions tab
- **Email**: Reach out to the maintainers

## 🎵 About the Creator

This project was created by a Swiftie who loves Python and data visualization. The goal is to combine the beauty of Taylor Swift's lyrics with the power of modern web technologies to create something both fun and educational.

---

**Made with ❤️ for Swifties and Pythonistas everywhere! 🐍🎵**

*"I'm the one who makes the jokes, but I'm the one who laughs the loudest"* - Taylor Swift