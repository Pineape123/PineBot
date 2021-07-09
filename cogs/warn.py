
import discord
from discord.ext import commands
import json


class warning(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(Administrator=True, aliases=['w'])
	async def warn(self, ctx, user:discord.User, *, reason): 
		with open('./warns.json', 'r') as f:
			warns = json.load(f)

			if not str(ctx.guild.id) in warns:
				warns[str(ctx.guild.id)] = {}

			if not str(user.id) in warns[str(ctx.guild.id)].keys():
				warns[str(ctx.guild.id)][str(user.id)] = []

			warns[str(ctx.guild.id)][str(user.id)].append(reason)

			with open('./warns.json', 'w') as f: 
				json.dump(warns, f, indent=4)
				embed=discord.Embed(description=f"{user} Warned for: {reason}",color=0x06c258)
				embed.set_author(name=user.name +'#'+ user.discriminator, icon_url=user.avatar_url)
				await ctx.send(embed=embed)

	@commands.command(Administrator=True, aliases=['dw'] )
	async def delwarn(self, ctx, user:discord.User, warnId:int): 
		with open('./warns.json', 'r') as f:
			warns = json.load(f)

			if not str(ctx.guild.id) in warns:
				warns[str(ctx.guild.id)] = {}

			if not str(user.id) in warns[str(ctx.guild.id)].keys():
				warns[str(ctx.guild.id)][str(user.id)] = []
				return await ctx.send("This user has no warnings!")

			try:
				del warns[str(ctx.guild.id)][str(user.id)][warnId - 1]
			except:
				return await ctx.send("Invalid warning ID given, please check the ID and try again.")
			else:
				await ctx.send(f"Warn `{warnId}` has been removed.")
				with open('./warns.json', 'w') as f: 
					json.dump(warns, f, indent=4)
	
	@commands.command(Administrator=True, aliases=['warnings'])
	async def warns(self, ctx, user:discord.User): 
		with open('./warns.json', 'r') as f:
			warns = json.load(f)

			if not str(ctx.guild.id) in warns:
				await ctx.send("There are no warnings for this user.")
				return

			if not str(user.id) in warns[str(ctx.guild.id)]:
				await ctx.send("This user has no warnings.")
				return

			userwarnlist = warns[str(ctx.guild.id)][str(user.id)]
			numWarns = 0
			
			embed=discord.Embed(title=f"Warns", color=0x06c258)
			embed.set_author(name=user.name +'#'+ user.discriminator, icon_url=user.avatar_url)

			for userwarn in userwarnlist:
				if numWarns != 25:
					numWarns += 1 
					embed.add_field(name="\uFEFF", value=str(numWarns) + '. ' + userwarn , inline=False)
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(warning(bot))