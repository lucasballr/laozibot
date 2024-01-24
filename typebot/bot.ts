import { Client, GatewayIntentBits } from 'discord.js';
import { REST, Routes } from 'discord.js';
import dotenv from 'dotenv';

var ytdl = require('ytdl-core');
const fs = require('fs');

dotenv.config();
const { createAudioPlayer } = require('@discordjs/voice');
const token = process.env.DISCORD_TOKEN
const player = createAudioPlayer();

const client = new Client({ intents: [
		GatewayIntentBits.Guilds,
		GatewayIntentBits.GuildMessages,
	],
});

client.once('ready', () => {
    console.log('Ready!');
    console.log(`Logged in as ${client.user?.tag}!. Here is my ID: ${client.user?.id}!`)
    const Guilds = client.guilds.cache.map(guild => guild.id);
    console.log(`Here are my guild id's ${Guilds}`);
});

client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;
  
    if (interaction.commandName === 'ping') {
      await interaction.reply('Pong!');
    }

    if (interaction.commandName === 'play') {
        const text = interaction.options.getString('link');
        const re = /http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?/;
        const match = text?.match(re);

        if (match && match[0]){
            const link = match[0]; // This is the extracted YouTube link
            await interaction.reply(`Found a YouTube link: ${link}`);
        } else {
            await interaction.reply(`No valid YouTube link found in the text.`);
        }   
    }
});

client.login(token!);
