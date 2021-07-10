
import discord
from db import Database
from discord.ext import commands

warnstructure = {
	'_id': "jsdafhadsjkfhsdasfgjjd", # Internal MONGODB
	'guild_id': 23984237842,
	'warn_data': {
		'23432424343242':[ # userid
			{
				'author_id': 782462384263462,
				'reason': "TRASH"
			}
		]
	}
}

class warning(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(Administrator=True, aliases=['w'])
	async def warn(self, ctx, user:discord.User, *, reason): 
		warns = Database.find('warns', {'guild_id': ctx.guild.id})

		if not warns:
			warns = {
				'guild_id': ctx.guild.id,
				'warn_data': {}
			}
			result = Database.insert('warns', warns)
			warns = Database.find('warns', {'_id':result.inserted_id})

		if not str(user.id) in warns['warn_data'].keys():
			warns['warn_data'][str(user.id)] = []

		warns['warn_data'][str(user.id)].append({
			'author_id': ctx.author.id,
			'reason': reason
		})

		Database.update('warns', {'guild_id':ctx.guild.id}, {'$set':{'warn_data':warns['warn_data']}})

		embed=discord.Embed(description=f"{user} Warned for: {reason}",color=0x06c258)
		embed.set_author(name=user.name +'#'+ user.discriminator, icon_url=user.avatar_url)
		await ctx.send(embed=embed)

	@commands.command(Administrator=True, aliases=['dw'] )
	async def delwarn(self, ctx, user:discord.User, warnId:int):
		warns = Database.find('warns', {'guild_id': ctx.guild.id})

		if not warns:
			warns = {
				'guild_id': ctx.guild.id,
				'warn_data': {}
			}
			result = Database.insert('warns', warns)
			warns = Database.find('warns', {'_id':result.inserted_id})
			return await ctx.send('There are no warnings for this user.')

		if not str(user.id) in warns['warn_data'].keys():
			warns['warn_data'][str(user.id)] = []
			return await ctx.send('There are no warnings for this user.')

		try:
			del warns['warn_data'][str(user.id)][warnId - 1]
		except:
			return await ctx.send("Invalid warning ID given, please check the ID and try again.")
		else:
			Database.update('warns', {'guild_id':ctx.guild.id}, {'$set': {'warn_data': warns['warn_data']}})
			return await ctx.send(f"Warn `{warnId}` has been removed.")
	
	@commands.command(Administrator=True, aliases=['warnings'])
	async def warns(self, ctx, user:discord.User): 
		warns = Database.find('warns', {'guild_id': ctx.guild.id})

		if not warns:
			warns = {
				'guild_id': ctx.guild.id,
				'warn_data': {}
			}
			result = Database.insert('warns', warns)
			warns = Database.find('warns', {'_id':result.inserted_id})
			return await ctx.send("There are no warnings for this user.")

		if not str(user.id) in warns['warn_data'].keys():
			warns['warn_data'][str(user.id)] = []
			return await ctx.send("There are no warnings for this user.")

		userwarnlist = warns['warn_data'][str(user.id)]
		numWarns = 0
		
		embed=discord.Embed(title=f"Warns", color=0x06c258)
		embed.set_author(name=user.name +'#'+ user.discriminator, icon_url=user.avatar_url)

		for userwarndata in userwarnlist:
			if numWarns != 25:
				numWarns += 1 

				warner = await self.bot.fetch_user(userwarndata['author_id'])
				if warner is not None: 
					warner = str(warner.name +'#'+ warner.discriminator)
				else: 
					warner = userwarndata['author_id']

				embed.add_field(name=str(numWarns) + '. ' + userwarndata['reason'], value=f"Warned by: {warner}", inline=False)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(warning(bot))
