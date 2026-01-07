"""Article Categorizer Module"""
import re

class ArticleCategorizer:
    """Categorizes articles based on intelligent keyword matching with word boundaries"""

    # Comprehensive keyword lists for accurate categorization
    KEYWORDS = {
        'AI': [
            # AI Companies and Labs
            r'\bopenai\b', r'\banthropic\b', r'\bdeepmind\b', r'\bmeta ai\b',
            r'\bgoogle ai\b', r'\bmicrosoft ai\b', r'\bnvidia ai\b',
            r'\bhugging face\b', r'\bstability ai\b', r'\bcohere\b',

            # AI Products and Models
            r'\bchatgpt\b', r'\bgpt-4\b', r'\bgpt-5\b', r'\bclaude\b',
            r'\bgemini\b', r'\bcopilot\b', r'\bllama\b', r'\bmistral\b',
            r'\bdall-e\b', r'\bmidjourney\b', r'\bstable diffusion\b',
            r'\bdeepseek\b', r'\bperplexity\b',

            # Core AI Terms
            r'\bartificial intelligence\b', r'\bmachine learning\b', r'\bdeep learning\b',
            r'\bneural network\b', r'\btransformer\b', r'\bllm\b', r'\bllms\b',
            r'\blarge language model\b', r'\bgenerative ai\b', r'\bfoundation model\b',

            # AI Technologies
            r'\bcomputer vision\b', r'\bnatural language processing\b', r'\bnlp\b',
            r'\breinforcement learning\b', r'\bsupervised learning\b',
            r'\bunsupervised learning\b', r'\bneural net\b',

            # AI Applications
            r'\bchatbot\b', r'\bai assistant\b', r'\bvoice assistant\b',
            r'\bautonomous vehicle\b', r'\bself-driving\b', r'\brobotics\b',
            r'\bai chip\b', r'\bai model\b', r'\bai system\b', r'\bai tool\b',

            # AI Concepts
            r'\bai safety\b', r'\bai ethics\b', r'\bai bias\b', r'\bai regulation\b',
            r'\bprompt engineering\b', r'\bai alignment\b', r'\bagi\b',
            r'\bai training\b', r'\bai inference\b', r'\bai hallucination\b',

            # Standalone AI (with context checking)
            r'\bai\s+(?:model|system|chip|tech|tool|bot|software|platform|startup|company|industry|sector|race|arms|boom|bubble|hype)\b',
            r'\b(?:developing|building|training|deploying|using)\s+ai\b'
        ],

        'Economy': [
            # Financial Institutions
            r'\bfederal reserve\b', r'\bthe fed\b', r'\bcentral bank\b',
            r'\bworld bank\b', r'\bimf\b', r'\btreasury\b', r'\bsec\b',
            r'\bwall street\b', r'\bgoldman sachs\b', r'\bjp morgan\b',
            r'\bmorgan stanley\b', r'\bciti(?:group|bank)\b',

            # Markets and Indices
            r'\bstock market\b', r'\bequity market\b', r'\bbond market\b',
            r'\bdow jones\b', r'\bnasdaq\b', r'\bs&p 500\b', r'\bnyse\b',
            r'\bftse\b', r'\bnikkei\b', r'\bhang seng\b',
            r'\bbull market\b', r'\bbear market\b', r'\bmarket rally\b',

            # Economic Indicators
            r'\binflation\b', r'\bdeflation\b', r'\bstagflation\b',
            r'\brecession\b', r'\bdepress(?:ion|ed economy)\b',
            r'\bgdp\b', r'\bgross domestic product\b',
            r'\bunemployment rate\b', r'\bjobs report\b', r'\bnonfarm payroll\b',
            r'\binterest rate\b', r'\bfed rate\b', r'\bconsumer price index\b',
            r'\bcpi\b', r'\bproducer price\b', r'\bhousing starts\b',
            r'\bconsumer confidence\b', r'\btrade deficit\b', r'\btrade surplus\b',

            # Financial Terms
            r'\bearnings\b', r'\bquarterly results\b', r'\bprofit\b', r'\brevenue\b',
            r'\bipo\b', r'\binitial public offering\b', r'\bmerger\b', r'\bacquisition\b',
            r'\btakeover\b', r'\bbuyout\b', r'\bdivestiture\b',
            r'\bbond yield\b', r'\btreasury yield\b', r'\byield curve\b',

            # Investment and Trading
            r'\bstock(?:s)?\b', r'\bshare(?:s)?\b', r'\bequit(?:y|ies)\b',
            r'\btrading\b', r'\btrader(?:s)?\b', r'\binvestor(?:s)?\b',
            r'\bhedge fund\b', r'\bprivate equity\b', r'\bventure capital\b',
            r'\bportfolio\b', r'\basset(?:s)?\b', r'\bcommodit(?:y|ies)\b',

            # Cryptocurrency
            r'\bbitcoin\b', r'\bethereum\b', r'\bcryptocurrency\b', r'\bcrypto\b',
            r'\bblockchain\b', r'\bdefi\b', r'\bnft\b', r'\bweb3\b',
            r'\bcoinbase\b', r'\bbinance\b', r'\bcrypto exchange\b',

            # Business Terms
            r'\bstartup\b', r'\bunicorn\b', r'\bfunding round\b',
            r'\bseries [a-z]\b', r'\bvaluation\b', r'\bbankruptcy\b',
            r'\blayoff(?:s)?\b', r'\bdownsizing\b', r'\brestructuring\b',

            # General Economic Terms
            r'\bmarket(?:s)?\b', r'\bfinancial\b', r'\beconomic\b', r'\beconomy\b',
            r'\bbusiness\b', r'\bcorporate\b', r'\bbanking\b', r'\bfinance\b',
            r'\bfiscal\b', r'\bmonetary\b', r'\bcapital\b', r'\binvestment\b',

            # Commodities and Resources
            r'\boil price\b', r'\bcrude oil\b', r'\bgold price\b', r'\bsilver\b',
            r'\bnatural gas\b', r'\bcommodity price\b', r'\benergy price\b',

            # Currency
            r'\bdollar\b', r'\beuro\b', r'\byen\b', r'\byuan\b', r'\bpound sterling\b',
            r'\bforex\b', r'\bcurrency\b', r'\bexchange rate\b'
        ],

        'Politics': [
            # US Government Institutions
            r'\bwhite house\b', r'\bcongress\b', r'\bsenate\b', r'\bhouse of representatives\b',
            r'\bsupreme court\b', r'\bstate department\b', r'\bpentagon\b',
            r'\bdepartment of defense\b', r'\bjustice department\b', r'\bdoj\b',
            r'\bhomeland security\b', r'\bfbi\b', r'\bcia\b', r'\bnsa\b',

            # Political Positions
            r'\bpresident\b', r'\bvice president\b', r'\bpresidential\b',
            r'\bsenator\b', r'\bcongressman\b', r'\bcongresswoman\b',
            r'\brepresentative\b', r'\bgovernor\b', r'\bmayor\b',
            r'\bcabinet\b', r'\bsecretary of state\b', r'\battorney general\b',

            # Political Parties and Ideology
            r'\bdemocrat(?:ic|s)?\b', r'\brepublican(?:s)?\b', r'\bgop\b',
            r'\bliberal\b', r'\bconservative\b', r'\bprogressive\b',
            r'\bbipartisan\b', r'\bpartisan\b', r'\bleft-wing\b', r'\bright-wing\b',

            # Elections and Campaigns
            r'\belection\b', r'\bpresidential election\b', r'\bmidterm\b',
            r'\bprimary\b', r'\bcaucus\b', r'\bballot\b', r'\bvot(?:e|ing|er)\b',
            r'\bcampaign\b', r'\bcampaign trail\b', r'\bcampaign finance\b',
            r'\bpoll(?:s|ing)?\b', r'\bpollster\b', r'\brunoff\b',

            # Legislative Actions
            r'\blegislation\b', r'\bbill\b', r'\blaw\b', r'\bstatute\b',
            r'\bveto\b', r'\bfilibuster\b', r'\bcloture\b',
            r'\bimpeachment\b', r'\bhearing\b', r'\btestimony\b',
            r'\bconfirmation\b', r'\bnominee\b', r'\bnomination\b',

            # Judicial
            r'\bcourt\b', r'\bjudge\b', r'\bjustice\b', r'\bruling\b',
            r'\bverdict\b', r'\btrial\b', r'\bappellate\b', r'\bjudicial\b',

            # International Politics
            r'\bnato\b', r'\bunited nations\b', r'\bu\.?n\.?\b', r'\bg7\b', r'\bg20\b',
            r'\bforeign policy\b', r'\bdiplomacy\b', r'\bdiplomatic\b',
            r'\bambassador\b', r'\benvoy\b', r'\bsummit\b', r'\btreaty\b',
            r'\bsanctions\b', r'\btariff(?:s)?\b', r'\btrade war\b',
            r'\bgeopolitical\b', r'\bgeopolitics\b',

            # General Political Terms
            r'\bpolitical\b', r'\bpolitics\b', r'\bgovernment\b',
            r'\bpolicy\b', r'\bregulation\b', r'\breform\b',
            r'\bprotest\b', r'\brally\b', r'\bdemonstration\b',
            r'\bactivis(?:t|m)\b', r'\badvocacy\b'
        ]
    }

    # Exclude patterns only for AI to prevent "daily", "said", etc.
    EXCLUDE_PATTERNS = {
        'AI': [
            r'\b(?:daily|laid|paid|said|wait|train|rain|gain|main|pain|straight|strain)\b'
        ]
    }

    def _has_ai_exclusion(self, text):
        """Check if text has AI exclusion patterns without AI context"""
        # Check for excluded words
        has_exclusion = any(re.search(pattern, text, re.IGNORECASE)
                           for pattern in self.EXCLUDE_PATTERNS['AI'])

        if not has_exclusion:
            return False

        # If we have exclusions, check if there's meaningful AI context
        # Check for compound AI terms or company names
        ai_context_patterns = [
            r'\bchatgpt\b', r'\bopenai\b', r'\banthropic\b', r'\bdeepseek\b',
            r'\bmachine learning\b', r'\bdeep learning\b', r'\bneural network\b',
            r'\bai\s+(?:model|system|chip|tech|tool|startup|company|training)\b',
            r'\bartificial intelligence\b', r'\bllm\b'
        ]

        has_ai_context = any(re.search(pattern, text, re.IGNORECASE)
                            for pattern in ai_context_patterns)

        return not has_ai_context

    def categorize(self, article):
        """Categorize a single article using comprehensive keyword matching"""
        title = article['title'].lower()
        description = article['description'].lower()
        text = f"{title} {description}"

        scores = {}

        for category in self.KEYWORDS.keys():
            score = 0

            # Skip AI category if we have exclusion patterns without AI context
            if category == 'AI' and self._has_ai_exclusion(text):
                scores[category] = 0
                continue

            # Score each keyword match
            for keyword_pattern in self.KEYWORDS[category]:
                # Count matches in full text
                matches = len(re.findall(keyword_pattern, text, re.IGNORECASE))
                if matches > 0:
                    # Check if keyword appears in title (more important)
                    title_matches = len(re.findall(keyword_pattern, title, re.IGNORECASE))

                    # Title matches get 3 points, description matches get 1 point
                    score += (3 * title_matches) + (1 * (matches - title_matches))

            scores[category] = score

        # Find category with highest score
        max_score = max(scores.values())

        # Require minimum score of 2 to avoid weak categorization
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
