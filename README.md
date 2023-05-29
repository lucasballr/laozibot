# Laozibot

So this is a MAJOR work in progress project. It's basically a discord bot that uses the gpt-3.5 api to aid its responses. I'll add a future feature list soon, but for now this is it.

# Installation

If you wanna run this yourself, You'll need an api key from OpenAI and OpenWeatherMap. Also, you'll need to make a discord bot account on discord, and copy the bot token into the config file. The config file looks like this:
```
### filename: config.py
OPENAI_API_KEY='<OpenAI API Key>'
DISCORD_API_KEY='<Discord bot token>'
OWM_API_KEY='<OWM KEY>'
```

Then you can instll the dependencies with:
```
pip install -r requirements.txt
```

Then run it with:
```
python laozibot.py
```

# Note

This is super early phases. Don't expect literally anything to work yet.
Anyone who submits a pull request that gets approved will get added to the "approved-users" list. Don't even try to exploit becuase by api keys have limits.
