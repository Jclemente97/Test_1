"""
News Aggregator Demo - Auto-fetches on startup
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from news_aggregator import NewsAggregatorApp

def main():
    app = QApplication(sys.argv)
    window = NewsAggregatorApp()
    window.show()

    # Auto-fetch articles after 2 seconds
    QTimer.singleShot(2000, window.fetch_articles)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
