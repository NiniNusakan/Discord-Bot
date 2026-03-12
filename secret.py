import typing

import discord
from discord.ext import commands

intents = discord.Intents.default()

bot = commands.Bot(command_prefix=commands.when_mentioned, description="Nothing to see here!", intents=intents)

the hidden keyword argument hides it from the help command.
@bot.group(hidden=True)
async def secret(ctx: commands.Context):
"""What is this "secret" you speak of?"""
if ctx.invoked_subcommand is None:
await ctx.send('Shh!', delete_after=5)

def create_overwrites(ctx, *objects):
"""This is just a helper function that creates the overwrites for the
voice/text channels.

A `discord.PermissionOverwrite` allows you to determine the permissions
of an object, whether it be a `discord.Role` or a `discord.Member`.

In this case, the `view_channel` permission is being used to hide the channel
from being viewed by whoever does not meet the criteria, thus creating a
secret channel.
"""

# a dict comprehension is being utilised here to set the same permission overwrites
# for each `discord.Role` or `discord.Member`.
overwrites = {obj: discord.PermissionOverwrite(view_channel=True) for obj in objects}

# prevents the default role (@everyone) from viewing the channel
# if it isn't already allowed to view the channel.
overwrites.setdefault(ctx.guild.default_role, discord.PermissionOverwrite(view_channel=False))

# makes sure the client is always allowed to view the channel.
overwrites[ctx.guild.me] = discord.PermissionOverwrite(view_channel=True)

return overwrites
