import discord
from discord.ext import commands
from db import Database
import random

class gamble(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

			
	@commands.command()
	@commands.max_concurrency(1, per=commands.BucketType.member)
	async def gamble(self, ctx: commands.Context, bet: str):
		""""""
		try:
			if bet.isdigit():
				bet = int(bet)
			guild_data = await Database.get_guild(ctx.guild.id)
			if str(ctx.author.id) not in guild_data["coins"]:
				return await ctx.send("Please init your account first.")

			elif isinstance(bet, int) and guild_data['coins'][str(ctx.author.id)] < bet:
				return await ctx.send("You do not have enough coins.")
			
			elif bet == "max" or bet == "all":
				bet = guild_data['coins'][str(ctx.author.id)]

			elif not isinstance(bet, int):
				return await ctx.send("Invalid Bet")

			luckynumber = random.uniform(0.01, 2)
			winnings = int(bet*luckynumber)
			guild_data['coins'][str(ctx.author.id)] += (-bet) + winnings
			await Database.set_guild(ctx.guild.id, guild_data)
			#await ctx.send("Please init your account")
			#await ctx.send(f"you have ${guild_data['coins'][str(ctx.author.id)]}")
			if winnings > bet:
				embed=discord.Embed(title = "Congratulations", description=f"You Won: {winnings - bet} Pinecones\n\nYou have {guild_data['coins'][str(ctx.author.id)]} Pinecones",color=0x06c258)
				embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar and ctx.author.avatar.url or None)
				await ctx.send(embed=embed)
			else: 
				embed=discord.Embed(title = "OOPSIE", description=f"You LOST: {bet - winnings} Pinecones\n\nYou have {guild_data['coins'][str(ctx.author.id)]} Pinecones",color=discord.Color.red())
				embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar and ctx.author.avatar.url or None)
				await ctx.send(embed=embed)
		except Exception as e:
			print(e)
	
	@commands.command()
	@commands.max_concurrency(1, per=commands.BucketType.member)
	async def mb(self, ctx: commands.Context):
		"""1000 Pinecones. You may win money or you may loose money"""
		guild_data = await Database.get_guild(ctx.guild.id)
		mysteryboxprice = 1000
		if str(ctx.author.id) not in guild_data["coins"]:
			return await ctx.send("Please init your account first.")
		elif guild_data['coins'][str(ctx.author.id)] < mysteryboxprice:
			return await ctx.send("You do not have enough coins. A mystery box is 1000 Pinecones.")
		mysterybox = random.randint(-200, 2000)

		guild_data['coins'][str(ctx.author.id)] += (mysterybox-mysteryboxprice)
		await Database.set_guild(ctx.guild.id, guild_data)

		if mysterybox < mysteryboxprice:
			embed=discord.Embed(title = "OOPSIE", description=f"You Won: {mysterybox} Pinecones\n\nYou have {guild_data['coins'][str(ctx.author.id)]} Pinecones",color=discord.Color.red())
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar and ctx.author.avatar.url or None)
			await ctx.send(embed=embed)
		else:
			embed=discord.Embed(title = "Congratulations", description=f"You Won: {mysterybox} Pinecones\n\nYou have {guild_data['coins'][str(ctx.author.id)]} Pinecones",color=0x06c258)
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar and ctx.author.avatar.url or None)
			await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
	await bot.add_cog(gamble(bot))


