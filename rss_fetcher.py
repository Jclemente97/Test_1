"""RSS Feed Fetcher Module"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import time
import html

class RSSFetcher:
    """Fetches and parses RSS feeds from multiple news sources"""

    FEEDS = {
        'NYT': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'WSJ': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
        'Bloomberg': 'https://feeds.bloomberg.com/markets/news.rss',
        'Axios': 'https://api.axios.com/feed/',
        'The Verge': 'https://www.theverge.com/rss/index.xml',
        'Wired': 'https://www.wired.com/feed/rss',
        'TechCrunch': 'https://techcrunch.com/feed/',
        'Reuters': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best'
    }

    def __init__(self):
        self.articles = []

    def fetch_articles(self, hours=24):
        """Fetch articles from the last N hours"""
        self.articles = []
        cutoff_time = datetime.now() - timedelta(hours=hours)

        for source, url in self.FEEDS.items():
            try:
                response = requests.get(url, timeout=15, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                response.raise_for_status()

                articles = self._parse_rss(response.content, source, cutoff_time)
                self.articles.extend(articles)
            except Exception as e:
                print(f"Error fetching {source}: {e}")

        # Sort by published date (newest first)
        self.articles.sort(key=lambda x: x['published'], reverse=True)
        return self.articles

    def _parse_rss(self, content, source, cutoff_time):
        """Parse RSS/Atom feed XML content"""
        articles = []
        try:
            root = ET.fromstring(content)

            # Detect feed type (RSS or Atom)
            if root.tag == '{http://www.w3.org/2005/Atom}feed':
                articles = self._parse_atom(root, source, cutoff_time)
            else:
                articles = self._parse_rss_2_0(root, source, cutoff_time)

        except Exception as e:
            print(f"Error parsing {source} XML: {e}")

        return articles

    def _parse_rss_2_0(self, root, source, cutoff_time):
        """Parse RSS 2.0 format"""
        articles = []

        for item in root.findall('.//item'):
            try:
                title = item.findtext('title', 'No Title')
                link = item.findtext('link', '')
                description = item.findtext('description', '')

                # Parse date
                pub_date_str = item.findtext('pubDate') or item.findtext('dc:date', namespaces={'dc': 'http://purl.org/dc/elements/1.1/'})
                published = None

                if pub_date_str:
                    try:
                        published = date_parser.parse(pub_date_str)
                    except:
                        published = datetime.now()
                else:
                    published = datetime.now()

                # Skip if too old
                if published < cutoff_time:
                    continue

                # Clean description
                description = self._clean_html(description)[:300]

                articles.append({
                    'title': html.unescape(title),
                    'link': link,
                    'description': description,
                    'source': source,
                    'published': published,
                    'category': None
                })
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue

        return articles

    def _parse_atom(self, root, source, cutoff_time):
        """Parse Atom format"""
        articles = []
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        for entry in root.findall('atom:entry', ns):
            try:
                title = entry.findtext('atom:title', 'No Title', ns)
                link_elem = entry.find('atom:link[@rel="alternate"]', ns) or entry.find('atom:link', ns)
                link = link_elem.get('href', '') if link_elem is not None else ''

                summary = entry.findtext('atom:summary', '', ns) or entry.findtext('atom:content', '', ns)

                # Parse date
                pub_date_str = entry.findtext('atom:published', ns) or entry.findtext('atom:updated', ns)
                published = None

                if pub_date_str:
                    try:
                        published = date_parser.parse(pub_date_str)
                    except:
                        published = datetime.now()
                else:
                    published = datetime.now()

                # Skip if too old
                if published < cutoff_time:
                    continue

                # Clean description
                summary = self._clean_html(summary)[:300]

                articles.append({
                    'title': html.unescape(title),
                    'link': link,
                    'description': summary,
                    'source': source,
                    'published': published,
                    'category': None
                })
            except Exception as e:
                print(f"Error parsing entry: {e}")
                continue

        return articles

    def _clean_html(self, text):
        """Remove HTML tags and clean text"""
        import re
        # Remove HTML tags
        text = re.sub('<[^<]+?>', '', text)
        # Decode HTML entities
        text = html.unescape(text)
        # Clean whitespace
        text = ' '.join(text.split())
        return text.strip()
