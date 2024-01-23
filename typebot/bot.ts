import { Client, GatewayIntentBits } from 'discord.js';
import { REST, Routes } from 'discord.js';
import dotenv from 'dotenv';

dotenv.config();
const token = process.env.DISCORD_TOKEN
//const clientId = '1199477265457758239'

const commands = [
  {
    name: 'ping',
    description: 'Replies with Pong!',
  },
];

const rest = new REST({ version: '10' }).setToken(token!);

// (async () => {
//     try {
//         console.log(`Started refreshing ${commands.length} application (/) commands.`);

//         // The put method is used to fully refresh all commands in the guild with the current set
//         const data = await rest.put(
//             Routes.applicationGuildCommands(clientId!, guildId),
//             { body: commands },
//         );

//         console.log(`Successfully reloaded ${data.length} application (/) commands.`);
//     } catch (error) {
//         // And of course, make sure you catch and log any errors!
//         console.error(error);
//     }
// })();

const client = new Client({ intents: [
		GatewayIntentBits.Guilds,
		GatewayIntentBits.GuildMessages,
	],
});

client.once('ready', () => {
    console.log('Ready!');
    console.log(`Logged in as ${client.user?.tag}!. Here is my ID: ${client.user?.id}!`)
    console.log("Here are my guild id's");
    let guildIds = client.guilds.fetch();
    for (let guildId in guildIds){
        console.log(guildId);
    }
});

client.on('messageCreate', message => {
    if (message.content === 'ping') {
        message.reply('pong');
    }
});


client.login(token!);
