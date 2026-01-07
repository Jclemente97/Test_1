# 📰 The Daily Digest - News Aggregator

A beautiful desktop GUI application for aggregating news from multiple sources with automatic categorization and reading list management.

## Features

- **Multi-Source RSS Feeds**: Fetches articles from NYT (Business, Technology, Politics), WSJ (World News, Markets, Opinion), TechCrunch, The Verge, Wired, Ars Technica, Reuters, BBC News, CNN, and NPR
- **Automatic Categorization**: Smart keyword-based categorization into AI, Economy, Politics, and Other
- **Reading Lists**: Save articles to Daily or Weekly reading lists
- **24-Hour Filter**: Only shows articles from the last 24 hours
- **Retro Newspaper Design**: Clean, old-fashioned newspaper aesthetic
- **One-Click Web Access**: Open any article in your browser with a single click

## Installation

### Prerequisites
- Python 3.11+
- Linux with display server (or Xvfb for headless environments)

### System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y libegl1 libgl1 libxkbcommon-x11-0 libdbus-1-3 \
  libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
  libxcb-render-util0 libxcb-xinerama0 libxcb-shape0 libxcb-cursor0 xvfb
```

### Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python news_aggregator.py
```

For headless environments (no display):
```bash
# Start virtual display
Xvfb :99 -screen 0 1920x1080x24 &

# Run app
export DISPLAY=:99
python news_aggregator.py
```

### Using the App

1. **Fetch News**: Click the "🔄 Fetch Latest News (Last 24 Hours)" button to retrieve articles
2. **Browse by Category**: Use the tabs to view articles categorized as AI, Economy, Politics, or Other
3. **Read Articles**: Click "📰 Read Article" to open any article in your web browser
4. **Save for Later**:
   - Click "📅 Add to Daily" to add to your daily reading list
   - Click "📌 Add to Weekly" to add to your weekly reading list
5. **Manage Reading Lists**: Use the "Daily List" and "Weekly List" tabs to view and manage saved articles

## Project Structure

```
.
├── news_aggregator.py    # Main GUI application
├── rss_fetcher.py        # RSS feed fetching and parsing
├── categorizer.py        # Article categorization logic
├── reading_list.py       # Reading list management
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## How It Works

### RSS Fetching
The app fetches RSS/Atom feeds from multiple news sources using HTTP requests and XML parsing. It supports both RSS 2.0 and Atom formats.

### Categorization
Articles are automatically categorized using an intelligent keyword matching system with priority weighting:

**Priority Keywords** (3x weight): Strong indicators like "ChatGPT", "Federal Reserve", "White House"
**Regular Keywords** (1x weight): General terms like "ai", "market", "politics"
**Title Boost** (2x multiplier): Keywords found in titles are weighted more heavily

Categories:
- **AI**: ChatGPT, LLMs, machine learning, neural networks, AI companies (OpenAI, Anthropic, etc.)
- **Economy**: Stock market, Federal Reserve, inflation, GDP, earnings, crypto, venture capital
- **Politics**: Congress, White House, elections, legislation, Supreme Court, foreign policy
- **Other**: Everything else (general news, science, culture, sports, etc.)

The system requires a minimum score to avoid weak categorization, ensuring articles are only categorized when there's strong evidence.

### Reading Lists
Reading lists are stored in a local JSON file (`reading_lists.json`) and persist between sessions. You can add articles to either daily or weekly lists for later reading.

## Customization

### Adding More News Sources
Edit `rss_fetcher.py` and add sources to the `FEEDS` dictionary:

```python
FEEDS = {
    'Source Name': 'https://example.com/rss/feed.xml',
    # ... more sources
}
```

### Adjusting Categories
Edit `categorizer.py` to modify category keywords:

```python
CATEGORIES = {
    'CategoryName': ['keyword1', 'keyword2', ...],
    # ... more categories
}
```

### Changing Time Window
By default, the app fetches articles from the last 24 hours. To change this, modify the `fetch_articles()` call in `news_aggregator.py`:

```python
fetcher.fetch_articles(hours=48)  # Fetch last 48 hours
```

## Design

The app features a retro newspaper aesthetic with:
- Georgia and Times New Roman serif fonts for readability
- Beige/cream color scheme reminiscent of newsprint
- Clear visual hierarchy with borders and frames
- Large, readable text sizes
- Intuitive button layouts

## Troubleshooting

### "No module named 'PyQt6'" error
Install PyQt6: `pip install PyQt6`

### "libEGL.so.1: cannot open shared object" error
Install system dependencies listed above

### No articles appearing
- Check your internet connection
- Some RSS feeds may be temporarily unavailable
- Try again in a few minutes

### App won't start on headless server
Use Xvfb (virtual framebuffer) as shown in the usage section

## License

This project is open source and available for personal and educational use.

## Credits

Built with Python, PyQt6, and enthusiasm for clean design.
