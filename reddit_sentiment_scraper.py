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
import seaborn as sns

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
                # Get comments for the post
                post.comments.replace_more(limit=0)  # Remove MoreComments objects
                comments = [comment.body for comment in post.comments.list()]
                
                posts.append({
                    'title': post.title,
                    'text': post.selftext,
                    'score': post.score,
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'subreddit': subreddit.display_name,
                    'comments': comments,
                    'num_comments': len(comments)
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
    text = ' '.join(df['title'] + ' ' + df['text'])
    text = re.sub(r'\b[A-Z]{1,5}\b', '', text)
    text = re.sub(r'\b\w{1,2}\b', '', text)
    
    wordcloud = WordCloud(width=1600, height=800, background_color='white').generate(text)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Reddit Posts')
    plt.tight_layout()
    plt.show()

def analyze_post_volume(df):
    """Analyze and visualize post volume over time."""
    daily_posts = df.groupby(df['created_utc'].dt.date).size()
    
    plt.figure(figsize=(12, 6))
    daily_posts.plot(kind='bar')
    plt.title('Daily Post Volume')
    plt.xlabel('Date')
    plt.ylabel('Number of Posts')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def analyze_subreddit_distribution(df):
    """Analyze and visualize post distribution across subreddits."""
    subreddit_counts = df['subreddit'].value_counts()
    
    plt.figure(figsize=(10, 6))
    plt.pie(subreddit_counts, labels=subreddit_counts.index, autopct='%1.1f%%')
    plt.title('Post Distribution Across Subreddits')
    plt.axis('equal')
    plt.show()

def analyze_top_posts(df):
    """Analyze and display top posts by score."""
    top_posts = df.nlargest(5, 'score')[['title', 'score', 'sentiment']]
    
    print("\nTop 5 Posts by Score:")
    print("=" * 50)
    for _, post in top_posts.iterrows():
        print(f"\nTitle: {post['title']}")
        print(f"Score: {post['score']}")
        print(f"Sentiment: {post['sentiment']:.2f}")
        print("-" * 50)

def analyze_comment_sentiment(df):
    """Analyze sentiment of comments for each post."""
    df['comment_sentiment'] = df['comments'].apply(
        lambda x: sum(analyze_sentiment(comment) for comment in x) / len(x) if x else 0
    )
    
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='subreddit', y='comment_sentiment', data=df)
    plt.title('Comment Sentiment by Subreddit')
    plt.xlabel('Subreddit')
    plt.ylabel('Average Comment Sentiment')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def analyze_time_distribution(df):
    """Analyze and visualize post distribution by hour of day."""
    df['hour'] = df['created_utc'].dt.hour
    hourly_posts = df.groupby('hour').size()
    
    plt.figure(figsize=(12, 6))
    hourly_posts.plot(kind='bar')
    plt.title('Post Distribution by Hour of Day')
    plt.xlabel('Hour of Day (UTC)')
    plt.ylabel('Number of Posts')
    plt.grid(True)
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
    
    # Calculate sentiment for all posts
    df['sentiment'] = df['text'].apply(analyze_sentiment)
    
    # Display all analyses
    print("\nGenerating visualizations and analyses...")
    
    # 1. Sentiment Trend
    print("\n1. Generating sentiment trend graph...")
    create_sentiment_trend(df)
    
    # 2. Word Cloud
    print("2. Generating word cloud...")
    create_wordcloud(df)
    
    # 3. Post Volume Analysis
    print("3. Analyzing post volume...")
    analyze_post_volume(df)
    
    # 4. Subreddit Distribution
    print("4. Analyzing subreddit distribution...")
    analyze_subreddit_distribution(df)
    
    # 5. Top Posts Analysis
    print("5. Analyzing top posts...")
    analyze_top_posts(df)
    
    # 6. Comment Sentiment Analysis
    print("6. Analyzing comment sentiment...")
    analyze_comment_sentiment(df)
    
    # 7. Time Distribution Analysis
    print("7. Analyzing time distribution...")
    analyze_time_distribution(df)
    
    print("\nAnalysis complete! All visualizations have been generated.")

if __name__ == "__main__":
    main() 