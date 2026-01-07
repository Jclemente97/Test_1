"""Reading List Manager"""
import json
import os
from datetime import datetime

class ReadingListManager:
    """Manages daily and weekly reading lists"""

    def __init__(self, data_file='reading_lists.json'):
        self.data_file = data_file
        self.daily_list = []
        self.weekly_list = []
        self.load()

    def load(self):
        """Load reading lists from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.daily_list = data.get('daily', [])
                    self.weekly_list = data.get('weekly', [])
            except Exception as e:
                print(f"Error loading reading lists: {e}")
                self.daily_list = []
                self.weekly_list = []

    def save(self):
        """Save reading lists to file"""
        try:
            data = {
                'daily': self.daily_list,
                'weekly': self.weekly_list
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving reading lists: {e}")

    def add_to_daily(self, article):
        """Add article to daily reading list"""
        article_data = {
            'title': article['title'],
            'link': article['link'],
            'source': article['source'],
            'added': datetime.now().isoformat()
        }

        # Check if already in list
        if not any(a['link'] == article['link'] for a in self.daily_list):
            self.daily_list.append(article_data)
            self.save()
            return True
        return False

    def add_to_weekly(self, article):
        """Add article to weekly reading list"""
        article_data = {
            'title': article['title'],
            'link': article['link'],
            'source': article['source'],
            'added': datetime.now().isoformat()
        }

        # Check if already in list
        if not any(a['link'] == article['link'] for a in self.weekly_list):
            self.weekly_list.append(article_data)
            self.save()
            return True
        return False

    def remove_from_daily(self, link):
        """Remove article from daily list"""
        self.daily_list = [a for a in self.daily_list if a['link'] != link]
        self.save()

    def remove_from_weekly(self, link):
        """Remove article from weekly list"""
        self.weekly_list = [a for a in self.weekly_list if a['link'] != link]
        self.save()

    def is_in_daily(self, link):
        """Check if article is in daily list"""
        return any(a['link'] == link for a in self.daily_list)

    def is_in_weekly(self, link):
        """Check if article is in weekly list"""
        return any(a['link'] == link for a in self.weekly_list)
