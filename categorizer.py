"""Article Categorizer Module"""
import re

class ArticleCategorizer:
    """Categorizes articles based on intelligent keyword matching with word boundaries"""

    # High-priority keywords that strongly indicate a category
    PRIORITY_KEYWORDS = {
        'AI': [
            # AI company names and products (very strong indicators)
            r'\bchatgpt\b', r'\bopenai\b', r'\banthropic\b', r'\bclaude\b',
            r'\bgemini\b', r'\bcopilot\b', r'\bgpt-4\b', r'\bgpt-5\b',
            r'\bdeepseek\b', r'\bdeepmind\b', r'\bllm\b', r'\bllms\b',

            # Core AI concepts (compound only to avoid false positives)
            r'\bartificial intelligence\b', r'\blarge language model\b',
            r'\bgenerative ai\b', r'\bmachine learning\b', r'\bdeep learning\b',
            r'\bneural network\b', r'\btransformer model\b'
        ],
        'Economy': [
            # Major financial institutions and terms
            r'\bfederal reserve\b', r'\bfed\b', r'\bwall street\b',
            r'\bdow jones\b', r'\bnasdaq\b', r'\bs&p 500\b',
            r'\bstock market\b', r'\bipo\b', r'\bearnings\b',
            r'\binflation\b', r'\brecession\b', r'\bgdp\b',
            r'\bbitcoin\b', r'\bethereum\b', r'\bcrypto\b',
            r'\bventure capital\b', r'\bstartup\b', r'\bmerger\b'
        ],
        'Politics': [
            # Government and political terms
            r'\bwhite house\b', r'\bcongress\b', r'\bsenate\b',
            r'\bsupreme court\b', r'\bpresident\b', r'\bpresidential\b',
            r'\belection\b', r'\bcampaign\b', r'\blegislation\b',
            r'\bnato\b', r'\bunited nations\b', r'\bpentagon\b'
        ]
    }

    # Regular keywords - broader terms that support categorization
    CATEGORIES = {
        'AI': [
            # AI terms (using word boundaries but more permissive)
            r'\b(?:ai|a\.i\.)\b(?:\s+(?:model|system|chip|tech|tool|bot|software|platform|startup|company))?',
            r'\bchatbot\b', r'\brobot(?:ics)?\b', r'\bautomation\b',
            r'\bcomputer vision\b', r'\bneural\b', r'\balgorithm\b',
            r'\b(?:nvidia|microsoft|google|meta)\s+ai\b',
            r'\bai\s+(?:regulation|safety|ethics|bias|model|chip|training|startup)\b'
        ],
        'Economy': [
            # Business and finance terms
            r'\bmarket(?:s)?\b', r'\bstock(?:s)?\b', r'\bshare(?:s)?\b',
            r'\btrading\b', r'\binvestor(?:s)?\b', r'\binvestment\b',
            r'\bfinancial\b', r'\bbusiness\b', r'\bcorporate\b',
            r'\beconomic\b', r'\beconomy\b', r'\bbanking\b',
            r'\bcryptocurrency\b', r'\bfunding\b', r'\bvaluation\b'
        ],
        'Politics': [
            # Political terms
            r'\bpolitical\b', r'\bpolitics\b', r'\bgovernment\b',
            r'\bsenator\b', r'\bcongressman\b', r'\bcongresswoman\b',
            r'\brepresentative\b', r'\bgovernor\b', r'\bmayor\b',
            r'\bdemocrat\b', r'\brepublican\b', r'\bvot(?:e|ing)\b',
            r'\bpolicy\b', r'\blaw\b', r'\bcourt\b', r'\bjudge\b'
        ]
    }

    # Only exclude for AI category and only if no other AI context exists
    EXCLUDE_PATTERNS = {
        'AI': [
            r'\b(?:daily|laid|paid|said|wait|train|rain|gain|main|pain)\b'
        ]
    }

    def _has_ai_exclusion(self, text):
        """Check if text has AI exclusion patterns without AI context"""
        # Check for excluded words
        has_exclusion = any(re.search(pattern, text, re.IGNORECASE)
                           for pattern in self.EXCLUDE_PATTERNS['AI'])

        if not has_exclusion:
            return False

        # If we have exclusions, check if there's any AI context
        # If there are priority AI keywords, ignore the exclusion
        has_ai_context = any(re.search(pattern, text, re.IGNORECASE)
                            for pattern in self.PRIORITY_KEYWORDS['AI'])

        # Also check for compound AI phrases in regular keywords
        has_ai_compound = bool(re.search(r'\bai\s+(?:model|system|chip|tech|tool|startup|company)\b',
                                        text, re.IGNORECASE))

        return not (has_ai_context or has_ai_compound)

    def categorize(self, article):
        """Categorize a single article with intelligent pattern matching"""
        title = article['title'].lower()
        description = article['description'].lower()
        text = f"{title} {description}"

        scores = {}

        for category in self.CATEGORIES.keys():
            score = 0

            # Skip AI category if we have exclusion patterns without AI context
            if category == 'AI' and self._has_ai_exclusion(text):
                scores[category] = 0
                continue

            # Priority keywords get higher weight
            for keyword_pattern in self.PRIORITY_KEYWORDS.get(category, []):
                matches = len(re.findall(keyword_pattern, text, re.IGNORECASE))
                if matches > 0:
                    title_matches = len(re.findall(keyword_pattern, title, re.IGNORECASE))
                    # Priority: 5 points base, 10 if in title
                    score += (10 * title_matches) + (5 * (matches - title_matches))

            # Regular keywords
            for keyword_pattern in self.CATEGORIES[category]:
                matches = len(re.findall(keyword_pattern, text, re.IGNORECASE))
                if matches > 0:
                    title_matches = len(re.findall(keyword_pattern, title, re.IGNORECASE))
                    # Regular: 2 points base, 4 if in title
                    score += (4 * title_matches) + (2 * (matches - title_matches))

            scores[category] = score

        # Find highest score
        max_score = max(scores.values())

        # Much lower threshold - just need SOME evidence
        if max_score >= 2:
            # Return highest scoring category
            for category, score in scores.items():
                if score == max_score:
                    return category

        return 'Other'

    def categorize_articles(self, articles):
        """Categorize a list of articles"""
        for article in articles:
            article['category'] = self.categorize(article)
        return articles
