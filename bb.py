import asyncio
import logging
import traceback

import aiohttp
import websockets

import config

import discord
from discord.ext import commands

DESCRIPTION = '''Blitzcrank Bot is a Discord bot written by Frosty ☃#5263 to pull various statsitics
               from Riot's API for a given summoner. All commands should be prefixed with 'b!'
               (for example, b!stats)'''

STARTUP_EXTENSIONS = ['utilities', 'summoner_stats', 'static_data', 'reload']

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

    #logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    async def on_ready(self):
        """Sets game presence and indicates when ready."""
        game = 'bl!help | Fleshling Compatibility Service'
        await self.change_presence(game=discord.Game(name=game))
        print('Logged in as:\n{0} (ID: {0.id})'.format(self.user))
        print('--------------------------------')

    async def on_message(self, message):
        """Functions that are not part of ext for various reasons."""
        #eval command here because idk how to get it to work in cogs
        if message.content.startswith('b!eval') and message.author.id == config.OWNER_ID:
            parameters = ' '.join(message.content.strip().split(' ')[1:])
            output = None
            try:
                temp = 'Executing: ' + message.content + ' one moment, please...'
                originalmessage = await message.channel.send(temp)
                output = eval(parameters)
            except Exception:
                error = "```fix\n" + str(traceback.format_exc()) + "\n```"
                await originalmessage.edit(content=error)
                traceback.print_exc()
            if asyncio.iscoroutine(output):
                output = await output
            if output:
                success = "```fix\n" + str(output) + "\n```"
                await originalmessage.edit(content=success)
        await self.process_commands(message)

    async def on_command(self, ctx):
        message = ctx.message
        destination = None
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            destination = 'Private message'
        else:
            destination = '#{0.channel.name}: {0.guild.name})'.format(message)

        self.logger.info('{0.created_at}: {0.author} in {1}: {0.content}'.format(message,
                                                                                 destination))

    async def on_command_error(self, error, ctx):
        """Error handling"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        elif isinstance(error, commands.TooManyArguments):
            error_msg = ('Too many arguments! If you are trying to use a champion or summoner name '
                         'that has a space, please enclose it in ""s (double quotes)')
        elif isinstance(error, commands.CommandInvokeError):
            if str(error).startswith('Command raised an exception: APIError: Server'
                                     ' returned error 404 on call'):
                error_msg = ('Could not find ranked statistics! Please ensure your summoner name is'
                             ' spelt correctly, and that you are level 30 and have completed your '
                             'placement games')
            elif str(error).startswith("Command raised an exception: AttributeError"
                                       ": 'NoneType' object has no attribute 'id'"):
                error_msg = ('Could not find the champion to lookup! Please use capitals for '
                             'champion names (i.e "Teemo" not "teemo")')
            elif str(error).startswith('Command raised an exception: APIError: Server'
                                       ' returned error 403 on call'):
                error_msg = ('My API key expired! Please be patient while we wait for Riot to '
                             'approve of my production API key :)')
            else:
                await ctx.send("Something unexpected went wrong, sorry :I")

            print(ctx.message.content)
            print(error)
            await ctx.send(error_msg)
            await ctx.send("If you feel like this shouldn't be happening, "
                               "feel free to join my support server with b!support")

    async def on_guild_join(self, guild):
        """Check for bot collection"""
        l = list(filter(lambda m: m.bot, guild.members))
        members = len(guild.members)
        if len(l) / members >= .55:
            bots = "{0}% bots".format(100 * (len(l) / members))
            await guild.default_channel.send("To avoid bot collection servers, I auto leave any "
                                             "server where 55% or above of the users are bots, "
                                             "sorry!")
            await guild.leave(guild)
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

    def run(self):
        super().run(config.TOKEN, reconnect=True)

if __name__ == '__main__':
    BlitzcrankBot().run()

#Base finished