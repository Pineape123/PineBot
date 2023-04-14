import discord
from discord.ext import commands
from db import Database

class account(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command()
	async def init(self, ctx: commands.Context):
		""""""
		guild_data = await Database.get_guild(ctx.guild.id)
		# If user is not in the list OR if user has 0 coins
		if str(ctx.author.id) not in guild_data['coins'] or guild_data['coins'][str(ctx.author.id)] == 0:
			guild_data['coins'][str(ctx.author.id)] = 100
			await Database.set_guild(ctx.guild.id, guild_data)
			embed=discord.Embed(title = "Account Initialized", description=f"You Have: ${guild_data['coins'][str(ctx.author.id)]}",color=0x06c258)
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar and ctx.author.avatar.url or None)
			await ctx.send(embed=embed)
		else:
			embed=discord.Embed(title = "Lol, Good Try!", description=f"You have to be broke to re-initialize your account.", color=discord.Color.red())
			await ctx.send(embed=embed)
		

			
	@commands.command()
	async def wallet(self, ctx: commands.Context):
		""""""
		guild_data = await Database.get_guild(ctx.guild.id)
		if str(ctx.author.id) not in guild_data['coins']:
			#await ctx.send("Please init your account")
			embed=discord.Embed(title = "Error", description=f"Please initialize your account by using the init command", color=discord.Color.red())
			await ctx.send(embed=embed)
		else:
			#await ctx.send(f"you have ${guild_data['coins'][str(ctx.author.id)]}")
			embed=discord.Embed(title = "Wallet", description=f"You Have: ${guild_data['coins'][str(ctx.author.id)]}",color=0x06c258)
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar and ctx.author.avatar.url or None)
			await ctx.send(embed=embed)


	@commands.command()
	async def lb(self, ctx: commands.Context):
		""""""
		guild_data = await Database.get_guild(ctx.guild.id)
		accounts = sorted(guild_data["coins"].items(), key=lambda i: i[1], reverse=True)

		printStr = ""
		count = 1
		for account in accounts:
			printStr += f"{count}. <@{account[0]}>: ${account[1]}\n\n"
			count += 1
		#await ctx.send(printStr[:-1])
		embed=discord.Embed(title = "Leaderboard", description=f"{printStr[:-1]}", color=0x06c258)
		await ctx.send(embed=embed)









async def setup(bot: commands.Bot):
	await bot.add_cog(account(bot))
