import discord
import pytz
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from model import Model


class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} is online')

    @app_commands.command()
    async def time(self, interaction: discord.Interaction, target: discord.User | None):

        uid = [interaction.user.id,]
        if target is not None:
            uid = [interaction.user.id, target.id,]

        connection = Model("timebot")

        timezones = await connection.getUsersTimezone(uid)

        uid_timezones = {}
        for timezone in timezones:
            uid_timezones[timezone['uid']] = timezone['timezone']

        if target.id not in uid_timezones:
            await interaction.response.send_message(
                f'{target.display_name} does not have a Timezone set. They can set it with /set_timezone',
                ephemeral=True
            )

        if interaction.user.id not in uid_timezones:
            await interaction.response.send_message(
                f'You don\'t have a Timezone set. You can set it with /set_timezone',
                ephemeral=True
            )

        if target is None:
            await interaction.response.send_message(
                f'Current Time: {datetime.now(pytz.timezone(uid_timezones[str(interaction.user.id)])).strftime("%H:%M:%S")}',
                ephemeral=True)
        await interaction.response.send_message(
            f'Your Current Time: {datetime.now(pytz.timezone(uid_timezones[str(interaction.user.id)])).strftime("%H:%M:%S")}\n'
            f'{target.display_name}\'s Current Time: {datetime.now(pytz.timezone(uid_timezones[str(target.id)])).strftime("%H:%M:%S")}',
            ephemeral=True)


async def setup(bot):
    await bot.add_cog(Time(bot))
