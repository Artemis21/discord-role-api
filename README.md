# Discord Role API

A discord bot that exposes an API to get users' roles for a specific server.

 - [Setup](#setup)
 - [API](#api)

## Setup

 1. Get a bot token for Discord ([instructions here](https://github.com/discord-apps/bot-tutorial#how-to-create-an-application)).
 2. Get the ID of the server you want to set the bot up for ([instructions here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)).
 3. Create a file called `config.json` that looks like this:
    ```json
    {
        "bot_token": "YOUR-VERY-LONG-BOT-TOKEN",
        "guild_id": 123456789012345
    }
    ```
 4. Make sure you have Python installed (must be version 3 and at least 3.9). You can download it [here](https://www.python.org/downloads/), and on Linux you may be able to install it with your package manager (some Linux distros come with older versions of Python, so if you're using a built in Python installation check the version number).
 5. Install the dependencies from PyPI. The command you run to do this depends on how you installed Python, but it will be something like `python3 -m pip install -Ur requirements.txt`. If that doesn't work, try replacing `python3` with `python`, `python3.9`, `py`, `py3` or `py3.9`.
 6. Run the server: `python3 -m uvicorn app:server`. You can specify the port/address to bind to with the `--host` and `--port` options, but beware that this service is only intended to run on localhost. You should make sure to include some authentication if you expose it to the web.

## API

The API currently exposes only two endpoints:

#### `GET /users/{user_id}/roles`

`{user_id}`, of course, should be replaced with the ID of the user whose roles you wish to get. It will return a JSON object with one key, `roles`, which maps to a list of `role` objects. A `role` object has two keys, `name` and `id`, mapping to the name and ID of the role respectively.

Example response:
```json
{
    "roles": [
        {
            "name": "Administrator",
            "id": 123456789012345
        },
        {
            "name": "Member",
            "id": 423491978162852
        }
    ]
}
```

If the user is not found, a 404 status code will be returned.

#### `GET /bans`

Requires `Ban Members` permission

This will return a JSON object with one key, `bans`, which maps to a list of bans, starting with a `user` JSON object, followed by a `reason` JSON object. This mimics discord.py's representation of [BanEntry](https://discordpy.readthedocs.io/en/stable/api.html?highlight=banentry#discord.BanEntry)

Example response:
```json
{
    "bans":[
        {
        "user_id": 123456789012345,
        "user_name": "Member",
        "user_discriminator": "0001",
        "user_is_bot": false,
        "reason": "Banned for Nitro Scams"
        },
        {
        "user_id": 123456789012323,
        "user_name": "MemberTwo",
        "user_discriminator": "0002",
        "user_is_bot": false,
        "reason": "Banned for Nitro Scams"},
    ],
}
```
