import discord
from discord.ext import commands

class info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	
	@commands.command()
	async def info(self, ctx):
		await ctx.send(f"Currently serving {len(self.bot.guilds)}!")

def setup(bot):
	bot.add_cog(info(bot))