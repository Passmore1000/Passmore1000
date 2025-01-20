import os
import tweepy
import re

def update_readme_with_tweets():
    # Twitter API authentication
    auth = tweepy.OAuthHandler(
        os.environ['TWITTER_API_KEY'],
        os.environ['TWITTER_API_SECRET']
    )
    auth.set_access_token(
        os.environ['TWITTER_ACCESS_TOKEN'],
        os.environ['TWITTER_ACCESS_SECRET']
    )
    
    api = tweepy.API(auth)
    
    # Get recent tweets
    tweets = api.user_timeline(count=5, tweet_mode="extended", exclude_replies=True)
    
    # Format tweets for README
    tweet_lines = []
    for tweet in tweets:
        text = tweet.full_text
        text = re.sub(r'https://\S+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = ' '.join(text.split())
        
        tweet_url = f"https://twitter.com/username/status/{tweet.id}"
        tweet_lines.append(f"- [{text}]({tweet_url})")
    
    # Read README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace tweets section
    start_marker = "<!-- TWEETS-START -->"
    end_marker = "<!-- TWEETS-END -->"
    
    new_content = content.split(start_marker)[0] + start_marker + "\n"
    new_content += "\n".join(tweet_lines) + "\n"
    new_content += end_marker + content.split(end_marker)[1]
    
    # Write updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme_with_tweets()
