# Clud Bot Architecture

## Overview
lud is a Twitter bot that uses Claude AI to automatically reply to mentions. This document explains how the system works.

## System Flow
```
1. Twitter Mention
   └─> Bot detects new @AI_clud mention
       └─> Extract tweet text and author
           └─> Send to Claude API with system prompt
               └─> Claude generates contextual response
                   └─> Bot posts reply to Twitter
                       └─> Update last processed mention ID
```

## Components

### 1. Twitter API Integration (`bot.py`)
- **Authentication:** Uses Tweepy library with OAuth 1.0a
- **Monitoring:** Polls for mentions every 60 seconds (configurable)
- **Rate Limiting:** Implements delays to respect Twitter API limits
- **Deduplication:** Tracks `last_mention_id` to avoid processing the same mention twice

### 2. Claude AI Integration (`bot.py`)
- **Model:** Claude Sonnet 4
- **System Prompt:** Custom personality defined in `config.py`
- **Context:** Each mention is sent with author username for personalization
- **Response Formatting:** Automatically trims responses to fit Twitter's 280 character limit

### 3. Configuration (`config.py`)
- **Personality Prompt:** Defines how clud responds (tone, style, guidelines)
- **Bot Settings:** Check intervals, character limits, rate limiting
- **Customizable:** Easy to modify clud's behavior without touching main code

### 4. Environment Variables (`.env`)
- **API Keys:** Twitter and Anthropic credentials loaded securely
- **Never Committed:** `.gitignore` prevents accidental exposure
- **Template Provided:** `.env.example` shows required variables

## Data Flow Diagram
```
┌─────────────┐
│   Twitter   │
│   Mention   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   bot.py        │
│ check_mentions()│
└──────┬──────────┘
       │
       ▼
┌──────────────────────┐
│  Claude API          │
│  + System Prompt     │
│  + Tweet Context     │
└──────┬───────────────┘
       │
       ▼
┌─────────────────┐
│  Claude Reply   │
│  (formatted)    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Twitter Reply  │
│  Posted         │
└─────────────────┘
```

## Key Features

### Real-time Monitoring
- Continuous polling loop
- Configurable check interval (default: 60 seconds)
- Graceful error handling

### AI-Powered Responses
- Each reply is generated contextually by Claude
- Maintains consistent personality across conversations
- Adapts to different types of mentions

### Rate Limit Management
- Built-in delays between API calls
- Respects Twitter's rate limits
- Error handling for rate limit exceeded

### Security
- API keys stored in environment variables
- No credentials in code
- `.gitignore` protects sensitive files

## Error Handling

The bot handles common errors:
- **Twitter API errors:** Logs and continues monitoring
- **Claude API errors:** Returns None, skips reply
- **Rate limiting:** Implements delays
- **Network issues:** Catches exceptions, retries on next cycle

## Limitations

- Polling-based (60 second delay by default)
- Single-threaded processing
- Conversation history tracking
- Basic rate limiting
- No analytics or metrics

## Future Improvements

Potential enhancements:
- Webhook-based real-time mentions
- Conversation threading and context
- Analytics dashboard
- Reply filtering and moderation
