import discord
from discord.ext import commands
import os, json
from db import Database

Database.init()

prefixstructure = {
	'_id': "jsdafhadsjkfhsdasfgjjd", # Internal MONGODB
	'guild_id': 23984237842,
	'prefix': "!"
}

def get_prefix(bot, message): 
	prefixes = Database.find('prefixes', {'guild_id': message.guild.id})
	return prefixes['prefix'] or '!'
	# with open('prefixes.json', 'r') as f:
	# 	prefixes = json.load(f) 
	# 	return prefixes[str(message.guild.id)]

bot = commands.AutoShardedBot(command_prefix = get_prefix, shard_count=1, case_insensitive=True, help_command=None)
#########################

###########################
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
##########################
@bot.event
async def on_guild_join(guild):
	Database.insert('prefixes', {'guild_id': guild.id, 'prefix': "!"})
    # with open('prefixes.json', 'r') as f: 
    #     prefixes = json.load(f) 

    # prefixes[str(guild.id)] = '!'

    # with open('prefixes.json', 'w') as f: 
    #     json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
	prefixes = Database.delete('prefixes', {'guild_id': guild.id})

    # with open('prefixes.json', 'r') as f:
    #     prefixes = json.load(f)

    # prefixes.pop(str(guild.id)) 

    # with open('prefixes.json', 'w') as f: 
    #     json.dump(prefixes, f, indent=4)

@bot.command(Administrator=True)
async def changeprefix(ctx, prefix): 
	prefixes = Database.find('prefixes', {'guild_id': ctx.guild.id})

	if not prefixes:
		Database.insert('prefixes', {'guild_id': ctx.guild.id, 'prefix': "!"})
		prefixes = Database.find('prefixes', {'guild_id': ctx.guild.id})

	prefixes['prefix'] = prefix

	Database.update('prefixes', {'guild_id': ctx.guild.id}, {'$set': {'prefix': prefixes['prefix']}})
	# with open('prefixes.json', 'r') as f:
	# 	prefixes = json.load(f)

	# 	prefixes[str(ctx.guild.id)] = prefix

	# 	with open('prefixes.json', 'w') as f: 
	# 		json.dump(prefixes, f, indent=4)
	# 		await ctx.send(f'Prefix changed to: {prefix}.') 

@bot.command(aliases=['lo'])
async def load(ctx, extension):
	bot.load_extension(f'cogs.{extension}') 
	await ctx.send(f'Loaded "{extension}".')
	print(f'Loaded "{extension}".')

@bot.command(aliases=['un'])
async def unload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}') 
	await ctx.send(f'Unloaded "{extension}".')
	print(f'Unloaded "{extension}".')


################
for FileName in os.listdir('./cogs'):
	if FileName.endswith(".py"):
		bot.load_extension(f'cogs.{FileName[:-3]}')
		print(FileName)

@bot.command()
async def listcogs(ctx):
	embed=discord.Embed(title="Loaded Cogs", color=0x06c258)
	embed.set_footer(text="PineBot")
	for cogname in bot.cogs.keys():
		embed.add_field(name=f'{str.capitalize(cogname)}:', value=f':white_check_mark: {cogname}')
	await ctx.send(embed=embed)
	
bot.run(TOKEN)