from discord.ext import commands
from db import Database
import re 
import discord
class blacklist(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.id == self.bot.user.id:
			return 

		if not message.guild:
			return

		blacklist = Database.get_guild(message.guild.id)["word_blacklist"]
		if blacklist:
			filtered_message = re.sub("(?i)[^a-z0-9]", "", message.content)
			for word in blacklist:
				if re.search(word, filtered_message):
					await message.delete()
					await message.author.send(f"The word `{word}` is banned! Try not to use it.")
					return

	@commands.command(aliases=['vbl', 'bannedwords'])
	@commands.has_permissions(administrator=True)
	async def viewBlacklist(self, ctx):
		blacklist = Database.get_guild(ctx.guild.id)["word_blacklist"]
		
		if not blacklist:
			return await ctx.send("The blacklist is empty.")

		blstring = ""

		for word in blacklist["blacklist_data"]:
			blstring = blstring + (f"\n- `{word}`")
		
		embed=discord.Embed(title="Banned Words", description=f"The blacklist contains:{blstring}", color=0x06c258)
		embed.set_footer(text="Pinebot")
		await ctx.send(embed=embed)
	
	@commands.command(aliases=['bl'])
	@commands.has_permissions(administrator=True)
	async def blacklist(self, ctx, word):
		guild_data = Database.get_guild(ctx.guild.id)
		blacklist = guild_data["word_blacklist"]
		word = word.lower()


		if word in blacklist:
			return await ctx.send(f"`{word}`` is already in the blacklist!")

		blacklist.append(word)

		Database.set_guild(ctx.guild.id, guild_data)
		await ctx.send(f"`{word}` has been added to the blacklist.")

	@commands.command(aliases=['unbl', 'wl', 'unblacklist'])
	@commands.has_permissions(administrator=True)
	async def whitelist(self, ctx, word):
		guild_data = Database.get_guild(ctx.guild.id)
		blacklist = guild_data["word_blacklist"]
		word = word.lower()

		if not word in blacklist:
			return await ctx.send(f"`{word}` is not in the blacklist!")

		try:
			blacklist.remove(word)
		except:
			await ctx.send("Something went wrong!")
		else:
			Database.set_guild(ctx.guild.id, guild_data)
			embed=discord.Embed(description=f"`{word}` has been removed from the blacklist.", color=0x06c258)
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(blacklist(bot))
