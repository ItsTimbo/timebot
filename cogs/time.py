import json

import discord
import mysql.connector
import pytz
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from mysql.connector import errorcode
from MySQLdb import connect, cursors


class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} is online')

    @app_commands.command()
    async def time(self, interaction: discord.Interaction, target: discord.User | None):

        uid = (interaction.user.id,)
        if target is not None:
            uid = (interaction.user.id, target.id,)

        with open('./settings.json', 'r') as file:
            data = json.load(file)['db']

        try:
            connection = connect(host=data['host'],
                                 user=data['user'],
                                 password=data['password'],
                                 database=data['database'],
                                 cursorclass=cursors.DictCursor)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cursor = connection.cursor()
            cursor.execute("SELECT uid, timezone FROM timebot WHERE uid IN %s", (uid,))
            timezones = cursor.fetchall()

            uid_timezones = {}
            for timezone in timezones:
                uid_timezones[timezone['uid']] = timezone['timezone']

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
