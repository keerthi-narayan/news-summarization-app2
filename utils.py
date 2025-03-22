import requests
from transformers import pipeline
from gtts import gTTS
import os
from collections import defaultdict
from functools import lru_cache

# Replace with your NewsAPI key
NEWS_API_KEY = "019f817f43fb4786ae786a1666eb80f0"

# Load sentiment analysis and summarization models once
@lru_cache(maxsize=1)
def load_models():
    try:
        sentiment_pipeline = pipeline("sentiment-analysis")
        summarizer = pipeline("summarization")
        return sentiment_pipeline, summarizer
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None

# Cache API calls to NewsAPI
@lru_cache(maxsize=100)
def scrape_news(company_name):
    try:
        if not company_name:
            raise ValueError("Company name cannot be empty.")
        
        # Fetch news articles from NewsAPI
        url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the JSON response
        data = response.json()
        articles = []
        
        # Extract relevant information
        for article in data.get("articles", [])[:2]:
            title = article.get("title", "No title")
            summary = article.get("description", "No summary")
            articles.append({"title": title, "summary": summary})
        
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from NewsAPI: {e}")
        return []
    except ValueError as e:
        print(f"Invalid input: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in scrape_news: {e}")
        return []

def analyze_sentiment(text, sentiment_pipeline):
    try:
        if not text:
            return "Neutral"
        result = sentiment_pipeline(text)
        return result[0]['label']
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "Neutral"

def extract_topics(text, summarizer):
    try:
        if not text:
            return "No topics extracted"
        summary = summarizer(text, max_length=30, min_length=10, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error extracting topics: {e}")
        return "No topics extracted"

# Cache TTS generation
@lru_cache(maxsize=100)
def generate_tts(text, language='hi', output_file="output.mp3"):
    try:
        if not text:
            raise ValueError("Text for TTS cannot be empty.")
        
        # Create the TTS object
        tts = gTTS(text=text, lang=language)
        
        # Save the audio file to a specific location
        tts.save(output_file)
        
        # Return the file path for playback
        return output_file
    except ValueError as e:
        print(f"Invalid input for TTS: {e}")
        return None
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None

def perform_comparative_analysis(articles):
    try:
        if not articles or len(articles) < 2:
            raise ValueError("At least 2 articles are required for comparison.")
        
        comparisons = []
        for i in range(len(articles) - 1):
            article1 = articles[i]
            article2 = articles[i + 1]
            
            comparison = {
                "Comparison": f"Article {i + 1} highlights {article1['title']}, while Article {i + 2} discusses {article2['title']}.",
                "Impact": f"The first article boosts confidence in {article1['title']}, while the second raises concerns about {article2['title']}."
            }
            comparisons.append(comparison)
        return comparisons
    except ValueError as e:
        print(f"Error in comparative analysis: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in perform_comparative_analysis: {e}")
        return []

def analyze_topic_overlap(articles, summarizer):
    try:
        if not articles or len(articles) < 2:
            raise ValueError("At least 2 articles are required for topic overlap analysis.")
        
        topics = defaultdict(list)
        for i, article in enumerate(articles):
            topics[f"Article {i + 1}"] = extract_topics(article['summary'], summarizer).split(", ")
        
        common_topics = set(topics["Article 1"]).intersection(*[set(topics[key]) for key in topics])
        unique_topics = {}
        for key in topics:
            unique_topics[key] = set(topics[key]) - common_topics
        
        return {
            "Common Topics": list(common_topics),
            "Unique Topics": unique_topics
        }
    except ValueError as e:
        print(f"Error in topic overlap analysis: {e}")
        return {"Common Topics": [], "Unique Topics": {}}
    except Exception as e:
        print(f"Unexpected error in analyze_topic_overlap: {e}")
        return {"Common Topics": [], "Unique Topics": {}}

def translate_to_hindi(text):
    try:
        if not text:
            raise ValueError("Text for translation cannot be empty.")
        
        # Simple translation mapping for key phrases
        translation_map = {
            "latest news coverage is mostly positive.": "नवीनतम समाचार कवरेज ज्यादातर सकारात्मक है।",
            "latest news coverage is mostly negative.": "नवीनतम समाचार कवरेज ज्यादातर नकारात्मक है।",
            "latest news coverage is neutral.": "नवीनतम समाचार कवरेज तटस्थ है।",
            "Out of": "कुल",
            "articles": "लेख",
            "are positive": "सकारात्मक हैं",
            "are negative": "नकारात्मक हैं",
            "are neutral": "तटस्थ हैं",
            "Potential stock growth expected.": "संभावित स्टॉक वृद्धि की उम्मीद है।",
            "Potential stock decline expected.": "संभावित स्टॉक गिरावट की उम्मीद है।",
            "Stock performance is uncertain.": "स्टॉक प्रदर्शन अनिश्चित है।"
        }
        
        # Replace English phrases with Hindi translations
        for english, hindi in translation_map.items():
            text = text.replace(english, hindi)
        
        return text
    except ValueError as e:
        print(f"Invalid input for translation: {e}")
        return ""
    except Exception as e:
        print(f"Error in translation: {e}")
        return ""