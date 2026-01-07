"""Article Categorizer Module"""
import re

class ArticleCategorizer:
    """Categorizes articles based on intelligent keyword matching with word boundaries"""

    # High-priority keywords that strongly indicate a category
    # Using word boundaries to avoid false matches like "ai" in "laid", "said", etc.
    PRIORITY_KEYWORDS = {
        'AI': [
            # Company names and products (strong indicators)
            r'\bchatgpt\b', r'\bopenai\b', r'\banthropic\b', r'\bclaude ai\b',
            r'\bgemini ai\b', r'\bcopilot ai\b', r'\bgpt-4\b', r'\bgpt-5\b',
            r'\bdeepseek\b', r'\bdeepmind\b', r'\bmeta ai\b',

            # Technical AI terms (specific)
            r'\bllm\b', r'\bllms\b', r'\blarge language model\b',
            r'\bgenerative ai\b', r'\bdeep learning\b', r'\bneural network\b',
            r'\bmachine learning model\b', r'\bai model\b', r'\bai system\b',
            r'\blanguage model\b', r'\btransformer model\b',

            # AI in specific contexts (compound phrases)
            r'\bartificial intelligence\b', r'\bai chip\b', r'\bai training\b',
            r'\bai startup\b', r'\bai regulation\b', r'\bai safety\b'
        ],
        'Economy': [
            # Financial institutions
            r'\bfederal reserve\b', r'\bfed rate\b', r'\bcentral bank\b',
            r'\bwall street\b', r'\btreasury\b', r'\bsec \b', r'\bs&p 500\b',

            # Markets and indices
            r'\bstock market\b', r'\bdow jones\b', r'\bnasdaq\b',
            r'\bnyse\b', r'\bbull market\b', r'\bbear market\b',

            # Economic indicators
            r'\binflation rate\b', r'\binterest rate\b', r'\bunemployment rate\b',
            r'\bgdp growth\b', r'\bjobs report\b', r'\bconsumer price\b',
            r'\bbond yield\b', r'\btrade deficit\b',

            # Corporate finance
            r'\bipo\b', r'\bmerger\b', r'\bacquisition\b', r'\bearnings report\b',
            r'\bquarterly results\b', r'\bventure capital\b'
        ],
        'Politics': [
            # Government institutions
            r'\bwhite house\b', r'\bcongress\b', r'\bsenate\b',
            r'\bhouse of representatives\b', r'\bsupreme court\b',
            r'\bstate department\b', r'\bpentagon\b',

            # Political events
            r'\bpresidential election\b', r'\bcampaign trail\b',
            r'\belection 2024\b', r'\belection 2026\b', r'\bballot\b',

            # Political actions
            r'\blegislation\b', r'\bbill passes\b', r'\bveto\b',
            r'\bimpeachment\b', r'\bfilibuster\b', r'\bhearing\b',

            # International politics
            r'\bforeign policy\b', r'\bsanctions\b', r'\btreaty\b',
            r'\bunited nations\b', r'\bnato\b'
        ]
    }

    # Regular keywords for additional matching with word boundaries
    CATEGORIES = {
        'AI': [
            # AI-specific terms (safe from false positives)
            r'\bchatbot\b', r'\bcomputer vision\b', r'\bnatural language processing\b',
            r'\bnlp model\b', r'\brobotics ai\b', r'\bautonomous vehicle\b',
            r'\bneural net\b', r'\bmachine learning\b',

            # AI companies and products
            r'\bhugging face\b', r'\bstable diffusion\b', r'\bmidjourney\b',
            r'\bdall-e\b', r'\bnvidia ai\b', r'\bmicrosoft ai\b',

            # AI concepts
            r'\bai ethics\b', r'\bai bias\b', r'\bai alignment\b',
            r'\bai hallucination\b', r'\bprompt engineering\b',
            r'\bdiffusion model\b', r'\bfoundation model\b'
        ],
        'Economy': [
            # Financial terms (with boundaries to avoid false matches)
            r'\bstock price\b', r'\bshare price\b', r'\btrading volume\b',
            r'\bmarket cap\b', r'\bmarket capitalization\b',

            # Crypto (specific)
            r'\bbitcoin\b', r'\bethereum\b', r'\bcryptocurrency\b',
            r'\bcrypto market\b', r'\bcrypto exchange\b',

            # Business/Finance
            r'\bhedge fund\b', r'\bprivate equity\b', r'\bfunding round\b',
            r'\bvaluation\b', r'\bbankruptcy filing\b', r'\brecession\b',

            # Commodities
            r'\boil price\b', r'\bgold price\b', r'\bcommodity\b',

            # Currency
            r'\bdollar index\b', r'\beuro\b', r'\byuan\b', r'\bforex\b',

            # Economic policy
            r'\bmonetary policy\b', r'\bfiscal policy\b', r'\btax policy\b'
        ],
        'Politics': [
            # Political figures and parties
            r'\bsenator\b', r'\bcongressman\b', r'\bcongresswoman\b',
            r'\brepresentative\b', r'\bgovernor\b', r'\bmayor\b',
            r'\bdemocrat\b', r'\brepublican\b', r'\bbipartisan\b',

            # Political processes
            r'\bvoting\b', r'\bprimary election\b', r'\bgeneral election\b',
            r'\bpolitical campaign\b', r'\bpoll\b', r'\bpolitical party\b',

            # Government agencies
            r'\bfbi\b', r'\bcia\b', r'\bfema\b', r'\bepa\b',

            # Legal/Judicial
            r'\battorney general\b', r'\bjudge\b', r'\bcourt ruling\b',
            r'\bjustice\b',

            # International
            r'\bambassador\b', r'\bsummit\b', r'\bdiplomacy\b',
            r'\bdiplomatic\b', r'\bgeopolitical\b'
        ]
    }

    # Excluded patterns - terms that often cause false positives
    EXCLUDE_PATTERNS = {
        'AI': [
            r'\bdaily\b', r'\blaid\b', r'\bpaid\b', r'\bsaid\b',
            r'\bwait\b', r'\bchain\b', r'\btrain\b', r'\brain\b',
            r'\bgain\b', r'\bmain\b', r'\bpain\b'
        ]
    }

    def categorize(self, article):
        """Categorize a single article with intelligent pattern matching"""
        title = article['title'].lower()
        description = article['description'].lower()
        text = f"{title} {description}"

        # Calculate scores with priority weighting
        scores = {}
        for category in self.CATEGORIES.keys():
            score = 0

            # Check for excluded patterns first (for AI category)
            if category in self.EXCLUDE_PATTERNS:
                excluded = False
                for exclude_pattern in self.EXCLUDE_PATTERNS[category]:
                    if re.search(exclude_pattern, text, re.IGNORECASE):
                        # If we find excluded terms, check if there are strong AI indicators
                        # Only exclude if there are no priority keywords
                        priority_matches = sum(1 for kw in self.PRIORITY_KEYWORDS.get(category, [])
                                             if re.search(kw, text, re.IGNORECASE))
                        if priority_matches == 0:
                            excluded = True
                            break

                if excluded:
                    continue

            # Priority keywords get 3x weight (using regex with word boundaries)
            for keyword_pattern in self.PRIORITY_KEYWORDS.get(category, []):
                matches = len(re.findall(keyword_pattern, text, re.IGNORECASE))
                if matches > 0:
                    # Check if in title for extra weight
                    title_matches = len(re.findall(keyword_pattern, title, re.IGNORECASE))
                    score += (6 * title_matches) + (3 * (matches - title_matches))

            # Regular keywords get 1x weight (using regex with word boundaries)
            for keyword_pattern in self.CATEGORIES[category]:
                matches = len(re.findall(keyword_pattern, text, re.IGNORECASE))
                if matches > 0:
                    # Check if in title for extra weight
                    title_matches = len(re.findall(keyword_pattern, title, re.IGNORECASE))
                    score += (2 * title_matches) + (1 * (matches - title_matches))

            scores[category] = score

        # Find category with highest score
        max_score = max(scores.values())

        # Require minimum score of 3 to avoid weak matches (increased from 2)
        if max_score >= 3:
            for category, score in scores.items():
                if score == max_score:
                    return category

        return 'Other'

    def categorize_articles(self, articles):
        """Categorize a list of articles"""
        for article in articles:
            article['category'] = self.categorize(article)
        return articles
