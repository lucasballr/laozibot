FROM debian:12
##FROM gorialis/discord.py
RUN apt update && apt install -y python3 ffmpeg python3-pip

RUN mkdir -p /usr/src/bot

COPY ./config.py /usr/src/bot
COPY ./laozibot.py /usr/src/bot
COPY ./requirements.txt /usr/src/bot
COPY ext/ /usr/src/bot/ext/
WORKDIR /usr/src/bot

RUN pip3 install -r /usr/src/bot/requirements.txt

CMD ["python3", "-u", "/usr/src/bot/laozibot.py"]
