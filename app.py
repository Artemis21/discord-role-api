"""A simple FastAPI server/Discord client that returns users' roles."""
import asyncio
import json

import discord

import fastapi


server = fastapi.FastAPI()
client: discord.Client = None

with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config['bot_token']
GUILD_ID = config['guild_id']


@server.on_event('startup')
async def startup():
    """Connect the Discord client."""
    global client
    loop = asyncio.get_running_loop()
    client = discord.Client(loop=loop)
    loop.create_task(client.start(TOKEN))


@server.get('/users/{user_id}/roles')
async def test_endpoint(user_id: int) -> dict:
    """Get a user's roles."""
    guild = client.get_guild(GUILD_ID)
    try:
        member = await guild.fetch_member(user_id)
    except discord.NotFound:
        raise fastapi.HTTPException(status_code=404, detail='User not found.')
    return {
        'roles': [
            {
                'name': role.name,
                'id': role.id
            } for role in member.roles if not role.is_default()
        ]
    }
