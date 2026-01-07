"""Article Categorizer Module"""

class ArticleCategorizer:
    """Categorizes articles based on keyword matching"""

    CATEGORIES = {
        'AI': [
            'artificial intelligence', 'ai', 'machine learning', 'deep learning',
            'neural network', 'chatgpt', 'openai', 'anthropic', 'claude',
            'google ai', 'llm', 'large language model', 'generative ai',
            'chatbot', 'gpt', 'neural', 'algorithm', 'automation', 'robot',
            'computer vision', 'natural language', 'nlp', 'ml model'
        ],
        'Economy': [
            'economy', 'economic', 'market', 'stock', 'trading', 'wall street',
            'federal reserve', 'inflation', 'recession', 'gdp', 'unemployment',
            'jobs report', 'interest rate', 'dow', 'nasdaq', 's&p', 'bitcoin',
            'cryptocurrency', 'crypto', 'finance', 'financial', 'banking',
            'investment', 'investor', 'earnings', 'revenue', 'profit',
            'business', 'corporate', 'company', 'startup', 'venture capital'
        ],
        'Politics': [
            'politics', 'political', 'election', 'congress', 'senate', 'house',
            'president', 'biden', 'trump', 'government', 'policy', 'legislation',
            'democrat', 'republican', 'vote', 'voting', 'campaign', 'white house',
            'governor', 'mayor', 'parliament', 'minister', 'law', 'regulation',
            'supreme court', 'court', 'justice', 'legal', 'foreign policy',
            'diplomacy', 'war', 'military', 'defense'
        ]
    }

    def categorize(self, article):
        """Categorize a single article"""
        text = f"{article['title']} {article['description']}".lower()

        # Count matches for each category
        scores = {}
        for category, keywords in self.CATEGORIES.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[category] = score

        # Find category with highest score
        max_score = max(scores.values())
        if max_score > 0:
            for category, score in scores.items():
                if score == max_score:
                    return category

        return 'Other'

    def categorize_articles(self, articles):
        """Categorize a list of articles"""
        for article in articles:
            article['category'] = self.categorize(article)
        return articles
