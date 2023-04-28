import asyncio, discord, traceback
from discord.ext import commands
from db import Database
import random

class blackjack(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.card_deck = [
			'<:A:1096575091464220702>', 
			'<:2:1096575139312836621>', 
			'<:3:1096575168027037746>', 
			'<:4:1096575169247580181>', 
			'<:5_:1096575170744950864>', 
			'<:6:1096575171764170762>', 
			'<:7:1096575173588684840>', 
			'<:8:1096575321551155290>', 
			'<:9:1096575174633078804>', 
			'<:10:1096575176008798258>', 
			'<:J:1096575179498459236>', 
			'<:Q:1096575181947936768>', 
			'<:K:1096575344389144688>']

	def smartSum(self, cards: list) -> int:
		cards_value = 0
		num_aces = 0
		for card in cards:
			if card == 0:  # ACE
				num_aces += 1
				cards_value += 11
			else:
				cards_value += min(card+1, 10)
			
			while cards_value > 21 and num_aces > 0:
				cards_value -= 10
				num_aces -= 1
		return cards_value
	
	def dealCard(self) -> int:
		return random.randint(0,12)

	def cardify(self, cards: list | int) -> str:
		if isinstance(cards, int):
			return self.card_deck[cards]
		
		card_str = ""
		for card in [self.card_deck[card] for card in cards]:
			card_str += card + ", "
		return card_str[:-2]
	
	def messageHeader(self, player_hand, dealer_hand) -> str:
		return f"Your Hand: {self.cardify(player_hand)}\n\nDealer's Hand: {self.cardify(dealer_hand)}\n"
	
	async def addReward(self, guild_id, user_id, bet):
		guild_data = await Database.get_guild(guild_id)
		guild_data['coins'][user_id] += bet*2
		await Database.set_guild(guild_id, guild_data)

	@commands.command(aliases=['blackjack'])
	@commands.max_concurrency(1, per=commands.BucketType.member)
	async def bj(self, ctx: commands.Context, bet: str):
		""""""
		try:
			if bet.isdigit():
				bet = int(bet)

			guild_data = await Database.get_guild(ctx.guild.id)
			if str(ctx.author.id) not in guild_data["coins"]:
				embed=discord.Embed(title = "Lol, Good Try!", description=f"Please Init your account first", color=discord.Color.red())
				return await ctx.send(embed=embed)
			elif isinstance(bet, int) and guild_data['coins'][str(ctx.author.id)] < bet:
				embed=discord.Embed(title = "Lol, BrOkE!", description=f"You have no pinecones", color=discord.Color.red())
				return await ctx.send(embed=embed)
			elif bet == "max" or bet == "all":
				bet = guild_data['coins'][str(ctx.author.id)]
			elif not isinstance(bet, int):
				return await ctx.send(embed=discord.Embed(description="Invalid Bet", colour=discord.Colour.red()))

			guild_data['coins'][str(ctx.author.id)] -= bet
			await Database.set_guild(ctx.guild.id, guild_data)

			player_hand = []
			dealer_hand = []
			player_hand.append(self.dealCard())
			player_hand.append(self.dealCard())
			dealer_hand.append(self.dealCard())
			dealer_hand.append(self.dealCard())

			main_msg = await ctx.reply(embed=discord.Embed(
				title="Welcome to BlackJack",
				description=self.messageHeader(player_hand, dealer_hand[0]),
				colour=0x06c258
			))
			while True:
				player_sum = self.smartSum(player_hand)
				if player_sum == 21:
					await self.addReward(ctx.guild.id, str(ctx.author.id), bet)
					return await main_msg.edit(embed=discord.Embed(description=self.messageHeader(player_hand, dealer_hand[0]) + f"You win!\n\nYou have ${(await Database.get_guild(ctx.guild.id))['coins'][str(ctx.author.id)]}.", colour=0x06c258))
				elif player_sum > 21:
					return await main_msg.edit(embed=discord.Embed(description=self.messageHeader(player_hand, dealer_hand[0]) + f"You busted!\n\nYou have ${(await Database.get_guild(ctx.guild.id))['coins'][str(ctx.author.id)]}.\nThat's why you don't gamble, kids.", colour=discord.Colour.red()))

				try:
					response = await self.bot.wait_for("message", check=lambda msg: msg.author.id==ctx.author.id, timeout=30)
					try:
						await response.delete()
					except:
						pass
				except asyncio.TimeoutError:
					return await main_msg.edit(embed=discord.Embed(title="Times Up!", description=f"{ctx.author.mention}, you took too long to respond...", colour=discord.Colour.red()))
			
				if response.content.lower() == "h" or "hit" in response.content.lower():
					player_hand.append(self.dealCard())
					main_msg = await main_msg.edit(embed=discord.Embed(description=self.messageHeader(player_hand, dealer_hand[0]), colour=0x06c258))
				elif response.content.lower() == "s" or "stand" in response.content.lower():
					break
				
			dealer_sum = self.smartSum(dealer_hand)
			while dealer_sum < 17:
				dealer_hand.append(self.dealCard())
				dealer_sum = self.smartSum(dealer_hand)
			
			result = self.messageHeader(player_hand, dealer_hand)
			colour = None
			if dealer_sum > 21:
				await self.addReward(ctx.guild.id, str(ctx.author.id), bet)
				result += "Dealer busted; you win!"
				colour = 0x06c258
			elif dealer_sum > player_sum:
				result += "Dealer wins!"
				colour = discord.Colour.red()
			elif dealer_sum < player_sum:
				await self.addReward(ctx.guild.id, str(ctx.author.id), bet)
				result += "You win!"
				colour=0x06c258
			else:
				await self.addReward(ctx.guild.id, str(ctx.author.id), int(bet/2))
				result += "Tie!"
				colour=discord.Colour.blue()
			
			result += f"\n\nYou have ${(await Database.get_guild(ctx.guild.id))['coins'][str(ctx.author.id)]}."
			await main_msg.edit(embed=discord.Embed(description=result, colour=colour))
		except Exception as e:
			traceback.print_exception(e)

async def setup(bot: commands.Bot):
	await bot.add_cog(blackjack(bot))

