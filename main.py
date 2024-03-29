import discord
from discord.ext import commands
import asyncio, os, json
from db import Database

Database.init()


async def get_prefix(bot, message):
    if message.guild is None:
        return commands.when_mentioned_or("!")(bot, message)
    prefix = (await Database.get_guild(message.guild.id))["custom_prefix"]
    return commands.when_mentioned_or(prefix or "!")(bot, message)


bot = commands.Bot(
    command_prefix=get_prefix, case_insensitive=True, intents=discord.Intents.all()
)


from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    guild_data = await Database.get_guild(ctx.guild.id)

    guild_data["custom_prefix"] = prefix

    await Database.set_guild(ctx.guild.id, guild_data)


@bot.command(aliases=["lo"])
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    try:
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send(f'Loaded "{extension}".')
        print(f'Loaded "{extension}".')
    except Exception as e:
        print(e)


@bot.command(aliases=["un"])
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    try:
        await bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f'Unloaded "{extension}".')
        print(f'Unloaded "{extension}".')
    except Exception as e:
        print(e)


@bot.command(aliases=["re"])
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    try:
        await bot.unload_extension(f"cogs.{extension}")
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send(f'Reloaded "{extension}".')
        print(f'Reloaded "{extension}".')
    except Exception as e:
        print(e)


@bot.command()
async def listcogs(ctx):
    embed = discord.Embed(title="Loaded Cogs", color=0x06C258)
    embed.set_footer(text="PineBot")
    for cogname in bot.cogs.keys():
        embed.add_field(
            name=f"{str.capitalize(cogname)}:", value=f":white_check_mark: {cogname}"
        )
    await ctx.send(embed=embed)


async def run_bot():
    async with bot:
        print("Loading Cogs...")
        for fileName in os.listdir("./cogs"):
            try:
                await bot.load_extension(f"cogs.{fileName[:-3]}")
            except Exception:
                print(f"Failed to load {fileName}")

        print("Starting Bot...")
        await bot.start(TOKEN)


asyncio.run(run_bot())
