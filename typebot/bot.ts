import { Client, GatewayIntentBits, VoiceChannel } from 'discord.js';
import { getVoiceConnection, joinVoiceChannel, createAudioPlayer, createAudioResource, AudioPlayerStatus, VoiceConnectionStatus } from '@discordjs/voice';
import dotenv from 'dotenv';
import ytdl from 'ytdl-core-discord';

//const fs = require('fs');

dotenv.config();
let connection;
const token = process.env.DISCORD_TOKEN;

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
        const youtubeLink = interaction.options.getString('link');
        if (!ytdl.validateURL(youtubeLink!)) {
            await interaction.reply('Invalid YouTube URL.');
            return;
        }
        const guild = client.guilds.cache.get(interaction.guildId!)
        const member = guild!.members.cache.get(interaction.member!.user.id);
        const voiceChannel = member!.voice.channel;
        if (!voiceChannel) {
            await interaction.reply('You need to be in a voice channel to play music!');
            return;
        } 

        try {
            const connection = joinVoiceChannel({
                channelId: voiceChannel!.id,
                guildId: interaction.guildId!,
                adapterCreator: guild!.voiceAdapterCreator,
            });

            const audioPlayer = createAudioPlayer();
            const resource = createAudioResource(await ytdl(youtubeLink!));
            resource.volume!.setVolume(1);
            await interaction.reply(`Now playing: ${youtubeLink}`);
            connection.subscribe(audioPlayer);
            // const player = createAudioPlayer();
            // connection.subscribe(player);
            // player.play(resource);
            // await interaction.reply(`Now playing: ${youtubeLink}`);
            
            // connection.on(VoiceConnectionStatus.Ready, () => {
            //     console.log('The connection is ready to play audio!');
            // });

            // player.on(AudioPlayerStatus.Idle, () => {
            //     connection.destroy();
            // });
        } catch (error) {
            console.error(error);
            await interaction.reply('Error playing the audio.');
        }
    }
    if (interaction.commandName === 'stop'){
        let connection = getVoiceConnection(interaction.guildId!);
        connection?.disconnect();
        await interaction.reply('Bye');
    }
});

client.login(token!);
