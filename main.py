import discord
from discord.ext import commands
import os, json

def get_prefix(bot, message): 
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f) 
		return prefixes[str(message.guild.id)]
#Loads the prefixes for each server in a `prefixes.json` categorized by server ID and then their prefix.
bot = commands.AutoShardedBot(command_prefix = get_prefix, activity=discord.Activity(type=discord.ActivityType.watching, name="Watching _ servers!"), shard_count=1)

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
#Loads package for .env to allow the secure and safe using of bot token.

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f) 

    prefixes[str(guild.id)] = '!' #Default prefix

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)
#Dumps the prefixes in that `prefixes.json`.
@bot.event
async def on_guild_remove(guild): 
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) 

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)
#Removes prefixes when the bot is removed from the server.
@bot.command(Administrator=True)
async def changeprefix(ctx, prefix): 
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

		prefixes[str(ctx.guild.id)] = prefix

		with open('prefixes.json', 'w') as f: 
			json.dump(prefixes, f, indent=4)
			await ctx.send(f'Prefix changed to: {prefix}.') 
#STATUS

@bot.command(aliases=['lo'])
async def load(ctx, extension):
	bot.load_extension(f'cogs.{extension}') 
	await ctx.send(f'Loaded "{extension}".')
	print(f'Loaded "{extension}".')
#Confirmation of loading of cogs.

@bot.command(aliases=['un'])
async def unload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}') 
	await ctx.send(f'Unloaded "{extension}".')
	print(f'Unloaded "{extension}".')
#Confirmation of unloading a cog.

bot.run(TOKEN) #Running the bot using the token.