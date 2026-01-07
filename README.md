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
Articles are automatically categorized using a **comprehensive keyword matching system** with intelligent filtering:

**Extensive Keyword Lists**: Each category has 50+ carefully chosen keywords:

**AI Category** (~60 keywords):
- Companies: OpenAI, Anthropic, DeepMind, Meta AI, Google AI, Microsoft AI, Hugging Face
- Products: ChatGPT, GPT-4, Claude, Gemini, Copilot, DALL-E, Midjourney
- Technologies: machine learning, deep learning, neural networks, LLMs, transformers
- Applications: chatbots, computer vision, NLP, autonomous vehicles, robotics
- Concepts: AI safety, AI ethics, AI regulation, prompt engineering

**Economy Category** (~90 keywords):
- Institutions: Federal Reserve, Wall Street, Treasury, SEC, central banks
- Markets: stock market, Dow Jones, NASDAQ, S&P 500, NYSE
- Indicators: inflation, recession, GDP, unemployment, interest rates, CPI
- Finance: earnings, IPO, mergers, acquisitions, venture capital
- Crypto: Bitcoin, Ethereum, blockchain, DeFi, NFT
- Terms: stocks, shares, trading, investors, commodities, currencies

**Politics Category** (~70 keywords):
- Institutions: White House, Congress, Senate, Supreme Court, Pentagon
- Positions: president, senator, governor, cabinet members
- Parties: Democrat, Republican, GOP, bipartisan
- Elections: campaign, ballot, voting, polls, primary
- Actions: legislation, veto, impeachment, hearings
- International: NATO, UN, foreign policy, sanctions, diplomacy

**Smart Features**:
- **Word Boundaries**: Prevents false matches ("ai" won't match in "daily", "said", "laid")
- **Exclusion Patterns**: Filters out common false positives for AI category
- **Title Weighting**: Keywords in titles get 3x weight vs description (1x)
- **Context Checking**: AI exclusions overridden by strong AI context
- **Minimum Score**: Requires score ≥2 to categorize, ensuring meaningful matches

The comprehensive keyword lists ensure accurate categorization while maintaining high precision.

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
