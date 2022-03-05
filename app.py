"""A simple FastAPI server/Discord client that returns users' roles."""
import asyncio
import json

import discord

import fastapi


server = fastapi.FastAPI()
client: discord.Client = None

with open("config.json") as config_file:
    config = json.load(config_file)

TOKEN = config["bot_token"]
GUILD_ID = config["guild_id"]


@server.on_event("startup")
async def startup():
    """Connect the Discord client."""
    global client
    loop = asyncio.get_running_loop()
    client = discord.Client(loop=loop)
    loop.create_task(client.start(TOKEN))


@server.get("/users/{user_id}/roles")
async def test_endpoint(user_id: int) -> dict:
    """Get a user's roles."""
    guild = client.get_guild(GUILD_ID)
    try:
        member = await guild.fetch_member(user_id)
    except discord.NotFound:
        raise fastapi.HTTPException(status_code=404, detail="User not found.")
    return {
        "roles": [
            {"name": role.name, "id": role.id}
            for role in member.roles
            if not role.is_default()
        ]
    }


@server.get("/bans")
async def ban_endpoint():
    """Get a guilds bans."""
    guild = client.get_guild(GUILD_ID)
    try:
        ban_list = await guild.bans()

    except discord.errors.Forbidden:
        raise fastapi.HTTPException(status_code=403, detail="Missing Permissions")
    
    return {
        "bans": [
            {
                "user_id": ban_entry.user.id,
                "user_name": ban_entry.user.name,
                "user_discriminator": ban_entry.user.discriminator,
                "user_is_bot": ban_entry.user.bot,
                "reason": ban_entry.reason,
            }
            for ban_entry in ban_list
        ]
    }
