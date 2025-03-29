# Reddit Stock Sentiment Scraper

A powerful Python-based tool that analyzes sentiment trends and generates insights from Reddit discussions about specific stocks. This tool helps investors and analysts understand market sentiment by analyzing posts from popular stock-related subreddits.

## Features

- **Reddit Data Collection**: Scrapes posts from multiple stock-related subreddits (wallstreetbets, stocks, investing)
- **Time-Based Analysis**: Focuses on posts from the last 7 days for current market sentiment
- **Sentiment Analysis**: Uses NLTK's VADER sentiment analyzer to evaluate post sentiment
- **Visualization**:
  - 7-day sentiment trend graph showing average sentiment over time
  - Word cloud visualization of common terms in discussions
  - Daily post volume analysis
  - Subreddit distribution pie chart
  - Comment sentiment analysis by subreddit
  - Time of day distribution analysis
- **Smart Text Processing**: 
  - Removes stock symbols and short words from word clouds
  - Combines post titles and content for comprehensive analysis
- **Top Posts Analysis**: Displays highest scoring posts with their sentiment scores

## Technical Details

The program uses several key technologies:
- **PRAW**: Python Reddit API Wrapper for Reddit data collection
- **NLTK**: Natural Language Toolkit for sentiment analysis
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **WordCloud**: Text visualization
- **python-dotenv**: Environment variable management
- **Seaborn**: Advanced statistical visualizations

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your Reddit API credentials:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

### Getting Reddit API Credentials:
1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app..."
3. Select "script"
4. Fill in the required information:
   - Name: RedditSentimentScraper
   - Description: A script to analyze Reddit sentiment for stocks
   - About URL: (can be left blank)
   - Redirect URI: http://localhost:8080
5. Copy the client ID and client secret

## Usage

Run the script:
```bash
python reddit_sentiment_scraper.py
```

Enter the stock symbol when prompted (e.g., AAPL, GOOGL, MSFT).

The script will:
1. Scrape posts from the last 7 days from stock-related subreddits
2. Perform sentiment analysis on the posts
3. Generate a sentiment trend graph
4. Create a word cloud from the posts
5. Display both visualizations

## Output

The program generates seven main analyses:

1. **Sentiment Trend Graph**: Shows the average sentiment score over the 7-day period
   - Positive values indicate bullish sentiment
   - Negative values indicate bearish sentiment
   - Values closer to zero indicate neutral sentiment

2. **Word Cloud**: Displays the most frequently used terms in the discussions
   - Larger words indicate more frequent usage
   - Stock symbols and short words are automatically filtered out

3. **Post Volume Analysis**: Bar chart showing the number of posts per day
   - Helps identify days with high discussion activity
   - Useful for tracking discussion momentum

4. **Subreddit Distribution**: Pie chart showing post distribution across subreddits
   - Helps understand which communities are most active
   - Shows relative importance of different subreddits

5. **Top Posts Analysis**: Displays the 5 highest-scoring posts
   - Shows post title, score, and sentiment
   - Helps identify most impactful discussions

6. **Comment Sentiment Analysis**: Box plot showing sentiment distribution of comments by subreddit
   - Compares comment sentiment across different subreddits
   - Helps identify which communities are more bullish/bearish

7. **Time Distribution Analysis**: Bar chart showing post activity by hour
   - Helps identify peak discussion times
   - Useful for understanding when the community is most active

## Limitations

- Reddit API rate limits may affect data collection
- Sentiment analysis accuracy depends on the quality and context of the posts
- Results may be skewed by meme stocks or highly volatile discussions
- Limited to publicly available Reddit data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 RedditSentimentScraper

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Disclaimer

This tool is for educational and research purposes only. The sentiment analysis and insights provided should not be considered financial advice. Always conduct your own research and consult with financial professionals before making investment decisions. 