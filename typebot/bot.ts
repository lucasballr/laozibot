import { Client, GatewayIntentBits, VoiceChannel } from 'discord.js';
import { NoSubscriberBehavior, getVoiceConnection, joinVoiceChannel, createAudioPlayer, createAudioResource, AudioPlayerStatus, VoiceConnectionStatus } from '@discordjs/voice';
import dotenv from 'dotenv';
import ytdl from 'ytdl-core';
//import Player from 'discord-player'
const { YouTubeExtractor } = require('@discord-player/extractor');
const { Player } = require('discord-player');
import fs from 'fs';
//const fs = require('fs');
dotenv.config();
const connection = joinVoiceChannel({
        	channelId: 958791787420483607,
        	guildId: 958791786099245056,
	        adapterCreator: guild!.voiceAdapterCreator,
        });

const token = process.env.DISCORD_TOKEN;

const client = new Client({ intents: [
		GatewayIntentBits.Guilds,
		GatewayIntentBits.GuildMessages,
        'GuildVoiceStates',
	],
});
//const player = new Player(client);

const player = createAudioPlayer({
    behaviors: {
        noSubscriber: NoSubscriberBehavior.Pause,
    },
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
        // player.extractors.register(YouTubeExtractor);
        const guild = client.guilds.cache.get(interaction.guildId!)
        const member = guild!.members.cache.get(interaction.member!.user.id);
        const voiceChannel = member!.voice.channel;
        if (!voiceChannel) {
            await interaction.reply('You need to be in a voice channel to play music!');
            return;
        }

        connection = joinVoiceChannel({
        	channelId: voiceChannel!.id,
        	guildId: guild!.id,
	        adapterCreator: guild!.voiceAdapterCreator,
        });
        const resource = createAudioResource('./music.mp3');
        player.play(resource);
        connection.subscribe(player);
        


        // try {
        //     const { song } = await player.play(voiceChannel, youtubeLink);
        //     await interaction.reply(`Playing: ${youtubeLink}`);
        // } catch (error) {
        //     console.error(error);
        //     await interaction.reply('Error occurred while trying to play the audio.');
        // }
    }
    if (interaction.commandName === 'stop'){
        player.stop();
        await interaction.reply('Bye');
    }
});

client.login(token!);
