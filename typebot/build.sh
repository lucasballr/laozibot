#! /bin/bash

git pull
tsc
node register-commands.js
node bot.js
