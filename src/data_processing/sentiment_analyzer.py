"""
Sentiment Analysis Module
Analyzes sentiment of ESG-related news articles
"""

from transformers import pipeline
from textblob import TextBlob
import nltk
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyzes sentiment of ESG news articles"""
    
    def __init__(self):
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            
            # Initialize Hugging Face sentiment pipeline
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
        except Exception as e:
            logger.warning(f"Could not initialize sentiment pipeline: {e}")
            self.sentiment_pipeline = None
    
    def analyze_textblob_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using TextBlob"""
        try:
            blob = TextBlob(text)
            
            # Get polarity (-1 to 1) and subjectivity (0 to 1)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Convert polarity to sentiment label
            if polarity > 0.1:
                sentiment_label = "positive"
            elif polarity < -0.1:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            return {
                "sentiment_score": polarity,
                "sentiment_label": sentiment_label,
                "subjectivity": subjectivity,
                "method": "textblob"
            }
        except Exception as e:
            logger.error(f"Error in TextBlob sentiment analysis: {e}")
            return {
                "sentiment_score": 0.0,
                "sentiment_label": "neutral",
                "subjectivity": 0.0,
                "method": "textblob_error"
            }
    
    def analyze_huggingface_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using Hugging Face transformers"""
        if not self.sentiment_pipeline:
            return self.analyze_textblob_sentiment(text)
        
        try:
            # Truncate text if too long
            if len(text) > 500:
                text = text[:500]
            
            results = self.sentiment_pipeline(text)
            
            # Extract scores
            scores = results[0]
            positive_score = next((score['score'] for score in scores if score['label'] == 'positive'), 0)
            negative_score = next((score['score'] for score in scores if score['label'] == 'negative'), 0)
            neutral_score = next((score['score'] for score in scores if score['label'] == 'neutral'), 0)
            
            # Calculate overall sentiment
            sentiment_score = positive_score - negative_score
            
            # Determine label
            if positive_score > negative_score and positive_score > neutral_score:
                sentiment_label = "positive"
            elif negative_score > positive_score and negative_score > neutral_score:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            return {
                "sentiment_score": sentiment_score,
                "sentiment_label": sentiment_label,
                "positive_score": positive_score,
                "negative_score": negative_score,
                "neutral_score": neutral_score,
                "method": "huggingface"
            }
        except Exception as e:
            logger.error(f"Error in Hugging Face sentiment analysis: {e}")
            return self.analyze_textblob_sentiment(text)
    
    def analyze_esg_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment with ESG-specific considerations"""
        # First get general sentiment
        sentiment = self.analyze_huggingface_sentiment(text)
        
        # Add ESG-specific analysis
        esg_keywords = {
            "positive": [
                "sustainability", "renewable", "green", "carbon neutral", "diversity",
                "inclusion", "transparency", "governance", "ethical", "responsible"
            ],
            "negative": [
                "pollution", "emissions", "controversy", "scandal", "violation",
                "fined", "investigation", "corruption", "discrimination"
            ]
        }
        
        text_lower = text.lower()
        esg_bonus = 0.0
        
        # Check for positive ESG keywords
        for keyword in esg_keywords["positive"]:
            if keyword in text_lower:
                esg_bonus += 0.1
        
        # Check for negative ESG keywords
        for keyword in esg_keywords["negative"]:
            if keyword in text_lower:
                esg_bonus -= 0.1
        
        # Adjust sentiment score
        adjusted_score = max(-1.0, min(1.0, sentiment["sentiment_score"] + esg_bonus))
        
        # Update sentiment label if needed
        if adjusted_score > 0.1:
            adjusted_label = "positive"
        elif adjusted_score < -0.1:
            adjusted_label = "negative"
        else:
            adjusted_label = "neutral"
        
        return {
            **sentiment,
            "sentiment_score": adjusted_score,
            "sentiment_label": adjusted_label,
            "esg_bonus": esg_bonus,
            "method": "esg_enhanced"
        }
    
    def analyze_news_batch(self, news_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze sentiment for a batch of news articles"""
        analyzed_news = []
        
        for article in news_articles:
            try:
                # Combine headline and content for analysis
                text = f"{article.get('headline', '')} {article.get('content', '')}"
                
                # Analyze sentiment
                sentiment_result = self.analyze_esg_sentiment(text)
                
                # Update article with sentiment data
                article.update({
                    "sentiment_score": sentiment_result["sentiment_score"],
                    "sentiment_label": sentiment_result["sentiment_label"],
                    "sentiment_method": sentiment_result["method"]
                })
                
                analyzed_news.append(article)
                
            except Exception as e:
                logger.error(f"Error analyzing sentiment for article: {e}")
                # Keep article with neutral sentiment
                article.update({
                    "sentiment_score": 0.0,
                    "sentiment_label": "neutral",
                    "sentiment_method": "error"
                })
                analyzed_news.append(article)
        
        return analyzed_news
