"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const discord_js_1 = require("discord.js");
const dotenv_1 = __importDefault(require("dotenv"));
//import Player from 'discord-player'
const { YouTubeExtractor } = require('@discord-player/extractor');
const { Player } = require('discord-player');
//const fs = require('fs');
dotenv_1.default.config();
let connection;
const token = process.env.DISCORD_TOKEN;
const client = new discord_js_1.Client({ intents: [
        discord_js_1.GatewayIntentBits.Guilds,
        discord_js_1.GatewayIntentBits.GuildMessages,
        'GuildVoiceStates',
    ],
});
const player = new Player(client);
client.once('ready', () => {
    var _a, _b;
    console.log('Ready!');
    console.log(`Logged in as ${(_a = client.user) === null || _a === void 0 ? void 0 : _a.tag}!. Here is my ID: ${(_b = client.user) === null || _b === void 0 ? void 0 : _b.id}!`);
    const Guilds = client.guilds.cache.map(guild => guild.id);
    console.log(`Here are my guild id's ${Guilds}`);
});
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isChatInputCommand())
        return;
    if (interaction.commandName === 'ping') {
        await interaction.reply('Pong!');
    }
    if (interaction.commandName === 'play') {
        const youtubeLink = interaction.options.getString('link');
        player.extractors.register(YouTubeExtractor);
        const guild = client.guilds.cache.get(interaction.guildId);
        const member = guild.members.cache.get(interaction.member.user.id);
        const voiceChannel = member.voice.channel;
        if (!voiceChannel) {
            await interaction.reply('You need to be in a voice channel to play music!');
            return;
        }
        try {
            const { song } = await player.play(voiceChannel, youtubeLink);
            await interaction.reply(`Playing: ${youtubeLink}`);
        }
        catch (error) {
            console.error(error);
            await interaction.reply('Error occurred while trying to play the audio.');
        }
    }
    if (interaction.commandName === 'stop') {
        await player.destroy();
        await interaction.reply('Bye');
    }
});
client.login(token);
