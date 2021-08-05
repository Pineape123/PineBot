from discord.ext import commands
from db import Database

class blacklist(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		pass

	@commands.command(Adminstrator=True, aliases=['vbl'])
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

		blstring = "\n- ".join(blacklist["blacklist_data"])

		await ctx.send(f"The blacklist contains:\n{blstring}")

	@commands.command(Adminstrator=True, aliases=['bl'])
	async def blacklist(self, ctx, word):
		blacklist = Database.find("blacklists", {"guild_id": ctx.guild.id})

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
		await ctx.send(f"`{word}` has been added from the blacklist.")

	@commands.command(Adminstrator=True, aliases=['unbl', 'wl', 'unblacklist'])
	async def whitelist(self, ctx, word):
		blacklist = Database.find("blacklists", {"guild_id": ctx.guild.id})

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
			await ctx.send(f"`{word}` has been removed from the blacklist.")

def setup(bot):
	bot.add_cog(blacklist(bot))