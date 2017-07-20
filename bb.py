import asyncio
import logging
import traceback

import config
import database

import discord
from discord.ext import commands

DESCRIPTION = '''Blitzcrank Bot is a Discord bot written by Frosty ☃#5263 to pull various statsitics
               from Riot's API for a given summoner. All commands should be prefixed with 'b!'
               (for example, b!stats)'''

STARTUP_EXTENSIONS = ['utilities', 'summoner_stats', 'static_data', 'default_regions', 'reload']


class BlitzcrankBot(commands.AutoShardedBot):
    """Main"""

    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('b!'), description=DESCRIPTION)
        self.bot_token = config.TOKEN
        self.api_key = config.API

        for extension in STARTUP_EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

    # logging
    logger1 = logging.getLogger('discord')
    logger1.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger1.addHandler(handler)

    async def on_ready(self):
        """Sets game presence and indicates when ready."""
        game = 'bl!help | Fleshling Compatibility Service'
        await self.change_presence(game=discord.Game(name=game))
        print('Logged in as:\n{0} (ID: {0.id})'.format(self.user))
        print('--------------------------------')

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_command(self, ctx):
        """Log command calls to file"""
        destination = None
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            destination = 'Private message'
        else:
            destination = '#{0.channel.name}: {0.guild.name})'.format(ctx.message)

        self.logger1.info('{0.created_at}: {0.author} in {1}: {0.content}'.format(ctx.message, destination))

    async def on_command_error(self, ctx, error):
        """Error handling"""
        error_msg = None
        self.logger1.error(ctx.message.content + ": " + str(error))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if isinstance(original, discord.Forbidden):
                error_msg = ("I need to have the 'embed links' permission to run properly!")
            else:
                error_msg = 'Something unexpected went wrong, sorry :I'

            print('{0.created_at}: {0.author}: {0.content}'.format(ctx.message))
            print(error)
            await ctx.send(error_msg)
            await ctx.send("If you feel like this shouldn't be happening, feel free to join my support server with b!support.")
        else:
            print('{0.created_at}: {0.author}: {0.content}'.format(ctx.message))
            print(str(error))

    async def on_guild_join(self, guild):
        """Check for bot collection"""
        l = list(filter(lambda m: m.bot, guild.members))
        members = len(guild.members)
        if len(l) / members >= .55:
            bots = "{0}% bots".format(100 * (len(l) / members))
            await guild.default_channel.send("To avoid bot collection servers, I auto leave any server where 55% or above of the users are bots, sorry!")
            await guild.leave()
            embed = discord.Embed(title="Left Server", colour=0x1affa7)
            embed.add_field(name="Server:", value=guild.name, inline=True)
            embed.add_field(name="Reason:", value="Bot collection server", inline=True)
            embed.add_field(name="Users:", value=members, inline=True)
            embed.add_field(name="Justification:", value=bots, inline=True)
            channel = self.get_channel(295831639219634177)
            await channel.send('', embed=embed)
        else:
            embed = discord.Embed(title="Joined Server", colour=0x1affa7)
            embed.add_field(name="Server:", value=guild.name, inline=True)
            embed.add_field(name="Users:", value=members, inline=True)
            embed.add_field(name="Total:", value=len(self.guilds), inline=True)
            channel = self.get_channel(295831639219634177)
            await channel.send('', embed=embed)
            await guild.default_channel.send("Beep, boop! To set up a default LoL region for my lookup commands, please use the `b!region set` command! (Example, `b!region set OCE`)")
            db = database.Database("guilds.db")
            db.add_table(str(guild.id))
            db.close_connection()

    def run(self):
        super().run(self.bot_token, reconnect=True)


if __name__ == '__main__':
    BlitzcrankBot().run()

# Base finished
