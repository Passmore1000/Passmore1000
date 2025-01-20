import os
import tweepy
import re

def update_readme_with_tweets():
    # Twitter API v1.1 authentication
    auth = tweepy.OAuth1UserHandler(
        os.environ['TWITTER_API_KEY'],
        os.environ['TWITTER_API_SECRET'],
        os.environ['TWITTER_ACCESS_TOKEN'],
        os.environ['TWITTER_ACCESS_SECRET']
    )
    
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    try:
        # Get recent tweets
        tweets = api.user_timeline(count=5, tweet_mode="extended", exclude_replies=True)
        
        # Format tweets for README
        tweet_lines = []
        for tweet in tweets:
            text = tweet.full_text
            text = re.sub(r'https://\S+', '', text)
            text = re.sub(r'@\w+', '', text)
            text = ' '.join(text.split())
            
            tweet_url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            tweet_lines.append(f"- [{text}]({tweet_url})")
        
        # Read README
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace tweets section
        start_marker = "<!-- TWEETS-START -->"
        end_marker = "<!-- TWEETS-END -->"
        
        if start_marker in content and end_marker in content:
            new_content = content.split(start_marker)[0] + start_marker + "\n"
            new_content += "\n".join(tweet_lines) + "\n"
            new_content += end_marker + content.split(end_marker)[1]
            
            # Write updated README
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(new_content)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e

if __name__ == "__main__":
    update_readme_with_tweets()
