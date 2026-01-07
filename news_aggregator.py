"""
News Aggregator Desktop Application
A retro newspaper-style news reader
"""

import sys
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QScrollArea,
                             QTabWidget, QFrame, QMessageBox, QSplitter)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

from rss_fetcher import RSSFetcher
from categorizer import ArticleCategorizer
from reading_list import ReadingListManager


class FetchThread(QThread):
    """Background thread for fetching articles"""
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def run(self):
        try:
            fetcher = RSSFetcher()
            articles = fetcher.fetch_articles(hours=24)
            categorizer = ArticleCategorizer()
            categorizer.categorize_articles(articles)
            self.finished.emit(articles)
        except Exception as e:
            self.error.emit(str(e))


class ArticleWidget(QFrame):
    """Widget for displaying a single article"""

    def __init__(self, article, reading_list_manager, parent=None):
        super().__init__(parent)
        self.article = article
        self.reading_list = reading_list_manager

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title_label = QLabel(article['title'])
        title_font = QFont('Georgia', 14, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("color: #1a1a1a;")
        layout.addWidget(title_label)

        # Source and date
        meta_text = f"{article['source']} • {article['published'].strftime('%B %d, %Y %I:%M %p')}"
        meta_label = QLabel(meta_text)
        meta_font = QFont('Times New Roman', 10, QFont.Weight.Normal)
        meta_label.setFont(meta_font)
        meta_label.setStyleSheet("color: #666666; font-style: italic;")
        layout.addWidget(meta_label)

        # Description
        if article['description']:
            desc_label = QLabel(article['description'])
            desc_font = QFont('Times New Roman', 11)
            desc_label.setFont(desc_font)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #333333; line-height: 1.6;")
            layout.addWidget(desc_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Open button
        open_btn = QPushButton('📰 Read Article')
        open_btn.setFont(QFont('Arial', 10))
        open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: 2px solid #1a252f;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #1a252f;
            }
        """)
        open_btn.clicked.connect(lambda: webbrowser.open(article['link']))
        button_layout.addWidget(open_btn)

        # Daily list button
        daily_btn = QPushButton('📅 Add to Daily')
        daily_btn.setFont(QFont('Arial', 10))
        daily_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if self.reading_list.is_in_daily(article['link']):
            daily_btn.setText('✓ In Daily List')
            daily_btn.setEnabled(False)
        daily_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: 2px solid #1e8449;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                border-color: #7f8c8d;
            }
        """)
        daily_btn.clicked.connect(self.add_to_daily)
        button_layout.addWidget(daily_btn)

        # Weekly list button
        weekly_btn = QPushButton('📌 Add to Weekly')
        weekly_btn.setFont(QFont('Arial', 10))
        weekly_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if self.reading_list.is_in_weekly(article['link']):
            weekly_btn.setText('✓ In Weekly List')
            weekly_btn.setEnabled(False)
        weekly_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: 2px solid #d35400;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f39c12;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                border-color: #7f8c8d;
            }
        """)
        weekly_btn.clicked.connect(self.add_to_weekly)
        button_layout.addWidget(weekly_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Widget styling
        self.setStyleSheet("""
            ArticleWidget {
                background-color: #fef9f3;
                border: 2px solid #d4c5b9;
                border-radius: 8px;
                margin: 5px;
            }
        """)

    def add_to_daily(self):
        if self.reading_list.add_to_daily(self.article):
            QMessageBox.information(self, 'Added', 'Article added to Daily reading list!')
            # Update button
            for child in self.findChildren(QPushButton):
                if 'Daily' in child.text():
                    child.setText('✓ In Daily List')
                    child.setEnabled(False)

    def add_to_weekly(self):
        if self.reading_list.add_to_weekly(self.article):
            QMessageBox.information(self, 'Added', 'Article added to Weekly reading list!')
            # Update button
            for child in self.findChildren(QPushButton):
                if 'Weekly' in child.text():
                    child.setText('✓ In Weekly List')
                    child.setEnabled(False)


class CategoryTab(QWidget):
    """Tab widget for a specific category"""

    def __init__(self, category_name, reading_list_manager):
        super().__init__()
        self.category_name = category_name
        self.reading_list = reading_list_manager
        self.articles = []

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #f5f5f0; }")

        # Container for articles
        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_layout.setSpacing(15)
        self.container_layout.setContentsMargins(20, 20, 20, 20)
        self.container.setLayout(self.container_layout)

        scroll.setWidget(self.container)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def set_articles(self, articles):
        """Set articles for this category"""
        # Clear existing
        while self.container_layout.count():
            child = self.container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.articles = articles

        if not articles:
            no_articles = QLabel(f"No {self.category_name} articles in the last 24 hours")
            no_articles.setFont(QFont('Times New Roman', 12))
            no_articles.setStyleSheet("color: #666666; padding: 40px;")
            no_articles.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.container_layout.addWidget(no_articles)
        else:
            for article in articles:
                article_widget = ArticleWidget(article, self.reading_list)
                self.container_layout.addWidget(article_widget)

        self.container_layout.addStretch()


class ReadingListTab(QWidget):
    """Tab for viewing reading lists"""

    def __init__(self, reading_list_manager, list_type='daily'):
        super().__init__()
        self.reading_list = reading_list_manager
        self.list_type = list_type

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel(f"{list_type.capitalize()} Reading List")
        title.setFont(QFont('Georgia', 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1a1a1a; padding: 10px;")
        layout.addWidget(title)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #f5f5f0; }")

        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_layout.setSpacing(10)
        self.container.setLayout(self.container_layout)

        scroll.setWidget(self.container)
        layout.addWidget(scroll)
        self.setLayout(layout)

        self.refresh()

    def refresh(self):
        """Refresh the reading list display"""
        # Clear existing
        while self.container_layout.count():
            child = self.container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        articles = self.reading_list.daily_list if self.list_type == 'daily' else self.reading_list.weekly_list

        if not articles:
            no_articles = QLabel(f"No articles in {self.list_type} reading list")
            no_articles.setFont(QFont('Times New Roman', 12))
            no_articles.setStyleSheet("color: #666666; padding: 40px;")
            no_articles.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.container_layout.addWidget(no_articles)
        else:
            for article in articles:
                item_frame = QFrame()
                item_frame.setFrameStyle(QFrame.Shape.Box)
                item_frame.setStyleSheet("""
                    QFrame {
                        background-color: #fef9f3;
                        border: 2px solid #d4c5b9;
                        border-radius: 6px;
                        padding: 10px;
                    }
                """)

                item_layout = QHBoxLayout()

                # Article info
                info_layout = QVBoxLayout()
                title_label = QLabel(article['title'])
                title_label.setFont(QFont('Georgia', 12, QFont.Weight.Bold))
                title_label.setWordWrap(True)
                info_layout.addWidget(title_label)

                source_label = QLabel(f"{article['source']} • Added: {article['added'][:10]}")
                source_label.setFont(QFont('Times New Roman', 9))
                source_label.setStyleSheet("color: #666666;")
                info_layout.addWidget(source_label)

                item_layout.addLayout(info_layout, 1)

                # Buttons
                open_btn = QPushButton('Open')
                open_btn.setFont(QFont('Arial', 9))
                open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                open_btn.clicked.connect(lambda checked, link=article['link']: webbrowser.open(link))
                item_layout.addWidget(open_btn)

                remove_btn = QPushButton('Remove')
                remove_btn.setFont(QFont('Arial', 9))
                remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                remove_btn.clicked.connect(lambda checked, link=article['link']: self.remove_article(link))
                item_layout.addWidget(remove_btn)

                item_frame.setLayout(item_layout)
                self.container_layout.addWidget(item_frame)

        self.container_layout.addStretch()

    def remove_article(self, link):
        """Remove article from reading list"""
        if self.list_type == 'daily':
            self.reading_list.remove_from_daily(link)
        else:
            self.reading_list.remove_from_weekly(link)
        self.refresh()


class NewsAggregatorApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.reading_list = ReadingListManager()
        self.articles = []
        self.fetch_thread = None

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('📰 The Daily Digest - News Aggregator')
        self.setGeometry(100, 100, 1200, 800)

        # Set application-wide style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f0;
            }
            QTabWidget::pane {
                border: 3px solid #8b7355;
                background-color: #f5f5f0;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #d4c5b9;
                color: #1a1a1a;
                padding: 12px 24px;
                margin-right: 2px;
                border: 2px solid #8b7355;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-family: 'Georgia';
                font-size: 12pt;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #fef9f3;
                color: #8b4513;
            }
            QTabBar::tab:hover {
                background-color: #e0d5c7;
            }
        """)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel('📰 THE DAILY DIGEST')
        header.setFont(QFont('Georgia', 32, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            color: #1a1a1a;
            background-color: #fef9f3;
            border: 4px double #8b7355;
            padding: 20px;
            border-radius: 8px;
            letter-spacing: 2px;
        """)
        layout.addWidget(header)

        # Subtitle
        subtitle = QLabel('Your Personal News Aggregator • Est. 2026')
        subtitle.setFont(QFont('Times New Roman', 11, QFont.Weight.Normal))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666666; font-style: italic; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        # Fetch button
        self.fetch_button = QPushButton('🔄 Fetch Latest News (Last 24 Hours)')
        self.fetch_button.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        self.fetch_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fetch_button.setMinimumHeight(50)
        self.fetch_button.setStyleSheet("""
            QPushButton {
                background-color: #8b4513;
                color: white;
                border: 3px solid #654321;
                padding: 12px;
                border-radius: 8px;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #a0522d;
            }
            QPushButton:pressed {
                background-color: #654321;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                border-color: #999999;
            }
        """)
        self.fetch_button.clicked.connect(self.fetch_articles)
        layout.addWidget(self.fetch_button)

        # Status label
        self.status_label = QLabel('Click "Fetch Latest News" to get started')
        self.status_label.setFont(QFont('Times New Roman', 11))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666666; padding: 5px;")
        layout.addWidget(self.status_label)

        # Tab widget
        self.tabs = QTabWidget()

        # Category tabs
        self.ai_tab = CategoryTab('AI', self.reading_list)
        self.economy_tab = CategoryTab('Economy', self.reading_list)
        self.politics_tab = CategoryTab('Politics', self.reading_list)
        self.other_tab = CategoryTab('Other', self.reading_list)

        self.tabs.addTab(self.ai_tab, '🤖 AI')
        self.tabs.addTab(self.economy_tab, '💰 Economy')
        self.tabs.addTab(self.politics_tab, '🏛️ Politics')
        self.tabs.addTab(self.other_tab, '📑 Other')

        # Reading list tabs
        self.daily_list_tab = ReadingListTab(self.reading_list, 'daily')
        self.weekly_list_tab = ReadingListTab(self.reading_list, 'weekly')

        self.tabs.addTab(self.daily_list_tab, '📅 Daily List')
        self.tabs.addTab(self.weekly_list_tab, '📌 Weekly List')

        layout.addWidget(self.tabs)

        main_widget.setLayout(layout)

    def fetch_articles(self):
        """Fetch articles in background thread"""
        if self.fetch_thread and self.fetch_thread.isRunning():
            return

        self.fetch_button.setEnabled(False)
        self.status_label.setText('⏳ Fetching articles from news sources...')

        self.fetch_thread = FetchThread()
        self.fetch_thread.finished.connect(self.on_fetch_finished)
        self.fetch_thread.error.connect(self.on_fetch_error)
        self.fetch_thread.start()

    def on_fetch_finished(self, articles):
        """Handle fetch completion"""
        self.articles = articles
        self.fetch_button.setEnabled(True)

        # Update status
        self.status_label.setText(f'✅ Fetched {len(articles)} articles from the last 24 hours')

        # Update category tabs
        ai_articles = [a for a in articles if a['category'] == 'AI']
        economy_articles = [a for a in articles if a['category'] == 'Economy']
        politics_articles = [a for a in articles if a['category'] == 'Politics']
        other_articles = [a for a in articles if a['category'] == 'Other']

        self.ai_tab.set_articles(ai_articles)
        self.economy_tab.set_articles(economy_articles)
        self.politics_tab.set_articles(politics_articles)
        self.other_tab.set_articles(other_articles)

        # Show breakdown
        QMessageBox.information(
            self,
            'Articles Fetched',
            f'Successfully fetched {len(articles)} articles:\n\n'
            f'🤖 AI: {len(ai_articles)}\n'
            f'💰 Economy: {len(economy_articles)}\n'
            f'🏛️ Politics: {len(politics_articles)}\n'
            f'📑 Other: {len(other_articles)}'
        )

    def on_fetch_error(self, error_msg):
        """Handle fetch error"""
        self.fetch_button.setEnabled(True)
        self.status_label.setText('❌ Error fetching articles')
        QMessageBox.critical(self, 'Error', f'Failed to fetch articles:\n{error_msg}')


def main():
    app = QApplication(sys.argv)

    # Set application font
    app.setFont(QFont('Times New Roman', 10))

    window = NewsAggregatorApp()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
