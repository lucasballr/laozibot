import { REST, Routes } from 'discord.js';
import dotenv from 'dotenv';

dotenv.config();
const token = process.env.DISCORD_TOKEN

const commands = [
  {
    name: 'ping',
    description: 'Replies with Pong!',
  },
];

const rest = new REST({ version: '10' }).setToken(token!);

try {
  console.log('Started refreshing application (/) commands.');

  await rest.put(Routes.applicationCommands('1199477265457758239'), { body: commands });

  console.log('Successfully reloaded application (/) commands.');
} catch (error) {
  console.error(error);
}
