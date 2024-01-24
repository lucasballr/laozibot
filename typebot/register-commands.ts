import { REST, Routes } from 'discord.js';
import dotenv from 'dotenv';

dotenv.config();
const token = process.env.DISCORD_TOKEN
const clientId = process.env.CLIENT_ID
const guildId = process.env.GUILD_ID

const commands = [
  {
    name: 'ping',
    description: 'Replies with Pong!',
  },
  {
    name: 'play',
    description: 'Plays music from YouTube',
  },
];

const rest = new REST({ version: '10' }).setToken(token!);

(async () => {
	try {
		console.log(`Started refreshing ${commands.length} application (/) commands.`);

		// The put method is used to fully refresh all commands in the guild with the current set
		const data = await rest.put(
			Routes.applicationGuildCommands(clientId!, guildId!),
			{ body: commands },
		);

		console.log(`Successfully reloaded application (/) commands.`);
	} catch (error) {
		// And of course, make sure you catch and log any errors!
		console.error(error);
	}
})();