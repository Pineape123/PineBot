import discord
from discord.ext import commands

class onmessageping(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.content == "<@966917475486818344>":
			prefix = await self.bot.get_prefix(message)
			embed=discord.Embed(description=f"My current prefix is `{prefix}`\n\nTo change my prefix run `{prefix}changeprefix <prefix>`", color=0x06c258)
			await message.reply(embed=embed)

def setup(bot):
	bot.add_cog(onmessageping(bot))
