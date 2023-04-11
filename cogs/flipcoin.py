import discord
from discord.ext import commands
import random

class flipcoin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(aliases=['flip', 'cointoss', 'coin', 'flipacoin', 'coinflip'] )
	async def flipcoin(self, ctx):
		x = random.choice(['Heads!', 'Tails!'])
		await ctx.reply(x)
		

async def setup(bot: commands.Bot):
	await bot.add_cog(flipcoin(bot))