from discord.ext import commands
from discord import app_commands
from model import Model
import discord
import pytz

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} is online')

    @app_commands.command()
    async def set_timezone(self, interaction: discord.Interaction, timezone: str, target: discord.User | None):
        if timezone not in pytz.all_timezones:
            await interaction.response.send_message('Invalid timezone specified', ephemeral=True)

        uid = interaction.user.id
        if target is not None and interaction.user.guild_permissions.administrator:
            uid = target.id

        connection = Model("timebot")

        user = await connection.getTimebotUser(uid)

        if len(user) == 0:
            await connection.insertUserTimezone(uid, timezone)
        else:
            await connection.updateUserTimezone(uid, timezone)

        await interaction.response.send_message(
            f'Timezone set to {timezone}.',
            ephemeral=True)


async def setup(bot):
    await bot.add_cog(Config(bot))
