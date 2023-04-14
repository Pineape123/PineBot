import discord
from discord.ext import commands
from db import Database
import random

class gamble(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

			
	@commands.command()
	async def gamble(self, ctx: commands.Context, bet: int):
		""""""
		try:
			guild_data = await Database.get_guild(ctx.guild.id)
			if str(ctx.author.id) not in guild_data["coins"]:
				await ctx.send("Please init your account first.")

			elif guild_data['coins'][str(ctx.author.id)] < bet:
				await ctx.send("You do not have enough coins.")

			luckynumber = random.uniform(0.01, 2)
			winnings = int(bet*luckynumber)
			guild_data['coins'][str(ctx.author.id)] += (-bet) + winnings
			await Database.set_guild(ctx.guild.id, guild_data)
			#await ctx.send("Please init your account")
			#await ctx.send(f"you have ${guild_data['coins'][str(ctx.author.id)]}")
			if winnings > bet:
				embed=discord.Embed(title = "Congratulations", description=f"You Won: ${winnings - bet}",color=0x06c258)
				embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar and ctx.author.avatar.url or None)
				await ctx.send(embed=embed)
			else: 
				embed=discord.Embed(title = "OOPSIE", description=f"You LOST: ${bet - winnings}",color=discord.Color.red())
				embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar and ctx.author.avatar.url or None)
				await ctx.send(embed=embed)
		except Exception as e:
			print(e)

async def setup(bot: commands.Bot):
	await bot.add_cog(gamble(bot))


