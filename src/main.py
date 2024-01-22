import os
import asyncio
from discord.ext import commands
import discord
from utils.config import BOT_TOKEN
from aiohttp.web import AppRunner, Application, TCPSite, RouteTableDef

routes = RouteTableDef()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

@routes.get('/healthCheck')
async def handle(request):
    return web.Response(text="OK")

@bot.event
async def on_ready():
    print(f"Login: {bot.user} Success.")


# load cog file


@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


# unload cog


@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")


# reload cog file.


@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    app = Application()
    app.add_routes(routes)
    
    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    if BOT_TOKEN is None:
        raise ValueError("Not found BOT_TOKEN")

    app['bot'] = bot
        
    try:
        async with bot:
            await load_extensions()
            await bot.start(BOT_TOKEN)

    except:
        bot.close(),
        raise

    finally:
        await runner.cleanup()



if __name__ == "__main__":
    asyncio.run(main())
