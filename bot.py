"""
Clud - AI Twitter Reply Bot
Monitors mentions and replies using Claude AI
"""

import tweepy
import anthropic
import os
import time
from dotenv import load_dotenv
from config import CLUD_SYSTEM_PROMPT, CHECK_MENTIONS_INTERVAL, MAX_RESPONSE_LENGTH

# Load environment variables
load_dotenv()

# Initialize Twitter API
twitter_client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
)

# Initialize Claude API
claude_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Track last processed mention to avoid duplicates
last_mention_id = None

def get_claude_response(tweet_text, author_username):
    """Send tweet to Claude and get response"""
    try:
        message = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=CLUD_SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Tweet from @{author_username}: {tweet_text}"
            }]
        )
        
        response = message.content[0].text
        
        # Trim if too long for Twitter
        if len(response) > MAX_RESPONSE_LENGTH:
            response = response[:MAX_RESPONSE_LENGTH-3] + "..."
            
        return response
    except Exception as e:
        print(f"Error getting Claude response: {e}")
        return None

def check_mentions():
    """Check for new mentions and reply"""
    global last_mention_id
    
    try:
        # Get recent mentions
        mentions = twitter_client.get_users_mentions(
            id=twitter_client.get_me().data.id,
            since_id=last_mention_id,
            max_results=10
        )
        
        if not mentions.data:
            print("No new mentions")
            return
        
        # Process each mention
        for mention in reversed(mentions.data):
            print(f"\nNew mention from @{mention.author_id}: {mention.text}")
            
            # Get Claude's response
            response = get_claude_response(mention.text, mention.author_id)
            
            if response:
                # Reply to the tweet
                twitter_client.create_tweet(
                    text=response,
                    in_reply_to_tweet_id=mention.id
                )
                print(f"Replied: {response}")
            
            # Update last processed mention
            last_mention_id = mention.id
            
            # Small delay to avoid rate limits
            time.sleep(10)
            
    except Exception as e:
        print(f"Error checking mentions: {e}")

def main():
    """Main bot loop"""
    print("Clud bot starting...")
    print(f"Checking mentions every {CHECK_MENTIONS_INTERVAL} seconds")
    
    while True:
        check_mentions()
        time.sleep(CHECK_MENTIONS_INTERVAL)

if __name__ == "__main__":
    main()
