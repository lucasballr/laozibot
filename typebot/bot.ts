import { Client, GatewayIntentBits, VoiceChannel } from 'discord.js';
import { getVoiceConnection, joinVoiceChannel, createAudioPlayer, createAudioResource, AudioPlayerStatus, VoiceConnectionStatus } from '@discordjs/voice';
import dotenv from 'dotenv';
import ytdl from 'ytdl-core';
//import Player from 'discord-player'
const { Player } = require('discord-player');
import fs from 'fs';
//const fs = require('fs');

dotenv.config();
let connection;
const token = process.env.DISCORD_TOKEN;

const client = new Client({ intents: [
		GatewayIntentBits.Guilds,
		GatewayIntentBits.GuildMessages,
        'GuildVoiceStates',
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
        const youtubeLink = interaction.options.getString('link');
        const player = new Player(client);
        const guild = client.guilds.cache.get(interaction.guildId!)
        const member = guild!.members.cache.get(interaction.member!.user.id);
        const voiceChannel = member!.voice.channel;
        if (!voiceChannel) {
            await interaction.reply('You need to be in a voice channel to play music!');
            return;
        }
        try {
            await player.join(voiceChannel);
            const song = await player.play(youtubeLink);

            await interaction.reply(`Playing: ${song.name}`);
        } catch (error) {
            console.error(error);
            await interaction.reply('Error occurred while trying to play the audio.');
        }
    }
    if (interaction.commandName === 'stop'){
        let connection = getVoiceConnection(interaction.guildId!);
        connection?.disconnect();
        await interaction.reply('Bye');
    }
});

client.login(token!);
