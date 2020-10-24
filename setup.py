import configparser
import json

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="@", intents=discord.Intents(guilds=True, messages=True))
config = configparser.ConfigParser()

token = input("Input a bot token: ")
main_server = int(input("What is the ID of the main server for your bot? (Suggestions, errors, and other stuff will be sent here): "))
trusted_ids = input("Input a list of trusted user IDs (allowing for moderation commands such as -dm, -refreshroles, -lookupinfo, and others.): ").split(", ")

def write_blank_json(name, type):
    with open(name, "x") as f:
        json.dump(type, f)

try:
    write_blank_json("settings.json", dict())
    write_blank_json("blocked_users.json", list())
except:
    print("Failed making one of the files! If you are resetting to default, delete the servers folder, all .txt, .json, and the .ini file before running this again!")
    raise SystemExit

config["Main"] = {
  "token": token,
  "main_server": main_server,
  "trusted_ids": trusted_ids,
}

config["Activity"] = {
    "name": "my owner set me up!",
    "type": "watching",
    "status": "idle",
}

@bot.event
async def on_ready():
    global config
    global logs

    guild = bot.get_guild(main_server)
    botcategory = await guild.create_category("Folding@Home Stats")
    overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False)}

    logs = await guild.create_text_channel("logs", category=botcategory, overwrites=overwrites)
    errors = await guild.create_text_channel("errors", category=botcategory, overwrites=overwrites)
    servers = await guild.create_text_channel("servers", category=botcategory, overwrites=overwrites)
    suggestions = await guild.create_text_channel("suggestions", category=botcategory, overwrites=overwrites)

    config["Channels"] = {
        "logs": logs.id,
        "errors": errors.id,
        "servers": servers.id,
        "suggestions": suggestions.id,
    }

    await logs.send(f"Are you sure you want {[str(bot.get_user(int(trusted_id))) for trusted_id in trusted_ids]} to be trusted? (do -yes to accept)")


@bot.command()
@commands.is_owner()
async def yes(ctx):
    with open("config.ini", "x") as configfile:
        config.write(configfile)

    await logs.send("Finished and written to config.ini, change the names of the channels all you want and Folding@Home Stats Bot should be startable!")
    await bot.close()

@bot.command()
@commands.is_owner()
async def no(ctx):
    await bot.close()

bot.run(token)
