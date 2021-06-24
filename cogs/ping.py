import discord
from discord.ext import commands
import math
class ping(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	
	@commands.command()
	async def ping(self, ctx):
		embed=discord.Embed(title="Ping!", description=f'in {round(self.bot.latency * 1000)}ms', color=0xafff24)
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(ping(bot))

	

