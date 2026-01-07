"""Article Categorizer Module"""

class ArticleCategorizer:
    """Categorizes articles based on keyword matching"""

    # High-priority keywords that strongly indicate a category
    PRIORITY_KEYWORDS = {
        'AI': [
            'artificial intelligence', 'chatgpt', 'claude ai', 'openai', 'anthropic',
            'gemini ai', 'copilot ai', 'gpt-4', 'gpt-5', 'llm', 'large language model',
            'generative ai', 'deep learning', 'neural network', 'machine learning model',
            'ai model', 'ai system', 'language model'
        ],
        'Economy': [
            'federal reserve', 'interest rate', 'inflation rate', 'stock market',
            'dow jones', 'nasdaq', 's&p 500', 'wall street', 'treasury', 'bond yield',
            'gdp growth', 'unemployment rate', 'jobs report', 'consumer price',
            'economic growth', 'trade deficit', 'ipo', 'merger', 'acquisition'
        ],
        'Politics': [
            'white house', 'congress', 'senate', 'house of representatives',
            'supreme court', 'presidential', 'election 2024', 'campaign', 'ballot',
            'legislation', 'bill passes', 'veto', 'impeachment', 'cabinet',
            'state department', 'foreign policy', 'sanctions', 'treaty'
        ]
    }

    # Regular keywords for additional matching
    CATEGORIES = {
        'AI': [
            'ai', 'chatbot', 'automation', 'algorithm', 'computer vision',
            'natural language processing', 'nlp', 'robotics', 'autonomous',
            'deepmind', 'meta ai', 'microsoft ai', 'nvidia ai', 'hugging face',
            'stable diffusion', 'midjourney', 'dall-e', 'ai chip', 'ai startup',
            'ai safety', 'ai regulation', 'ai ethics', 'transformer', 'diffusion model'
        ],
        'Economy': [
            'market', 'stock', 'shares', 'trading', 'investor', 'investment',
            'earnings', 'revenue', 'profit', 'quarterly results', 'financial',
            'banking', 'crypto', 'cryptocurrency', 'bitcoin', 'ethereum',
            'venture capital', 'funding round', 'valuation', 'bankruptcy',
            'recession', 'bull market', 'bear market', 'portfolio', 'hedge fund',
            'private equity', 'commodity', 'oil price', 'gold price', 'dollar',
            'euro', 'yuan', 'fiscal', 'monetary policy', 'central bank'
        ],
        'Politics': [
            'politics', 'political', 'democrat', 'republican', 'senator',
            'representative', 'governor', 'mayor', 'parliament', 'minister',
            'vote', 'voting', 'policy', 'regulation', 'law', 'legal',
            'justice', 'judge', 'attorney general', 'fbi', 'cia', 'pentagon',
            'nato', 'united nations', 'diplomacy', 'ambassador', 'summit',
            'protest', 'reform', 'bipartisan', 'filibuster', 'hearing'
        ]
    }

    def categorize(self, article):
        """Categorize a single article with priority weighting"""
        title = article['title'].lower()
        description = article['description'].lower()
        text = f"{title} {description}"

        # Calculate scores with priority weighting
        scores = {}
        for category in self.CATEGORIES.keys():
            score = 0

            # Priority keywords get 3x weight
            for keyword in self.PRIORITY_KEYWORDS.get(category, []):
                if keyword in text:
                    # Double weight if in title
                    score += 6 if keyword in title else 3

            # Regular keywords get 1x weight
            for keyword in self.CATEGORIES[category]:
                if keyword in text:
                    # Double weight if in title
                    score += 2 if keyword in title else 1

            scores[category] = score

        # Find category with highest score
        max_score = max(scores.values())

        # Require minimum score of 2 to avoid weak matches
        if max_score >= 2:
            for category, score in scores.items():
                if score == max_score:
                    return category

        return 'Other'

    def categorize_articles(self, articles):
        """Categorize a list of articles"""
        for article in articles:
            article['category'] = self.categorize(article)
        return articles
