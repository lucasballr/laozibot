FROM python:3-alpine
##FROM gorialis/discord.py
RUN apk add  --no-cache ffmpeg

RUN mkdir -p /usr/src/bot

COPY ./config.py /usr/src/bot
COPY ./laozibot.py /usr/src/bot
COPY ./requirements.txt /usr/src/bot
COPY ext/ /usr/src/bot/ext/
WORKDIR /usr/src/bot

RUN pip install -r /usr/src/bot/requirements.txt

CMD ["python3", "-u", "/usr/src/bot/laozibot.py"]
