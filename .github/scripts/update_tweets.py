import os
import tweepy
import re

def update_readme_with_tweets():
    try:
        # Twitter API v1.1 authentication
        auth = tweepy.OAuth1UserHandler(
            os.environ['TWITTER_API_KEY'],
            os.environ['TWITTER_API_SECRET'],
            os.environ['TWITTER_ACCESS_TOKEN'],
            os.environ['TWITTER_ACCESS_SECRET']
        )
        
        # Create API object
        api = tweepy.API(auth)
        
        # Verify credentials and get username
        me = api.verify_credentials()
        username = me.screen_name
        print(f"Authenticated as: {username}")
        
        # Get tweets from user's timeline
        tweets = api.user_timeline(screen_name=username, count=5, tweet_mode="extended")
        print(f"Found {len(tweets)} tweets")
        
        # Format tweets for README
        tweet_lines = []
        for tweet in tweets:
            text = tweet.full_text
            # Clean up text
            text = re.sub(r'https://\S+', '', text)
            text = re.sub(r'@\w+', '', text)
            text = ' '.join(text.split())
            tweet_url = f"https://twitter.com/{username}/status/{tweet.id}"
            tweet_lines.append(f"- [{text}]({tweet_url})")
        
        # Read and update README
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace tweets section
        start_marker = "<!-- TWEETS-START -->"
        end_marker = "<!-- TWEETS-END -->"
        
        if start_marker in content and end_marker in content:
            new_content = content.split(start_marker)[0] + start_marker + "\n"
            new_content += "\n".join(tweet_lines) + "\n"
            new_content += end_marker + content.split(end_marker)[1]
            
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(new_content)
                print("README updated successfully")
                
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise e

if __name__ == "__main__":
    update_readme_with_tweets()
