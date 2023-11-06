import asyncio
import logging

from discord import AllowedMentions
from discord.ext import commands

from django.conf import settings

logger = logging.getLogger(__name__)


class Remind(commands.Cog):
    """
    Set reminders
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='remind', description="Set a Reminder", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def reminder(self, ctx, reminder: str, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
        counter = seconds + minutes * 60 + hours * 60 * 60 + days * 60 * 60 * 24
        await ctx.respond(f"Alright, I will remind you about {reminder} in {seconds}s {minutes}m {hours}h {days}d.", allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False))
        await asyncio.sleep(counter)
        await ctx.respond(f"{ctx.user.mention} Hi, you asked me to remind you about {reminder}, {seconds}s {minutes}m {hours}h {days}d ago.", allowed_mentions=AllowedMentions(everyone=False, roles=False, users=[ctx.user]))


def setup(bot):
    bot.add_cog(Remind(bot))
