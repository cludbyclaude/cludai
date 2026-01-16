# Clud - AI Twitter Reply Bot

This repository contains the code for clud, an AI-powered Twitter bot that automatically replies to mentions using Claude AI.

**Note:** This is a demonstration repository showing how the bot works. API keys and credentials are not included.

## How It Works

1. Bot monitors Twitter for mentions of @AI_clud
2. New mentions are sent to Claude API with a custom personality prompt
3. Claude generates a contextual reply
4. Bot automatically posts the reply back to Twitter

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed flow diagrams.

## Setup (For Reference)

```shell
pip install -r requirements.txt
# Add your API keys to .env (see .env.example)
python bot.py
```

**Required API Keys:**
- Twitter API credentials (see `.env.example`)
- Anthropic Claude API key

## Bot Personality

Clud is configured with a custom system prompt that makes it [describe personality - helpful/humorous/technical/etc]. See `config.py` for the full prompt.

## Example Interactions

See the `screenshots/` folder for examples of Clud responding to various mentions and conversations.

## Technical Details

- **AI Model:** Claude (Anthropic API)
- **Twitter Integration:** Tweepy library
- **Response Time:** ~1+ minute per mention
- **Rate Limiting:** Respects Twitter API limits

## License

This code is licensed under the Apache 2.0 license.
```
