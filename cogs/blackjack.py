import asyncio, discord, traceback
from discord.ext import commands
from db import Database
import random

class blackjack(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.card_deck = [':regional_indicator_a:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:', ':regional_indicator_j:', ':regional_indicator_q:', ':regional_indicator_k:']

	def smartSum(self, cards: list) -> int:
		cards_value = 0
		num_aces = 0
		for card in cards:
			if card == 0:  # ACE
				num_aces += 1
				cards_value += 11
			else:
				cards_value += min(card, 10)
			
			while cards_value > 21 and num_aces > 0:
				cards_value -= 10
				num_aces -= 1
		return cards_value
	
	def dealCard(self) -> int:
		return random.randint(0,13)

	def cardify(self, cards: list | int) -> str:
		if isinstance(cards, int):
			return self.card_deck[cards]
		
		card_str = ""
		for card in [self.card_deck[card] for card in cards]:
			card_str += card + ", "
		return card_str[:-2]
	
	def messageHeader(self, player_hand, dealer_hand) -> str:
		return f"Your Hand: {self.cardify(player_hand)}\nDealer's Hand: {self.cardify(dealer_hand)}\n"
	
	async def addReward(self, guild_id, user_id, bet):
		guild_data = await Database.get_guild(guild_id)
		guild_data['coins'][user_id] += bet*2
		await Database.set_guild(guild_id, guild_data)

	@commands.command()
	async def bj(self, ctx: commands.Context, bet: int):
		""""""
		try:
			guild_data = await Database.get_guild(ctx.guild.id)

			if str(ctx.author.id) not in guild_data["coins"]:
				await ctx.send("Please init your account first.")

			elif guild_data['coins'][str(ctx.author.id)] < bet:
				await ctx.send("You do not have enough coins.")
			
			else:
				guild_data['coins'][str(ctx.author.id)] -= bet
				await Database.set_guild(ctx.guild.id, guild_data)

				player_hand = []
				dealer_hand = []
				player_hand.append(self.dealCard())
				player_hand.append(self.dealCard())
				dealer_hand.append(self.dealCard())
				dealer_hand.append(self.dealCard())

				main_msg = await ctx.send("Welcome to BlackJack\n\n" + self.messageHeader(player_hand, dealer_hand[0]))
				while True:
					player_sum = self.smartSum(player_hand)
					if player_sum == 21:
						await self.addReward(ctx.guild.id, str(ctx.author.id), bet)
						return await main_msg.edit(content=self.messageHeader(player_hand, dealer_hand[0]) + f"You win!\n\nYou have ${(await Database.get_guild(ctx.guild.id))['coins'][str(ctx.author.id)]}.")
					elif player_sum > 21:
						return await main_msg.edit(content=self.messageHeader(player_hand, dealer_hand[0]) + f"You busted!\n\nYou have ${(await Database.get_guild(ctx.guild.id))['coins'][str(ctx.author.id)]}.")

					try:
						response = await self.bot.wait_for("message", check=lambda msg: msg.author.id==ctx.author.id, timeout=30)
						try:
							await response.delete()
						except:
							pass
					except asyncio.TimeoutError:
						return await main_msg.edit(content=f"{ctx.author.mention}, you took too long to respond...")
				
					if response.content.lower() == "h" or "hit" in response.content:
						player_hand.append(self.dealCard())
						main_msg = await main_msg.edit(content=self.messageHeader(player_hand, dealer_hand[0]))
					elif response.content.lower() == "s" or "stand" in response.content:
						break
					
				dealer_sum = self.smartSum(dealer_hand)
				while dealer_sum < 17:
					dealer_hand.append(self.dealCard())
					dealer_sum = self.smartSum(dealer_hand)
				
				result = self.messageHeader(player_hand, dealer_hand)
				if dealer_sum > 21:
					await self.addReward(ctx.guild.id, str(ctx.author.id), bet)
					result += "Dealer busted; you win!"
				elif dealer_sum > player_sum:
					result += "Dealer wins!"
				elif dealer_sum < player_sum:
					await self.addReward(ctx.guild.id, str(ctx.author.id), bet)
					result += "You win!"
				else:
					result += "Tie!"
				
				result += f"\n\nYou have ${(await Database.get_guild(ctx.guild.id))['coins'][str(ctx.author.id)]}."
				await main_msg.edit(content=result)
		except Exception as e:
			traceback.print_exception(e)


async def setup(bot: commands.Bot):
	await bot.add_cog(blackjack(bot))

