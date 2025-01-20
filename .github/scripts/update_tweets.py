import os
import tweepy
import re

def update_readme_with_tweets():
    try:
        # Twitter API v2 authentication
        client = tweepy.Client(
            consumer_key=os.environ['TWITTER_API_KEY'],
            consumer_secret=os.environ['TWITTER_API_SECRET'],
            access_token=os.environ['TWITTER_ACCESS_TOKEN'],
            access_token_secret=os.environ['TWITTER_ACCESS_SECRET']
        )
        
        # Get authenticated user's ID
        me = client.get_me()
        user_id = me.data.id
        username = me.data.username
        print(f"Authenticated as: {username}")
        
        # Get tweets using v2 endpoint
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=5,
            exclude=['retweets', 'replies']
        )
        
        if not tweets.data:
            print("No tweets found")
            return
            
        print(f"Found {len(tweets.data)} tweets")
        
        # Format tweets for README
        tweet_lines = []
        for tweet in tweets.data:
            text = tweet.text
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
