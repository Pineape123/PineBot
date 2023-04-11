
import discord
from db import Database
from discord.ext import commands

warnstructure = {
	'warns': {
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
		guild_data = await Database.get_guild(ctx.guild.id)

		if not str(user.id) in guild_data['warns'].keys():
			guild_data['warns'][str(user.id)] = []

		guild_data['warns'][str(user.id)].append({
			'author_id': ctx.author.id,
			'reason': reason
		})
	
		await Database.set_guild(ctx.guild.id, guild_data)
		embed=discord.Embed(description=f"{user} Warned for: {reason}",color=0x06c258)
		embed.set_author(name=user.name +'#'+ user.discriminator, icon_url=user.avatar.url)
		await ctx.send(embed=embed)

	@commands.command(Administrator=True, aliases=['dw', 'removewarn', 'deletewarn'] )
	async def delwarn(self, ctx, user:discord.User, warnId:int):
		guild_data = await Database.get_guild(ctx.guild.id)

		if not str(user.id) in guild_data['warns'].keys():
			return await ctx.send('There are no warnings for this user.')

		try:
			del guild_data['warns'][str(user.id)][warnId - 1]
		except:
			return await ctx.send("Invalid warning ID given, please check the ID and try again.")
		else:
			await Database.set_guild(ctx.guild.id, guild_data)
			return await ctx.send(f"Warn `{warnId}` has been removed.")
	
	@commands.command(Administrator=True, aliases=['warnings'])
	async def warns(self, ctx, user:discord.User):
		guild_data = await Database.get_guild(ctx.guild.id)

		if not str(user.id) in guild_data['warns'].keys():
			guild_data['warns'][str(user.id)] = []
			return await ctx.send("There are no warnings for this user.")

		userwarnlist = guild_data['warns'][str(user.id)]
		numWarns = 0
		
		embed=discord.Embed(title=f"Warns", color=0x06c258)
		embed.set_author(name=user.name +'#'+ user.discriminator, icon_url=user.avatar.url)

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


async def setup(bot: commands.Bot):
	await bot.add_cog(warning(bot))
