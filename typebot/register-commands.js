"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const discord_js_1 = require("discord.js");
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
const token = process.env.DISCORD_TOKEN;
const clientId = process.env.CLIENT_ID;
const guildId = process.env.GUILD_ID;
// SUB_COMMAND 1   
// SUB_COMMAND_GROUP 2 
// STRING 3    
// INTEGER 4
// BOOLEAN 5   
// USER 6  
// CHANNEL 7
// ROLE 8  
// MENTIONABLE 9
// NUMBER 10
// ATTACHMENT 11
const commands = [
    {
        name: 'ping',
        description: 'Replies with Pong!',
    },
    {
        name: 'play',
        description: 'Plays music from YouTube',
        options: [{
                name: 'link',
                type: 3,
                description: 'The YouTube link',
                required: true,
            }],
    },
    {
        name: 'stop',
        description: 'Stops the music',
    },
];
const rest = new discord_js_1.REST({ version: '10' }).setToken(token);
(async () => {
    try {
        console.log(`Started refreshing ${commands.length} application (/) commands.`);
        // The put method is used to fully refresh all commands in the guild with the current set
        const data = await rest.put(discord_js_1.Routes.applicationGuildCommands(clientId, guildId), { body: commands });
        console.log(`Successfully reloaded application (/) commands.`);
    }
    catch (error) {
        // And of course, make sure you catch and log any errors!
        console.error(error);
    }
})();
