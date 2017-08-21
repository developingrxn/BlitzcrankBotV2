'''
Created on 23Jul.,2017

@author: Alex Palmer | SuperFrosty
'''
import json
import logging
import requests
import collections

import discord
from discord.ext import commands
import exceptions

import database


class Events:

    def __init__(self, bot):
        self.bot = bot

    # logging
    logger1 = logging.getLogger('discord')
    logger1.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger1.addHandler(handler)

    async def post_stats(self):
        dbots_url = 'https://bots.discord.pw/api/bots/282765243862614016/stats'
        dbots_org_url = 'https://discordbots.org/api/bots/282765243862614016/stats'
        dbots_header = {'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2NjE0MTIwMTYzMTI4NTI0OCIsInJhbmQiOjc5MSwiaWF0IjoxNDg3MDQwMzMzfQ.xGa4_BIw0qufQHKecuUZ2WzeDD5lEGxttsf5GNhfJXg", 'Content-Type': 'application/json'}
        dbots_org_header = {
            'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2MTQxMjAxNjMxMjg1MjQ4IiwiaWF0IjoxNTAwNTU4MTE5fQ.e-Yh1jzGMXOIQl0DkiG2QL5GOxK_wAKf3aaX7ZKiBV4", 'Content-Type': 'application/json'}
        dbots_payload = json.dumps({'server_count': len(self.bot.guilds)})
        sharded_guilds = collections.Counter(
            x.shard_id for x in self.bot.guilds)
        d = []
        for shard in sharded_guilds:
            d.append(sharded_guilds[shard])
        dbots_org_payload = json.dumps({'shards': d})
        requests.post(dbots_url, data=dbots_payload, headers=dbots_header)
        requests.post(dbots_org_url, data=dbots_org_payload,
                      headers=dbots_org_header)

    async def on_ready(self):
        """Sets game presence and indicates when ready."""
        game = 'bl!help | Fleshling Compatibility Service'
        await self.bot.change_presence(game=discord.Game(name=game))
        print('Logged in as:\n{0} (ID: {0.id})'.format(self.bot.user))
        print('--------------------------------')

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.bot.process_commands(message)

    async def on_command(self, ctx):
        """Log command calls to file"""
        destination = None
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            destination = 'Private message'
        else:
            destination = '#{0.channel.name}: {0.guild.name})'.format(
                ctx.message)

        self.logger1.info('{0.created_at}: {0.author} in {1}: {0.content}'.format(
            ctx.message, destination))

    async def on_command_error(self, ctx, error):
        """Error handling"""
        error_msg = None
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if isinstance(original, discord.Forbidden):
                await ctx.send("I need to have the 'embed links' permission to send messages!")
                return
            elif isinstance(original, exceptions.Halt):
                return

            print('{0.created_at}: {0.author}: {0.content}'.format(ctx.message))
            print(error)
            embed = discord.Embed(title="An unexpected error occured :I", colour=0xCA0147,
                                  description="If you feel like this shouldn't be happening [click here to join my support server](https://discord.gg/UP4TwFX).")
            await ctx.send("", embed=embed)
        else:
            print('{0.created_at}: {0.author}: {0.content}'.format(ctx.message))
            print(str(error))

    async def on_guild_join(self, guild):
        """Check for bot collection"""
        l = list(filter(lambda m: m.bot, guild.members))
        members = len(guild.members)
        if len(l) / members >= .55:
            bots = "{0:.0F}% bots".format(100 * (len(l) / members))
            channel_test = discord.utils.find(lambda c: c.permissions_for(
                c.guild.me).send_messages, guild.text_channels)
            await channel_test.send("To avoid bot collection servers, I auto leave any server where 55% or above of the users are bots, sorry!")
            await guild.leave()
            embed = discord.Embed(title="Left Server", colour=0x1affa7)
            embed.add_field(name="Server:", value=guild.name, inline=True)
            embed.add_field(
                name="Reason:", value="Bot collection server", inline=True)
            embed.add_field(name="Users:", value=members, inline=True)
            embed.add_field(name="Justification:", value=bots, inline=True)
            channel = self.bot.get_channel(295831639219634177)
            await channel.send('', embed=embed)
        else:
            embed = discord.Embed(title="Joined Server", colour=0x1affa7)
            embed.add_field(name="Server:", value=guild.name, inline=True)
            embed.add_field(name="Users:", value=members, inline=True)
            embed.add_field(name="Total:", value=len(
                self.bot.guilds), inline=True)
            channel = self.bot.get_channel(295831639219634177)
            await channel.send('', embed=embed)
            channel_test = discord.utils.find(lambda c: c.permissions_for(
                c.guild.me).send_messages, guild.text_channels)
            await channel_test.send("Beep, boop! To set up a default LoL region for my lookup commands, please use the `b!region set` command! (Example, `b!region set OCE`)")
            db = database.Database("guilds.db")
            db.add_table(str(guild.id))
            db.close_connection()
            await self.post_stats()

    async def on_guild_remove(self, guild):
        await self.post_stats()
        pass


def setup(bot):
    """Adds cog to bot"""
    bot.add_cog(Events(bot))
