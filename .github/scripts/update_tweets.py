import os
import tweepy
import re
import time

def update_readme_with_tweets():
    try:
        # Use Bearer Token authentication
        client = tweepy.Client(
            bearer_token=os.environ['TWITTER_BEARER_TOKEN'],
            wait_on_rate_limit=True  # Auto-wait when rate limited
        )
        
        # Get user ID by username
        user = client.get_user(username="samrpassmore")
        if not user.data:
            print("Could not find user")
            return
            
        user_id = user.data.id
        print(f"Found user ID: {user_id}")
        
        # Add delay to avoid rate limits
        time.sleep(2)
        
        # Get tweets with retry logic
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                tweets = client.get_users_tweets(
                    id=user_id,
                    max_results=5,
                    exclude=['retweets', 'replies'],
                    tweet_fields=['text', 'created_at']
                )
                break
            except tweepy.TooManyRequests:
                if attempt < max_retries - 1:
                    print(f"Rate limited. Waiting {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    raise
        
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
            tweet_url = f"https://twitter.com/samrpassmore/status/{tweet.id}"
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
