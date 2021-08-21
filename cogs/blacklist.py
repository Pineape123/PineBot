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

		blacklist = Database.find('blacklists', {'guild_id': message.guild.id})
		if blacklist:
			filtered_message = re.sub("[(?i)[^a-z0-9]", "", message.content)
			for word in blacklist["blacklist_data"]:
				if re.search(word, filtered_message):
					await message.delete()
					await message.author.send(f"The word `{word}` is banned! Try not to use it.")
					return

	@commands.command(aliases=['vbl', 'bannedwords'])
	@commands.has_permissions(administrator=True)
	async def viewBlacklist(self, ctx):
		blacklist = Database.find('blacklists', {'guild_id': ctx.guild.id})

		if not blacklist:
			blacklist = {
				"guild_id": ctx.guild.id,
				"blacklist_data": []
			}
			result = Database.insert('blacklists', blacklist)
			blacklist = Database.find("blacklists", {"_id":result.inserted_id})

		if not blacklist["blacklist_data"]:
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
		blacklist = Database.find("blacklists", {"guild_id": ctx.guild.id})
		word = word.lower()

		if not blacklist:
			blacklist = {
				"guild_id": ctx.guild.id,
				"blacklist_data": []
			}
			result = Database.insert('blacklists', blacklist)
			blacklist = Database.find("blacklists", {"_id":result.inserted_id})

		if word in blacklist["blacklist_data"]:
			return await ctx.send(f"`{word}`` is already in the blacklist!")

		blacklist["blacklist_data"].append(word)

		Database.update("blacklists", {"guild_id": ctx.guild.id}, {"$set": {"blacklist_data": blacklist["blacklist_data"]}})
		await ctx.send(f"`{word}` has been added to the blacklist.")

	@commands.command(aliases=['unbl', 'wl', 'unblacklist'])
	@commands.has_permissions(administrator=True)
	async def whitelist(self, ctx, word):
		blacklist = Database.find("blacklists", {"guild_id": ctx.guild.id})
		word = word.lower()

		if not blacklist:
			blacklist = {
				"guild_id": ctx.guild.id,
				"blacklist_data": []
			}
			result = Database.insert('blacklists', blacklist)
			blacklist = Database.find("blacklists", {"_id":result.inserted_id})

		if not word in blacklist["blacklist_data"]:
			return await ctx.send(f"`{word}` is not in the blacklist!")

		try:
			blacklist["blacklist_data"].remove(word)
		except:
			await ctx.send("Something went wrong!")
		else:
			Database.update("blacklists", {"guild_id": ctx.guild.id}, {"$set": {"blacklist_data": blacklist["blacklist_data"]}})
			embed=discord.Embed(description=f"`{word}` has been removed from the blacklist.", color=0x06c258)
			await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(blacklist(bot))