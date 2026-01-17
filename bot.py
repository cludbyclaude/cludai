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

# Load environment variables from .env file
# This keeps API keys secure and out of the codebase
load_dotenv()

# Initialize Twitter API client with OAuth 1.0a credentials
# Tweepy handles authentication and API communication
twitter_client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
)

# Initialize Anthropic Claude API client
# Used for generating intelligent responses to mentions
claude_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Track the ID of the last processed mention to avoid duplicate responses
# This is reset when the bot restarts, so it only processes new mentions
last_mention_id = None

def get_claude_response(tweet_text, author_username):
    """
    Send tweet content to Claude API and get an AI-generated response
    
    Args:
        tweet_text (str): The text content of the tweet mention
        author_username (str): Username of the person who mentioned the bot
        
    Returns:
        str: Claude's response, trimmed to Twitter's character limit
        None: If an error occurs during API call
    """
    try:
        # Create a message using Claude's API
        # The system prompt defines Clud's personality and behavior
        message = claude_client.messages.create(
            model="claude-sonnet-4-20250514",  # Using Claude Sonnet 4 for quality responses
            max_tokens=1000,  # Allows Claude enough tokens for a full response
            system=CLUD_SYSTEM_PROMPT,  # Personality and guidelines from config.py
            messages=[{
                "role": "user",
                "content": f"Tweet from @{author_username}: {tweet_text}"
            }]
        )
        
        # Extract the text content from Claude's response
        response = message.content[0].text
        
        # Trim response if it exceeds Twitter's character limit
        # Adds ellipsis to indicate truncation
        if len(response) > MAX_RESPONSE_LENGTH:
            response = response[:MAX_RESPONSE_LENGTH-3] + "..."
            
        return response
        
    except Exception as e:
        # Log error but don't crash - bot continues monitoring
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
    """
    Main bot loop - continuously monitors for mentions and responds
    
    Runs indefinitely until manually stopped (Ctrl+C)
    Checks for new mentions at regular intervals defined in config
    """
    print("Clud bot starting...")
    print(f"Checking mentions every {CHECK_MENTIONS_INTERVAL} seconds")
    
    # Infinite loop - bot runs continuously
    while True:
        check_mentions()  # Check for and respond to new mentions
        time.sleep(CHECK_MENTIONS_INTERVAL)  # Wait before next check

# Standard Python entry point
# Allows bot to be run directly: python bot.py
if __name__ 
