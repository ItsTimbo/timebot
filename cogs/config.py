from datetime import datetime
from MySQLdb import connect
from mysql.connector import errorcode
from discord.ext import commands
from discord import app_commands
import discord
import pytz
import mysql.connector


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

        timezone_time = pytz.timezone(timezone)
        uid = interaction.user.id
        if target is not None and interaction.user.guild_permissions.administrator:
            uid = target.id

        try:
            connection = connect(host="127.0.0.1", user="timebot", password="DoJ6_vf)JFZxfsPt", database="timebot")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM timebot WHERE uid = %s", (str(uid),))

            user = cursor.fetchall()

            query = "UPDATE timebot SET timezone = %s WHERE uid = %s"
            if len(user) == 0:
                query = "INSERT INTO timebot (timezone, uid) VALUES (%s, %s)"

            try:
                cursor.execute(query, (str(timezone), str(uid),))
                connection.commit()
            except mysql.connector.Error as err:
                print(err)
                interaction.response.send_message('There was an error setting the timezone', ephemeral=True)
            else:
                connection.close()
                await interaction.response.send_message(
                    f'Timezone set to {timezone}. Current time: {datetime.now(timezone_time).strftime("%H:%M:%S")}',
                    ephemeral=True)


async def setup(bot):
    await bot.add_cog(Config(bot))
