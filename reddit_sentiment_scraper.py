import os
import praw
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import nltk
from dotenv import load_dotenv
import re

# Download required NLTK data
nltk.download('vader_lexicon')

# Load environment variables
load_dotenv()

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

# Stock-related subreddits
SUBREDDITS = ['wallstreetbets', 'stocks', 'investing']

def get_posts(stock_symbol):
    """Fetch posts from subreddits containing the stock symbol."""
    posts = []
    cutoff_date = datetime.utcnow() - timedelta(days=7)
    
    for subreddit in SUBREDDITS:
        subreddit = reddit.subreddit(subreddit)
        for post in subreddit.search(stock_symbol, time_filter='week'):
            if datetime.fromtimestamp(post.created_utc) >= cutoff_date:
                posts.append({
                    'title': post.title,
                    'text': post.selftext,
                    'score': post.score,
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'subreddit': subreddit.display_name
                })
    
    return pd.DataFrame(posts)

def analyze_sentiment(text):
    """Perform sentiment analysis on text."""
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)['compound']

def create_sentiment_trend(df):
    """Create a sentiment trend graph."""
    df['sentiment'] = df['text'].apply(analyze_sentiment)
    daily_sentiment = df.groupby(df['created_utc'].dt.date)['sentiment'].mean()
    
    plt.figure(figsize=(12, 6))
    daily_sentiment.plot(kind='line', marker='o')
    plt.title('7-Day Sentiment Trend')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def create_wordcloud(df):
    """Create a word cloud from post titles and text."""
    # Combine titles and text
    text = ' '.join(df['title'] + ' ' + df['text'])
    
    # Remove common words and stock symbols
    text = re.sub(r'\b[A-Z]{1,5}\b', '', text)  # Remove stock symbols
    text = re.sub(r'\b\w{1,2}\b', '', text)     # Remove 1-2 letter words
    
    wordcloud = WordCloud(width=1600, height=800, background_color='white').generate(text)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Reddit Posts')
    plt.tight_layout()
    plt.show()

def main():
    stock_symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
    
    print(f"Fetching posts about {stock_symbol}...")
    df = get_posts(stock_symbol)
    
    if df.empty:
        print("No posts found for the specified stock symbol.")
        return
    
    print(f"Found {len(df)} posts. Analyzing sentiment...")
    create_sentiment_trend(df)
    
    print("Generating word cloud...")
    create_wordcloud(df)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main() 