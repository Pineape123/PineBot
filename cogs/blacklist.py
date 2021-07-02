import discord, json
from discord.ext import commands

class blacklist(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.listener()
	async def on_message(message):
		pass

	@commands.command(Adminstrator=True, aliases=['vbl', 'viewblacklist'])
	async def viewBlacklist(self, ctx):
		with open('/blacklist.json', 'r') as f:
			blacklist = json.load(f)

			if not str(ctx.guild.id) in blacklist:
				return await ctx.send("The blacklist is empty.")

			blstring = "\n".join(blacklist)

			await ctx.send(f"The blacklist contains: {blstring}")

	@commands.command(Adminstrator=True, aliases=['bl'])
	async def blacklist(self, ctx, word):
		with open('./blacklist.json', 'r') as f:
			blacklist = json.load(f)

			if not str(ctx.guild.id) in blacklist:
				blacklist[str(ctx.guild.id)] = []

			if word in blacklist[str(ctx.guild.id)]:
				return await ctx.send(f"Dw, `{word}` is already in the blacklist!")

			blacklist[str(ctx.guild.id)].append(word)

			with open('./blacklist.json', 'w') as f:
				json.dump(blacklist, f, indent=4)
				await ctx.send(f'`{word}`` has been added to the blacklist.')

	@commands.command(Adminstrator=True, aliases=['unbl', 'wl', 'unblacklist'])
	async def whitelist(self, ctx, word):
		with open('./blacklist.json', 'r') as f:
			blacklist = json.load(f)

			if not str(ctx.guild.id) in blacklist:
				blacklist[str(ctx.guild.id)] = []

			if not word in blacklist[str(ctx.guild.id)]:
				return await ctx.send(f"`{word}` is not in the blacklist!")

			try:
				blacklist[str(ctx.guild.id)].remove(word)
			except:
				await ctx.send("We're sorry but something went wrong and we weren't able to remove the word from the blacklist. Please try again or contact the owner of the bot.")
			else:
				with open('./blacklist.json', 'w') as f:
					json.dump(blacklist, f, indent=4)
					await ctx.send(f'`{word}`` has been removed from the blacklist.')